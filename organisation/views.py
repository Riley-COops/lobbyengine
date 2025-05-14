# views.py

from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.models import CustomUser, OrganisationProfile
from .models import Team, TeamMember
from .serializers import TeamSerializer, TeamMemberSerializer
from authentication.permissions import IsOrganisation
from rest_framework.decorators import action

# Team CRUD view (create + list only for orgs)
class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, IsOrganisation]

    def get_queryset(self):
        org_profile = OrganisationProfile.objects.get(user=self.request.user)
        return Team.objects.filter(organisation=org_profile)

    def perform_create(self, serializer):
        org_profile = OrganisationProfile.objects.get(user=self.request.user)
        serializer.save(organisation=org_profile)


# Add members to a team
class AddMemberView(generics.CreateAPIView):
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAuthenticated, IsOrganisation]

    def create(self, request, *args, **kwargs):
        team_id = self.kwargs['team_id']
        try:
            team = Team.objects.get(id=team_id, organisation__user=request.user)
        except Team.DoesNotExist:
            return Response({"detail": "Team not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)

        user_email = request.data.get('email')
        role = request.data.get('role', 'member')

        try:
            user = CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User with that email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        membership, created = TeamMember.objects.get_or_create(team=team, user=user, defaults={'role': role})
        if not created:
            return Response({"detail": "User already in team."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(membership)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Remove member from team
class RemoveMemberView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOrganisation]

    def delete(self, request, *args, **kwargs):
        team_id = self.kwargs['team_id']
        user_id = self.kwargs['user_id']

        try:
            team = Team.objects.get(id=team_id, organisation__user=request.user)
            membership = TeamMember.objects.get(team=team, user__id=user_id)
            membership.delete()
            return Response({"detail": "Member removed."}, status=status.HTTP_204_NO_CONTENT)
        except (Team.DoesNotExist, TeamMember.DoesNotExist):
            return Response({"detail": "Team or member not found."}, status=status.HTTP_404_NOT_FOUND)
