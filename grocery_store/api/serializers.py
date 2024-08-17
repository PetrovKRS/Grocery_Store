

# from djoser.serializers import UserCreateSerializer, UserSerializer
# from rest_framework import exceptions, serializers
#
# from users.models import User
#
#
# class CustomUserSerializer(UserSerializer):
#     """ Получение пользователя. """
#
#     class Meta:
#         model = User
#         fields = (
#             'id', 'username', 'email',
#         )
#
# class CustomUserCreateSerializer(UserCreateSerializer):
#     """ Создание пользователя. """
#
#     password = serializers.CharField(
#         max_length=150,
#         write_only=True,
#     )
#
#     class Meta:
#         model = User
#         fields = (
#             'id', 'username', 'email', 'password',
#         )
