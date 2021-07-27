from django.contrib import admin

from .models import Activity, Survey


class SurveyInline(admin.StackedInline):
    model = Survey
    extra = 0


class ActivityAdmin(admin.ModelAdmin):
    list_display = [
        "property",
        "schedule",
        "title",
        "created_at",
        "updated_at",
        "status",
    ]
    list_filter = ["created_at", "updated_at", "status", ]
    inlines = [
        SurveyInline,
    ]
    readonly_fields = ["created_at", "updated_at"]
    search_fields = ["property", "schedule", "title", ]

admin.site.register(Activity, ActivityAdmin)
