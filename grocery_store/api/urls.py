from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework import routers

from .views import (
    CategoryViewSet, ProductViewSet,
    ShoppingCartViewSet, ShoppingCartItemViewSet,
)

app_name = 'api'

router = routers.DefaultRouter()

# router.register(r'users', UserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'shopping_cart', ShoppingCartViewSet, basename='shopping_cart')
router.register(
   r'shopping_cart/(?P<shopping_cart_id>\d+)/shopping_cart_item',
   ShoppingCartItemViewSet, basename='cart_item'
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
