from activity.models import Activity

from django.contrib import admin

from .models import Property


class ActivityInline(admin.StackedInline):
    model = Activity
    extra = 0
    show_change_link = True


class PropertyAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        "address",
        "description",
        "created_at",
        "updated_at",
        "disabled_at",
        "status",
    ]
    list_filter = ["status", "created_at", "updated_at", "disabled_at"]
    inlines = [
        ActivityInline,
    ]
    readonly_fields = ["created_at", "updated_at", ]
    search_fields = ["title", "address", "description", ]

admin.site.register(Property, PropertyAdmin)
