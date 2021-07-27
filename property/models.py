from django.db import models


class Property(models.Model):
    title = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    disabled_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=35)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Propertys"

    def __str__(self):
        return self.title
