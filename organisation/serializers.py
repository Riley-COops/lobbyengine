from rest_framework import serializers
from .models import *
from authentication.models import OrganisationProfile


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = "__all__"
        read_only_fields = ["organisation","created_at"]

    def create(self, validated_data):
        org_profile = OrganisationProfile.objects.get(user=self.context['request'].user)
        validated_data['organisation'] = org_profile
        return super().create(validated_data)
    

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = "__all__"
        read_only_fields = ["joined_at"]


