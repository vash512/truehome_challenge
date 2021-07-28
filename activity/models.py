from datetime import timedelta

from django.contrib.postgres.fields import JSONField
from django.db import models

from property.models import Property


class DisabledPropertyError(Exception):
    pass


class SimilarSchedulesError(Exception):
    pass


class ChangeSchedulesError(Exception):
    pass


class ActivityCancelledError(Exception):
    pass


def get_datetime_mx(datetime_utc):
    import pytz
    cdmx_tz = pytz.timezone("America/Mexico_City")
    return datetime_utc.astimezone(cdmx_tz)


class Activity(models.Model):

    STATUS_CHOICES = (
        ("active", u"Active"),
        ("done", u"Done"),
        ("cancelled", u"Cancelled"),
    )
    property = models.ForeignKey(Property, related_name="activities")
    schedule = models.DateTimeField()
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=35, choices=STATUS_CHOICES)

    def save(self, *args, **kwargs):
        is_created = True if self.pk is None else False
        if self.property.status == "disabled":
            raise DisabledPropertyError("Disabled Property.")

        if not is_created:
            original_schedule, original_status = Activity.objects\
                .values_list("schedule", "status").get(id=self.id)
            original_schedule = get_datetime_mx(original_schedule)
            print(original_schedule)
            print(original_status)

            if original_status == "cancelled":
                # un objeto cancelado ya no se puede modificar
                return

            # print(original_schedule, "  ", original_schedule.time())
            # print(self.schedule, "  ", self.schedule.time())
            if original_schedule.time() != self.schedule.time():
                raise DisabledPropertyError(
                    "Only the date can be changed, not the time."
                )

        if not self.check_schedule_availability(is_created):
            raise SimilarSchedulesError(
                "Similar schedules already exist for this Property."
            )
        super(Activity, self).save(*args, **kwargs)

    def check_schedule_availability(self, is_created):
        activities_queryset = self.property.activities.filter(
            schedule__gt=self.schedule - timedelta(hours=1),
            schedule__lt=self.schedule + timedelta(hours=1)
        ).exclude(status="cancelled")
        if not is_created:
            activities_queryset = activities_queryset.exclude(id=self.id)

        return not activities_queryset.exists()

    def delete(self):
        if self.status != "cancelled":
            self.status = "cancelled"
            Activity.objects.filter(id=self.id).update(status="cancelled")

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activitys"

    def __str__(self):
        return self.title


class Survey(models.Model):
    activity = models.OneToOneField(Activity)
    answers = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"

    def __str__(self):
        pass
