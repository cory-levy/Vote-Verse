from django.shortcuts import get_object_or_404, render
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Choice, Profile, Question, School, Vote, VoteUser
from .serializers import (
    ChangePasswordSerializer,
    ChoiceSerializer,
    ProfileSerializer,
    QuestionSerializer,
    RegisterSerializer,
    SchoolSerializer,
    VoteSerializer,
)

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
