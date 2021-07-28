# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from datetime import timedelta

from activity.models import Activity, get_datetime_mx

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from property.models import Property

# Django Rest Framework
from rest_framework import status
from rest_framework.test import APIClient


class ActivityTestCase(TestCase):
    fixtures = ["auth.json", "property.json", "activity.json"]

    def setUp(self):
        self.user = User.objects.get(email="root_test@test.com")
        self.enabled_property = Property.objects\
            .filter(status="enabled").first()
        self.disabled_property = Property.objects\
            .filter(status="disabled").first()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    # Schedule Activities
    def test_api_activity_create(self):
        response = self.client.post(
            "/api/activity/",
            {
                "schedule": "2021-07-28 11:00:00",
                "title": "activity title test",
                "status": "active",
                "property": self.enabled_property.id
            },
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        activity_attrs = [
            "id",
            "schedule",
            "title",
            "created_at",
            "updated_at",
            "status",
            "property",
        ]
        self.assertTrue(
            all([activity_attr in response_data
                 for activity_attr in activity_attrs])
        )

    def test_api_activity_create_disabled_propertyerror(self):
        response = self.client.post(
            "/api/activity/",
            {
                "schedule": "2021-07-28 11:00:00",
                "title": "activity error test",
                "status": "active",
                "property": self.disabled_property.id
            },
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content)
        self.assertIn("property", response_data)

    def test_api_activity_create_similar_schedules_error(self):

        active_activity = Activity.objects.filter(status="active").first()
        base_context = {
            "title": "activity error test",
            "status": "active",
            "property": self.enabled_property.id
        }

        # schedule in same active_activity.schedule
        base_context["schedule"] = get_datetime_mx(active_activity.schedule)\
            .strftime('%Y-%m-%d %H:%M:%S')
        response = self.client.post(
            "/api/activity/", base_context, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content)
        self.assertIn("schedule", response_data)

        # schedule plus 59 minutes active_activity.schedule
        base_context["schedule"] = get_datetime_mx(
            active_activity.schedule + timedelta(seconds=60 * 59)
        ).strftime('%Y-%m-%d %H:%M:%S')
        response = self.client.post(
            "/api/activity/", base_context, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content)
        self.assertIn("schedule", response_data)

        # schedule less 59 minutes active_activity.schedule
        base_context["schedule"] = get_datetime_mx(
            active_activity.schedule - timedelta(seconds=60 * 59)
        ).strftime('%Y-%m-%d %H:%M:%S')
        response = self.client.post(
            "/api/activity/", base_context, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content)
        self.assertIn("schedule", response_data)

    # Reschedule Activities
    def test_api_activity_update(self):
        activity = Activity.objects.filter(status="active").first()
        activity_new_schedule = get_datetime_mx(
            activity.schedule + timedelta(days=5)
        ).strftime('%Y-%m-%d %H:%M:%S')
        response = self.client.put(
            "/api/activity/%s/" % (activity.id),
            {
                "schedule": activity_new_schedule,
            },
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_activity_update_change_schedules_error(self):
        activity = Activity.objects.filter(status="active").first()
        activity_new_schedule = get_datetime_mx(
            activity.schedule + timedelta(hours=1)
        ).strftime('%Y-%m-%d %H:%M:%S')
        response = self.client.put(
            "/api/activity/%s/" % (activity.id),
            {
                "schedule": activity_new_schedule,
            },
            format="json"
        )
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("schedule", response_data)

    def test_api_activity_update_cancelled_error(self):
        activity = Activity.objects.filter(status="cancelled").first()
        activity_same_schedule = get_datetime_mx(
            activity.schedule
        ).strftime('%Y-%m-%d %H:%M:%S')
        response = self.client.put(
            "/api/activity/%s/" % (activity.id),
            {
                "schedule": activity_same_schedule,
            },
            format="json"
        )
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response_data)

    # Cancel Activities
    def test_api_activity_destoy(self):
        activity = Activity.objects.filter(status="active").first()
        response = self.client.delete("/api/activity/%s/" % (activity.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(
            Activity.objects.filter(
                status="cancelled",
                id=activity.id).exists())

    # Activities list
    def test_api_activity_list(self):
        response = self.client.get("/api/activity/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = json.loads(response.content)
        self.assertIsInstance(response_data, list)
        first_activity_list = response_data[0]

        activity_attrs = [
            "id",
            "schedule",
            "title",
            "created_at",
            "status",
            "condition",
            "property",
            "survey",
        ]

        self.assertTrue(
            all([activity_attr in first_activity_list
                 for activity_attr in activity_attrs])
        )

        property_attrs = [
            "id",
            "title",
            "address",
        ]
        self.assertTrue(
            all([property_attr in first_activity_list["property"]
                 for property_attr in property_attrs])
        )

    def test_api_activity_retrieve(self):
        activity = Activity.objects.filter(status="active").first()
        response = self.client.get("/api/activity/%s/" % activity.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = json.loads(response.content)

        activity_attrs = [
            "id",
            "schedule",
            "title",
            "created_at",
            "status",
            "condition",
            "property",
            "survey",
        ]

        self.assertTrue(
            all([activity_attr in response_data
                 for activity_attr in activity_attrs])
        )

        property_attrs = [
            "id",
            "title",
            "address",
        ]
        self.assertTrue(
            all([property_attr in response_data["property"]
                 for property_attr in property_attrs])
        )

    def test_api_activity_retrieve_pending(self):
        """
        Pending to be carried out.

        If the activity has an active status and the schedule date on which
        the activity will be carried out is greater than or equal to the
        current date, then the condition is: Pending to be carried out
        """

        activity = Activity.objects.create(
            property_id=1,
            schedule=timezone.now() + timedelta(days=1),
            title="activity test",
            status="active",
        )
        response = self.client.get("/api/activity/%s/" % activity.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = json.loads(response.content)

        self.assertEqual(response_data["condition"], "Pendiente a realizar")

    def test_api_activity_retrieve_overdue(self):
        """
        Overdue.

        If the activity has an active status and the schedule date on which it
        will take place is less than the current date, then the condition is:
        Overdue
        """
        activity = Activity.objects.create(
            property_id=1,
            schedule=timezone.now() - timedelta(days=1),
            title="activity test",
            status="active",
        )
        response = self.client.get("/api/activity/%s/" % activity.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = json.loads(response.content)

        self.assertEqual(response_data["condition"], "Atrasada")

    def test_api_activity_retrieve_finished(self):
        """
        Finished.

        If the activity has the status of done, the condition is: Finished
        """
        activity = Activity.objects.filter(status="done").first()
        response = self.client.get("/api/activity/%s/" % activity.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(response_data["condition"], "Finalizada")

    def test_api_activity_retrieve_cancelled(self):

        activity = Activity.objects.filter(status="cancelled").first()
        response = self.client.get("/api/activity/%s/" % activity.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(response_data["condition"], None)
        pass
