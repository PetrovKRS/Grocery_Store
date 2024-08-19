from itertools import count, product

from attr.setters import validate
from djoser.serializers import UserSerializer
from rest_framework import exceptions, serializers

from products.models import (
    Category, SubCategory, Product, ShoppingCart,
    ShoppingCartItem,
)
from rest_framework.exceptions import ValidationError
from urllib3 import request
from users.models import User


class SubCategorySerializer(serializers.ModelSerializer):
    """ Список подкатегорий. """

    class Meta:
        model = SubCategory
        fields = (
            'name', 'slug', 'image',
        )


class CategorySerializer(serializers.ModelSerializer):
    """ Список категорий с подкатегориями. """

    subcategories = SubCategorySerializer(
        many=True,
    )

    class Meta:
        model = Category
        fields = (
            'name', 'slug', 'image', 'subcategories',
        )


class ProductSerializer(serializers.ModelSerializer):
    """ Список продуктов. """

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


class ShoppingCartItemProductSerializer(serializers.ModelSerializer):
    """ """

    product = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCartItem
        fields = ('product', 'count', 'price')

    def get_product(self, obj):
        return ProductSerializer(
            Product.objects.filter(
                id=obj.product.id
            ),
            context=self.context,
            many=True
        ).data


class ShoppingCartItemSerializer(serializers.ModelSerializer):
    """ Подготовка данных для добавления/удаления товара,
        изменение кол-ва товара. """

    shopping_cart = serializers.PrimaryKeyRelatedField(
        queryset=ShoppingCart.objects.all(),
        required=False
    )

    class Meta:
        model = ShoppingCartItem
        fields = (
            'shopping_cart', 'product', 'count', 'price',
        )

    def validate(self, data):
        """ Проверка на дубли товаров в корзине при добавлении.
            Проверка количества товара, что оно больше нуля. """

        request = self.context.get('request')
        if request.method == 'POST':
            if ShoppingCart.objects.filter(
                shopping_cart=data.get('shopping_cart'),
                product=data.get('product')
            ).exists():
                raise ValidationError(
                    'Нельзя повторно добавить товар в корзину, '
                    'но можно изменить количество!'
                )
            if data.get('count') <= 0:
                raise ValidationError(
                    'Количество добавляемого в корзину товара '
                    'должно быть больше нуля!'
                )
            return data

    def create(self, validated_data):
        """ Добавление нового товара в корзину. """

        shopping_cart = ShoppingCart.get(
            id=validated_data.get('shopping_cart_id')
        )
        product = validated_data.get('product')
        count = validated_data.get('count')
        price = product.price * count
        shopping_cart_item = ShoppingCartItem.objects.create(
            shopping_cart=shopping_cart,
            product=product,
            count=count,
            price=price
        )
        return shopping_cart_item

    def update(self, instance, validated_data):
        """ Изменение количества товара.
            Если введен 0 - товар будет удален. """

        count = validated_data.get('count')
        product = Product.objects.get(
            id=instance.product.id
        )
        instance.count += count
        instance.price = product.price * instance.count
        if instance.count <= 0:
            instance.delete()
        else:
            instance.save()
        return instance


class ShoppingCartSerializer(serializers.ModelSerializer):
    """ Список товаров в корзине пользователя с указанием общего
        кол-ва товаров и их суммарной стоймости. """

    products = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = (
            'products', 'total_count', 'total_coast',
        )

    def validate(self, data):
        user = self.context.get('request').user
        if not user.is_authenticated:
            raise ValidationError('Учетные данные не предоставлены!')

    def get_products(self, obj):
        return ShoppingCartItemProductSerializer(
            ShoppingCartItem.objects.filter(
                shopping_cart=obj,
            ),
            context=self.context,
            many=True
        ).data
