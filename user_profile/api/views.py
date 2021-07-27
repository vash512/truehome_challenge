# -*- coding: utf-8 -*-
from rest_framework import (permissions, status, views)
from rest_framework.exceptions import ParseError
# from rest_framework.exceptions import (
#     NotFound, PermissionDenied, ValidationError)
from rest_framework.response import Response


from . import serializers


class UserLoginAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        from rest_framework.authtoken.models import Token
        from django.contrib.auth.models import User

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username', None)
            password = request.data.get('password', None)

            if username:
                user = User.objects.filter(username=username).first()
                if not user:
                    raise ParseError("Unregister user.")

            if user:
                if not user.check_password(password):
                    raise ParseError("Invalid credentials.")

            auth_token = getattr(user, "auth_token", None)
            if not auth_token:
                user.auth_token, is_created = Token.objects\
                    .get_or_create(user=user)

            user_serializer = serializers.UserProfileSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
