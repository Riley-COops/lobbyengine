from django.contrib.auth import authenticate
from djoser.conf import settings
from djoser.serializers import TokenCreateSerializer
from django.contrib.auth.models import User
# serializers.py
from rest_framework import serializers
from .models import Profile

class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
        ]
    def validate_email(sellf, email):
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                raise serializers.ValidateError(
                    "Email is already registered with another user"
                )
        except User.DoesNotExist:
            pass
        return email

    
    def create(self, validated_data):
        data = validated_data.copy()
        user = User.objects.create_user(**data)
        profile = Profile.objects.create(user=user)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class CustomTokenCreateSerializer(TokenCreateSerializer):

    def validate(self, attrs):
        password = attrs.get("password")
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        # We changed only below line
        if self.user: # and self.user.is_active: 
            return attrs
        self.fail("invalid_credentials")