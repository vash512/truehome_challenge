# -*- coding: utf-8 -*-
# from django.contrib.auth.models import User

from activity.models import Activity, Survey

from django.utils import timezone

from property.models import Property

from rest_framework import serializers


class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = "__all__"


class PropertySimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = ["id", "title", "address"]


class ActivityRetrieveSerializer(serializers.ModelSerializer):
    condition = serializers.SerializerMethodField()
    property = PropertySimpleSerializer()
    survey = serializers.SerializerMethodField()

    def get_condition(self, obj):

        if obj.status == "done":
            return "Finalizada"
        elif obj.status == "active":
            if obj.schedule >= timezone.now():
                return "Pendiente a realizar"
            else:
                return "Atrasada"

    def get_survey(self, obj):
        from django.urls import reverse
        return reverse('api:activity:suervey', kwargs={'activity_id': obj.id})

    class Meta:
        model = Activity
        fields = [
            "id",
            "schedule",
            "title",
            "created_at",
            "status",
            "condition",
            "property",
            "survey",
        ]


class ActivityUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = "__all__"
        read_only_fields = [
            "property",
            "title",
            "created_at",
            "updated_at",
            "status",
        ]


class SurveySerializer(serializers.ModelSerializer):

    class Meta:
        model = Survey
        fields = "__all__"
