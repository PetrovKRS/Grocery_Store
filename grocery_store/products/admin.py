from django.contrib import admin

from grocery_store.settings import EMPTY_VALUE
from products.models import (
    Category, SubCategory, Product, ShoppingCart,
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
        'slug', 'image_size_a',
        'image_size_b', 'image_size_c',
        'price',
    )
    prepopulated_fields = {
        'slug': ('name',),
    }
    prepopulated_fields = {
        'slug': ('name',),
    }
