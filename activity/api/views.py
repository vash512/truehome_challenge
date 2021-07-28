# -*- coding: utf-8 -*-
from datetime import timedelta

from activity.models import Activity

from api.mixins import MultiSerializerModelViewSet

from django.utils import timezone

from rest_framework import permissions, views
from rest_framework.response import Response

from . import serializers


class ActivityViewSet(MultiSerializerModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = serializers.ActivityRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated]

    action_serializers = {
        "create": serializers.ActivitySerializer,
        "update": serializers.ActivityUpdateSerializer,
    }

    def get_queryset(self):
        """
        Filtering rules.

        1°.- If schedule_gte or schedule_lte is not sent, the filtering must
        comply with:
            (current_date - 3 days) <= schedule <= (current_date + 2 weeks)
        2°.- if sent, the first rule will be skipped and filtered by the
        range of dates given.

        """
        if self.action not in ["list"]:
            return Activity.objects.all()
        schedule_gte = self.request.query_params.get("schedule_gte")
        schedule_lte = self.request.query_params.get("schedule_lte")
        status = self.request.query_params.get("status")

        activity_filter = {}
        if schedule_gte or schedule_lte:
            if schedule_gte:
                activity_filter["schedule__gte"] = schedule_gte
            if schedule_lte:
                activity_filter["schedule__lte"] = schedule_lte
        else:
            now = timezone.now()
            activity_filter["schedule__gte"] = now - timedelta(days=3)
            activity_filter["schedule__lte"] = now + timedelta(days=14)

        if status:
            activity_filter["status__iexact"] = status

        return Activity.objects.filter(**activity_filter)


class SurveyView(views.APIView):
    serializer_class = serializers.SurveySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response()
