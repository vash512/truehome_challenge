# -*- coding: utf-8 -*-
from django.conf.urls import include, url

from rest_framework.authtoken import views

from user_profile.api.views import UserLoginAPIView

urlpatterns = [
    url(r'^api-auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    url(r'^token-auth/', views.obtain_auth_token),

    url(r'^login/', UserLoginAPIView.as_view(), name='login'),
    url(r'^property/', include("property.api.urls", namespace='property')),
    url(r'^activity/', include("activity.api.urls", namespace='activity')),
]
