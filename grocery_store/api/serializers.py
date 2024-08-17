from rest_framework import exceptions, serializers

from products.models import (
    Category, SubCategory, Product, ShoppingCart
)
from users.models import User


class SubCategorySerializer(serializers.ModelSerializer):
    """ SubCategories list. """

    class Meta:
        model = SubCategory
        fields = (
            'name', 'slug', 'image',
        )


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(
        many=True
    )

    class Meta:
        model = Category
        fields = (
            'subcategories', 'name', 'slug', 'image',
        )


class ProductSerializer(serializers.ModelSerializer):

    category = serializers.SerializerMethodField()
    subcategory = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = (
            'name', 'slug', 'category', 'subcategory',
            'price', 'image_size_a', 'image_size_b',
            'image_size_c',
        )

    def get_category(self, obj):
        return obj.subcategory.category.name
