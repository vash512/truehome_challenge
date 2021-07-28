# -*- coding: utf-8 -*-
from activity.models import (
    Activity,
    ActivityCancelledError,
    ChangeSchedulesError,
    DisabledPropertyError,
    SimilarSchedulesError,
    Survey
)


from django.utils import timezone

from property.models import Property

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError


class ActivityBusinessValidation:
    """Check the Business Logics on saved objects.."""

    def save(self, *args, **kwargs):
        try:
            return super().save(*args, **kwargs)
        except ActivityCancelledError:
            raise PermissionDenied("Canceled activities cannot be modified.")
        except DisabledPropertyError:
            raise ValidationError({
                "property": "You cannot create activities to a "
                "disabled property."
            })
        except ChangeSchedulesError:
            raise ValidationError({
                "schedule": "Only the date can be changed, not the time."
            })
        except SimilarSchedulesError:
            raise ValidationError({
                "schedule": "Similar schedules already exist for "
                "this Property."
            })
        except Exception as e:
            raise e


class ActivitySerializer(
    ActivityBusinessValidation, serializers.ModelSerializer
):

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


class ActivityUpdateSerializer(
    ActivityBusinessValidation, serializers.ModelSerializer
):

    class Meta:
        model = Activity
        fields = "__all__"
        read_only_fields = [
            "property",
            "title",
            "created_at",
            "updated_at"
        ]


class SurveySerializer(serializers.ModelSerializer):

    class Meta:
        model = Survey
        fields = "__all__"
