from rest_framework import permissions

from products.models import ShoppingCart


class IsShoppingCartOwner(permissions.BasePermission):
    """ Доступ к своей корзине. """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsShoppingCartItemOwner(permissions.BasePermission):
    """ Действия со своей корзиной. """

    def has_permission(self, request, view):
        shopping_cart = ShoppingCart.objects.get(
            id=view.kwargs.get('shopping_cart_id')
        )
        return shopping_cart.user == request.user
