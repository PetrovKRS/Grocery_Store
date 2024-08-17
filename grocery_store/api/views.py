from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, mixins
from rest_framework.permissions import (
    AllowAny, IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response

from products.models import (
    Category, SubCategory, Product, ShoppingCart
)
from .serializers import (
    CategorySerializer, ProductSerializer,
)
from users.models import User


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ Categories list with subcategories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ Product list. """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
