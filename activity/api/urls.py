from activity.api.views import ActivityViewSet, SurveyView

from django.conf.urls import include, url

from rest_framework import routers

router = routers.DefaultRouter()
router.register('', ActivityViewSet)

urlpatterns = [
    url(r'^(?P<activity_id>[-\d]+)/survey',
        SurveyView.as_view(), name="suervey"),
    url('', include(router.urls)),
]
