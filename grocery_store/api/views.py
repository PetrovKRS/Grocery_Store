from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets, mixins
from rest_framework.permissions import (
    AllowAny, IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response

from users.models import User
from products.models import (
    Category, SubCategory, Product, ShoppingCart
)
from .serializers import (
    CategorySerializer, ProductSerializer,
    ShoppingCartSerializer, ShoppingCartItemSerializer,
)
from .permissions import (
    IsShoppingCartOwner, IsShoppingCartItemOwner
)


class CustomUserViewSet(UserViewSet):
    permission_classes = (AllowAny,)

class CategoryViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet):
    """ Categories list with subcategories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet):
    """ Products list. """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ShoppingCartViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet):
    """ Получение списка товаров в корзине пользователя. """

    serializer_class = ShoppingCartSerializer
    permission_classes = (IsShoppingCartOwner,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return ShoppingCart.objects.filter(
                user=user
            )
        return []


class ShoppingCartItemViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """ Добавление, изменение, удаление товаров в корзине. """

    serializer_class = ShoppingCartItemSerializer
    Permission_classes = (AllowAny,)

    def get_queryset(self):
        shopping_cart = get_object_or_404(
            ShoppingCart, id=self.kwargs.get('shopping_cart_id'))
        queryset = shopping_cart.cart_items.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            cart_id=self.kwargs.get('shopping_cart_id')
        )

    def create(self, request, *args, **kwargs):
        """Добавить продукты в корзину"""
        request.data['cart'] = self.kwargs.get('shopping_cart_id')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        """Изменить количество продукта в корзине"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if instance.id is None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        """ Очистка корзины."""

        instance = self.get_queryset()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
