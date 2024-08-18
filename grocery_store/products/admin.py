from itertools import product

from django.contrib import admin

from grocery_store.settings import EMPTY_VALUE
from products.models import (
    Category, SubCategory, Product, ShoppingCart,
    ShoppingCartItem,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug', 'image'
    )
    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug', 'image', 'category'
    )
    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'subcategory', 'name',
        'price', 'slug', 'image_size_a',
        'image_size_b', 'image_size_c',
    )
    prepopulated_fields = {
        'slug': ('name',),
    }
    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user',
        'total_count', 'total_coast'
    )
    readonly_fields = (
        'total_count', 'total_coast'
    )


@admin.register(ShoppingCartItem)
class ShoppingCartItemAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'shopping_cart', 'product',
        'count', 'price',
        'total_coast',
    )
    readonly_fields = ('price',)

    def total_coast(self, obj):
        """ Общая цена за кол-во товара. Добавляем
            цену единицы для каждого товара в корзине. """

        price = obj.product.price
        obj.price = price
        obj.save()
        return obj.price * obj.count
