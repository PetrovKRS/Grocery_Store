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
    mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """ Получение списка товаров в корзине пользователя. """

    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsShoppingCartOwner,)


class ShoppingCartItemViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """ Добавление, изменение, удаление товаров в корзине. """

    serializer_class = ShoppingCartItemSerializer
    Permission_classes = (IsShoppingCartItemOwner,)

    def get_queryset(self):
        shopping_cart = get_object_or_404(
            ShoppingCart, id=self.kwargs.get('shopping_cart_id'))
        queryset = shopping_cart.shopping_cart_items.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            shopping_cart_id=self.kwargs.get('shopping_cart_id')
        )

    def create(self, request, *args, **kwargs):
        """ Добавление продукта в корзину. """

        request.data['shopping_cart'] = self.kwargs.get('shopping_cart_id')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        """ Изменение кол-ва продукта в корзине. """

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
        """ Очистка корзины. """

        instance = self.get_queryset()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
