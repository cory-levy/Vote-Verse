from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasScope, TokenHasReadWriteScope

from .serializers import RegisterSerializer, ChangePasswordSerializer, ProfileSerializer
from .models import VoteUser, Profile

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
        TokenHasScope,
    ]
    required_scopes = ["write"]
    serializer_class = ChangePasswordSerializer
    

class RetrieveProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = ProfileSerializer
    
    def get_object(self):
        pk = self.kwargs['pk']
        queryset = self.get_queryset()
        
        obj = get_object_or_404(queryset, pk=pk)
        
        return obj
    