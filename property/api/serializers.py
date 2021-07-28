# -*- coding: utf-8 -*-
# from django.contrib.auth.models import User
from activity.api.serializers import ActivitySerializer

from property.models import Property

from rest_framework import serializers


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = "__all__"


class PropertyRetrieveSerializer(PropertySerializer):
    activities = ActivitySerializer(many=True)
