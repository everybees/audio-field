from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from rest_framework.routers import DefaultRouter

import audio_book.views as av

router = DefaultRouter(trailing_slash=False)
app_router = routers.DefaultRouter()
app_router.register('audio', av.AudioViewSets, basename='audio')

urlpatterns = [
    path('', include(app_router.urls))
]