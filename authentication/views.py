from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, PersonalSerializer, InvestorSerializer, OrganisationSerializer, AddOrganisationToInvestorSerializer

from .permissions import IsInvestor, IsOrganisation, IsPersonal, IsInvestorOrOrganisation

from .models import PersonalProfile, InvestorProfile, OrganisationProfile

class CustomRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


        

class InvestorProfileView(APIView):
    permission_classes = [IsAuthenticated, IsInvestor]

    def get(self, request):
        try: 
            profile = InvestorProfile.objects.get(user=request.user)
            serializer = InvestorSerializer(profile)
            return Response(serializer.data)
        except InvestorProfile.DoesNotExist:
            return Response({"message":"Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        

    def put(self, request):
        try:
            profile = InvestorProfile.objects.get(user=request.user)
            serializer = InvestorSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except InvestorProfile.DoesNotExist:
            return Response({"message":"Profile not found"}, status=status.HTTP_404_NOT_FOUND)


class OrganisationProfileView(APIView):
    permission_classes = [IsAuthenticated, IsOrganisation]

    def get(self, request):
        try:
            profile = OrganisationProfile.objests.get(user=request.user)
            serializer = OrganisationSerializer(profile)
            return Response(serializer.data)
        except OrganisationProfile.DoesNotExist:
            return Response({"message":"Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        

    def put(self, request):
        try:
            profile = OrganisationProfile.objects.get(user=request.user)
            serializer = OrganisationSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except OrganisationProfile.DoesNotExist:
            return Response({"message":"Profile not found"}, status=status.HTTP_404_NOT_FOUND)
                

class UnifiedProfileView(APIView):
    permission_classes = [IsAuthenticated, IsInvestorOrOrganisation]

    def get(self, request):
        account_type = request.user.account_type
        print("Authenticated user:", request.user, "Account type:", account_type)

        if account_type == 'investor':
            try:
                profile = InvestorProfile.objects.get(user=request.user)
                serializer = InvestorSerializer(profile)
                return Response(serializer.data)
            except InvestorProfile.DoesNotExist:
                return Response({"message": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        elif account_type == 'organisation':
            try:
                profile = OrganisationProfile.objects.get(user=request.user)
                serializer = OrganisationSerializer(profile)
                return Response(serializer.data)
            except OrganisationProfile.DoesNotExist:
                return Response({"message": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Invalid account type"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        account_type = request.user.account_type

        if account_type == 'investor':
            try:
                profile = InvestorProfile.objects.get(user=request.user)
                serializer = InvestorSerializer(profile, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except InvestorProfile.DoesNotExist:
                return Response({"message": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        elif account_type == 'organisation':
            try:
                profile = OrganisationProfile.objects.get(user=request.user)
                serializer = OrganisationSerializer(profile, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except OrganisationProfile.DoesNotExist:
                return Response({"message": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Invalid account type"}, status=status.HTTP_400_BAD_REQUEST)

 
    
class AddOrganisationToInvestorView(APIView):
    permission_classes = [IsAuthenticated, IsInvestor]

    def post(self, request):
        serializer = AddOrganisationToInvestorSerializer(data=request.data)
        if serializer.is_valid():
            organisation = serializer.save()
            return Response({"message":f"Organisation '{organisation.organisation_name}' added"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PersonalProfileView(APIView):
    permission_classes = [IsAuthenticated, IsPersonal]

    def get(self, request):
        try:
            profile = PersonalProfile.objects.get(user=request.user)
            serializer = PersonalSerializer(profile)
            return Response(serializer.data)
        except PersonalProfile.DoesNotExist:
            return Response({"message":"Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request):
        try:
            profile = PersonalProfile.objects.get(user=request.user)
            serializer = PersonalSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PersonalProfile.DoesNotExist:
            return Response({"message":"Profile not found"}, status=status.HTTP_404_NOT_FOUND)
