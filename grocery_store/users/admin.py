from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from grocery_store.settings import EMPTY_VALUE
from .models import User


@register(User)
class UserAdmin(UserAdmin):
    pass