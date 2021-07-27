# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth.models import User
from django.test import TestCase

# Django Rest Framework
from rest_framework import status
from rest_framework.test import APIClient


class ProfileTestCase(TestCase):
    fixtures = ["auth.json"]

    def test_user_create(self):
        user = User(
            email="testing_new@test.com",
            first_name="Testing",
            last_name="Testing",
            username="testing_new"
        )
        user.set_password("admin123")
        user.save()

        self.assertIsInstance(user, User)
        self.assertTrue(hasattr(user, "auth_token"))

    def test_login(self):
        client = APIClient()
        response = client.post(
            "/api/login/",
            {
                "username": "root_test",
                "password": "root_test_password",
            },
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", json.loads(response.content))

    def test_non_existent_user(self):
        client = APIClient()
        response = client.post(
            "/api/login/",
            {
                "username": "non-existent_user",
                "password": "non-existent_user",
            },
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", json.loads(response.content))

    def test_wrong_password(self):
        client = APIClient()
        response = client.post(
            "/api/login/",
            {
                "username": "root_test",
                "password": "wrong password",
            },
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", json.loads(response.content))
