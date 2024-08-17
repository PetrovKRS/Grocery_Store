from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework import routers

from .views import (
    CategoryViewSet, ProductViewSet,
    # ShoppingCart,
)

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
]
