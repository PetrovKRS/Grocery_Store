from django.urls import include, path, re_path
from django.utils.text import re_words
from rest_framework import routers

# from views import (
#     CustomUserViewSet,
# )

app_name = 'api'

router = routers.DefaultRouter()

# router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
]
