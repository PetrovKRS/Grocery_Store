from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.core.validators import RegexValidator

from users.models import User


class Category(models.Model):
    """ Модель категории. """

    name = models.CharField(
        max_length=150,
        db_index=True,
        verbose_name='Наименование',
        help_text='Наименование категории',
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        validators=(
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Недопустимые символы в идентификаторе!',
            ),
        ),
        verbose_name='Slug-имя',

    )
    image = models.ImageField(
        upload_to='media/products/category/',
        blank=True,
        verbose_name='Изображение товара',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = (
            'name',
        )

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    """ Модель подкатегории. """

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Категория',
    )
    name = models.CharField(
        max_length=150,
        db_index=True,
        verbose_name='Наименование',
        help_text='Наименование подкатегории',
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        validators=(
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Недопустимые символы в идентификаторе!',
            ),
        ),
        verbose_name='Slug-имя',

    )
    image = models.ImageField(
        upload_to='media/products/category/subcategory/',
        blank=True,
        verbose_name='Изображение товара',
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = (
            'name',
        )

    def __str__(self):
        return self.name


class Product(models.Model):
    """ Модель товара. """

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        verbose_name='Подкатегория',
    )
    name = models.CharField(
        max_length=150,
        db_index=True,
        verbose_name='Наименование',
        help_text='Наименование категории',
    )
    slug = models.SlugField(
        max_length=150,
        db_index=True,
        unique=True,
        validators=(
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Недопустимые символы в идентификаторе!',
            ),
        ),
        verbose_name='Slug-имя',

    )
    image_size_a = models.ImageField(
        upload_to='media/products/category/subcategory/',
        blank=True,
        verbose_name='Изображение товара',
    )
    image_size_b = models.ImageField(
        upload_to='media/products/category/subcategory/',
        blank=True,
        verbose_name='Изображение товара',
    )
    image_size_c = models.ImageField(
        upload_to=',=media/products/category/subcategory/',
        blank=True,
        verbose_name='Изображение товара',
    )
    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Цена',
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = (
            'name',
        )

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    """ Модель Корзины. """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Товар',
    )
    count = models.IntegerField()
    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Цена',
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'user',
                    'product'
                ),
                name='unique_shopping_cart_product'
            ),
        )

    def __str__(self):
        return f'{self.user} добавил {self.product}'