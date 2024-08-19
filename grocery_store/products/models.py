from django.db import models
from django.db.models import Sum, F
from django.core.validators import RegexValidator
from django.db.models import IntegerField, DecimalField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from users.models import User


class Category(models.Model):
    """ Category model. """

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
        upload_to='products/category/',
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
    """ Subcategory model. """

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
        upload_to='products/category/subcategory/',
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
    """ Product model. """

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
        upload_to='products/category/subcategory/',
        blank=True,
        verbose_name='Изображение товара',
    )
    image_size_b = models.ImageField(
        upload_to='products/category/subcategory/',
        blank=True,
        verbose_name='Изображение товара',
    )
    image_size_c = models.ImageField(
        upload_to='products/category/subcategory/',
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
    """ Модель корзины. """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    total_count = models.IntegerField(
        default=0,
        verbose_name='Количество',
    )
    total_coast = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name='Цена за все',
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = (
            'id',
        )
        constraints = (
            models.UniqueConstraint(
                fields=('user',),
                name='unique_shopping_cart',
            ),
        )

    def __str__(self):
        return f'Корзина пользователя {self.user.username}'


class ShoppingCartItem(models.Model):
    """ Список товаров для корзины. """

    shopping_cart = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE,
        related_name='shopping_cart_items',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    count = IntegerField(
        verbose_name='Количество',
    )
    price = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        verbose_name='Цена',
    )

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
        ordering = (
            'id',
        )
        constraints = (
            models.UniqueConstraint(
                fields=('product', 'shopping_cart',),
                name='shopping_cart_unique_product',
            ),
        )

    def __str__(self):
        return (
            f'Корзина пользователя - '
            f'{self.shopping_cart.user.username}'
        )


@receiver(post_save, sender=User)
def create_shopping_cart(sender, **kwargs):
    """ Автоматическое создание корзины, при
        создании пользователя. """

    user = kwargs['instance']

    if not ShoppingCart.objects.filter(user=user).exists():
        shopping_cart = ShoppingCart.objects.create(user=user)
        shopping_cart.save()


@receiver([post_save, post_delete], sender=ShoppingCartItem)
def update_shopping_cart_total_price_count(sender, **kwargs):
    """ Автоматическое обновление общего количества
        товаров и их суммарной стоймости в корзине при
        изменении кол-ва. """

    shopping_cart_item = kwargs['instance']
    shopping_cart = ShoppingCart.objects.get(
        id=shopping_cart_item.shopping_cart.id
    )
    result = ShoppingCartItem.objects.filter(
        shopping_cart=shopping_cart
    ).aggregate(
        total_coast=Sum(F('price') * F('count')),
        total_count=Sum('count')
    )
    shopping_cart.total_coast = result['total_coast']
    shopping_cart.total_count = result['total_count']
    if not result['total_count'] and not result['total_coast']:
        shopping_cart.total_coast = 0
        shopping_cart.total_count = 0
    shopping_cart.save()
