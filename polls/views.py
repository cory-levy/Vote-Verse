from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.contrib.auth import get_user_model
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from oauth2_provider.models import Application, AccessToken, RefreshToken
from oauthlib import common
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from friendship.models import FriendshipRequest, Friend
from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError

from .models import Choice, Profile, Question, School, Vote, VoteUser
from .serializers import (
    ChangePasswordSerializer,
    ChoiceSerializer,
    ProfileSerializer,
    QuestionSerializer,
    RegisterSerializer,
    SchoolSerializer,
    VoteSerializer,
    FriendSerializer,
    FriendshipRequestSerializer,
    FriendshipRequestResponseSerializer,
)
from .utils import generate_otp, send_otp_email

# Create your views here.


class RegisterView(generics.CreateAPIView):
    queryset = VoteUser.objects.all()
    permission_classes = [
        AllowAny,
    ]
    serializer_class = RegisterSerializer


class ChangePasswordView(generics.UpdateAPIView):
    queryset = VoteUser.objects.all()
    permission_classes = [
        IsAuthenticated,
        TokenHasReadWriteScope,
    ]
    serializer_class = ChangePasswordSerializer


class RetrieveProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = ProfileSerializer


class ListVoteView(generics.ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]


class RetrieveVoteView(generics.RetrieveAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]


class ListChoiceView(generics.ListAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]


class RetrieveChoiceView(generics.RetrieveAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]


class ListQuestionView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]


class RetrieveQuestionView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]


class CreateQuesitonView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]


class CreateChoiceView(generics.CreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]


class CreateVoteView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]


class ListSchoolView(generics.ListAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]


class RetrieveSchoolView(generics.RetrieveAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]


class CreateSchoolView(generics.CreateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", "")
        try:
            user = VoteUser.objects.get(email=email)
        except VoteUser.DoesNotExist:
            return Response(
                {"error": "Email does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        otp = generate_otp()
        user.otp = otp
        user.save()

        send_otp_email(email=email, otp=otp)

        return Response(
            {"success": f"OTP has been sent to {email}."}, status=status.HTTP_200_OK
        )


class ValidateOTP(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", "")
        otp = request.data.get("otp", "")
        client_id = request.data.get("client_id", "")

        try:
            user = VoteUser.objects.get(email=email)
        except VoteUser.DoesNotExist:
            return Response(
                {"error": "Email does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            application = Application.objects.get(client_id=client_id)
        except VoteUser.DoesNotExist:
            return Response(
                {"error": "Client does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        if user.otp == otp:
            user.otp = None
            user.save()

            expires = timezone.now() + timezone.timedelta(seconds=300)
            access_token = AccessToken(
                user=user,
                scope="read write groups",
                expires=expires,
                token=common.generate_token(),
                application=application,
            )
            access_token.save()
            refresh_token = RefreshToken(
                user=user,
                token=common.generate_token(),
                application=application,
                access_token=access_token,
            )
            refresh_token.save()

            response_data = {
                "access_token": access_token.token,
                "expires_in": 300,
                "token_type": "Bearer",
                "scope": access_token.scope,
                "refresh_token": refresh_token.token,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST
            )


class FriendViewSet(viewsets.ModelViewSet):
    serializer_class = FriendSerializer

    def list(self, request):
        friend_requests = Friend.objects.friends(user=request.user)
        self.queryset = friend_requests
        self.http_method_names = [
            "get",
            "head",
            "options",
        ]
        return Response(FriendSerializer(friend_requests, many=True).data)

    def retrieve(self, request, pk=None):
        self.queryset = Friend.objects.friends(user=request.user)
        requested_user = get_object_or_404(get_user_model(), pk=pk)
        if Friend.objects.are_friends(request.user, requested_user):
            self.http_method_names = [
                "get",
                "head",
                "options",
            ]
            return Response(FriendSerializer(requested_user, many=False).data)
        else:
            return Response(
                {"message": "Friend relationship not found for user."},
                status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False)
    def requests(self, request):
        friend_requests = Friend.objects.unrejected_requests(user=request.user)
        self.queryset = friend_requests
        return Response(FriendshipRequestSerializer(friend_requests, many=True).data)

    @action(detail=False)
    def sent_requests(self, request):
        friend_requests = Friend.objects.sent_requests(user=request.user)
        self.queryset = friend_requests
        return Response(FriendshipRequestSerializer(friend_requests, many=True).data)

    @action(detail=False)
    def rejected_requests(self, request):
        friend_requests = Friend.objects.rejected_requests(user=request.user)
        self.queryset = friend_requests
        return Response(FriendshipRequestSerializer(friend_requests, many=True).data)

    @action(
        detail=False, serializer_class=FriendshipRequestSerializer, methods=["post"]
    )
    def add_friend(self, request, username=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        to_user = get_object_or_404(
            get_user_model(), username=serializer.validated_data.get("to_user")
        )

        try:
            friend_obj = Friend.objects.add_friend(
                # The sender
                request.user,
                # The recipient
                to_user,
                # Message (...or empty str)
                message=request.data.get("message", ""),
            )
            return Response(
                FriendshipRequestSerializer(friend_obj).data, status.HTTP_201_CREATED
            )
        except (AlreadyExistsError, AlreadyFriendsError) as e:
            return Response({"message": str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False, serializer_class=FriendshipRequestSerializer, methods=["post"]
    )
    def remove_friend(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        to_user = get_object_or_404(
            get_user_model(), username=serializer.validated_data.get("to_user")
        )

        if Friend.objects.remove_friend(request.user, to_user):
            message = "Friend deleted."
            status_code = status.HTTP_204_NO_CONTENT
        else:
            message = "Friend not found."
            status_code = status.HTTP_400_BAD_REQUEST

        return Response({"message": message}, status=status_code)

    @action(
        detail=False,
        serializer_class=FriendshipRequestResponseSerializer,
        methods=["post"],
    )
    def accept_request(self, request, id=None):
        id = request.data.get("id", None)
        friendship_request = get_object_or_404(FriendshipRequest, pk=id)

        if not friendship_request.to_user == request.user:
            return Response(
                {"message": "Request for current user not found."},
                status.HTTP_400_BAD_REQUEST,
            )

        friendship_request.accept()
        return Response(
            {"message": "Request accepted, user added to friends."},
            status.HTTP_201_CREATED,
        )

    @action(
        detail=False,
        serializer_class=FriendshipRequestResponseSerializer,
        methods=["post"],
    )
    def reject_request(self, request, id=None):
        id = request.data.get("id", None)
        friendship_request = get_object_or_404(FriendshipRequest, pk=id)
        if not friendship_request.to_user == request.user:
            return Response(
                {"message": "Request for current user not found."},
                status.HTTP_400_BAD_REQUEST,
            )

        friendship_request.reject()

        return Response(
            {"message": "Request rejected, user NOT added to friends."},
            status.HTTP_201_CREATED,
        )
