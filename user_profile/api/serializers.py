# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from rest_framework import serializers


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True, write_only=True,
        style={'input_type': 'password'})


class UserProfileSerializer(serializers.ModelSerializer):
    token = serializers.ReadOnlyField(source="auth_token.key")
    name = serializers.ReadOnlyField(source="first_name")

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "name",
            "token",
        ]
        read_only_fields = ["email"]
