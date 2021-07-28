from django.conf.urls import include, url

from property.api.views import PropertyViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register('', PropertyViewSet)

urlpatterns = [
    url('', include(router.urls)),
]
