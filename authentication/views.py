# views.py
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .serializers import CustomUserSerializer, ProfileSerializer
from .models import CustomUser, Profile
from djoser.views import UserViewSet

class UserRegistrationView(UserViewSet):
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': CustomUserSerializer(user, context=self.get_serializer_context()).data,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)