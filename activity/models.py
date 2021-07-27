from django.contrib.postgres.fields import JSONField
from django.db import models

from property.models import Property


class Activity(models.Model):
    property = models.ForeignKey(Property)
    schedule = models.DateTimeField()
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=35)

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activitys"

    def __str__(self):
        return self.title


class Survey(models.Model):
    activity = models.ForeignKey(Activity)
    answers = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"

    def __str__(self):
        pass
