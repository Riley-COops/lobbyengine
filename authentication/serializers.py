from django.contrib.auth import authenticate
from djoser.conf import settings
from djoser.serializers import TokenCreateSerializer

# serializers.py
from rest_framework import serializers
from .models import CustomUser, Profile

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'first_name', 'last_name']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['category', 'dob', 'location', 'skills']


class CustomTokenCreateSerializer(TokenCreateSerializer):

    def validate(self, attrs):
        password = attrs.get("password")
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        if not self.user:
            self.user = CustomUser.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        # We changed only below line
        if self.user: # and self.user.is_active: 
            return attrs
        self.fail("invalid_credentials")