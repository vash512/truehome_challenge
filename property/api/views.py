# -*- coding: utf-8 -*-
from api.mixins import MultiSerializerListRetrieveMix

from property.models import Property

from rest_framework import permissions

from . import serializers


class PropertyViewSet(MultiSerializerListRetrieveMix):
    queryset = Property.objects.all()
    serializer_class = serializers.PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    action_serializers = {
        "retrieve": serializers.PropertyRetrieveSerializer
    }
