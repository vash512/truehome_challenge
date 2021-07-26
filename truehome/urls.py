from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path

admin.site.site_header = "TrueHome Challenge"
admin.site.site_title = "TrueHome Challenge"
admin.site.index_title = "TrueHome Challenge"


urlpatterns = [
    path('', lambda request: redirect('admin/', permanent=False)),
    path('admin/', admin.site.urls),
]


if getattr(settings, "STATIC_FILES_BY_DJANGO", False):
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if getattr(settings, "MEDIA_FILES_BY_DJANGO", False):
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
