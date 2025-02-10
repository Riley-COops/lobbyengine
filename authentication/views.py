#rest
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

#local
from .serializers import UserCreationSerializer, ProfileSerializer
from authentication.models import Profile

#djoser
# from djoser.views import UserViewSet


#views
class AuthenticationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserCreationSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"success":True}, status.HTTP_201_CREATED)
        
        return Response(
            {"errors": serializers.errors, "success":False}, status=status.HTTP_400_BAD_REQUEST,
        )



class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({'error':'Profile deos not exist'}, status.status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(user_profile)

    def put(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)