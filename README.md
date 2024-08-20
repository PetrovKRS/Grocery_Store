
#  -- > API - Магазин продуктов < --
***

### Основные возможности проекта:
    
- добавление, удаление, редактирование категорий и подкатегорий товаров в админке.
- добавление, удаление, редактирование товаров через админку
- корзина пользователя создается автоматически при его создании
- добавление, удаление, редактирование товаров в корзине через админку
- автоматический подсчет количества различных товаров в корзине пользователя
  и подсчет общей их стоимости
- авторизация по токенам
- создание токена пользователя через админку
- возможность полной очистки корзины

### Эндпоинты API сервиса:
* (GET запрос) http://127.0.0.1:8000/api/categories/ - все категории с подкатегориями.
* (GET запрос) http://127.0.0.1:8000/api/products/ - все товары.
* (GET запрос) http://127.0.0.1:8000/api/shopping_cart/{shopping_cart_id} - все товары в корзине пользователя.
* (POST запрос) http://127.0.0.1:8000/api/shopping_cart/{shopping_cart_id}/shopping_cart_item/ - добавление товара в 
  корзину пользователя.
* (PATCH запрос) http://127.0.0.1:8000/api/shopping_cart/{shopping_cart_id}/shopping_cart_item/{id} - изменение кол-ва 
  товара в корзине пользователя.
* (DELETE запрос) http://127.0.0.1:8000/api/shopping_cart/{shopping_cart_id}/shopping_cart_item/{id}/ - полная 
  очистка корзины.
* (GET запрос) http://127.0.0.1:8000/users/ - работа с пользователями.
* (POST запрос) http://127.0.0.1:8000/api/auth/token/login/ - получение токена.

### Установка и запуск

#### Создание файла .env переменнх окружения
- клонировать проект
 ```shell
  git clone git@github.com:PetrovKRS/Grocery_Store.git
 ``` 
- Создайте в корне проекта .env файл и заполните его следующими данными 
  (см. env_example.txt):
 ```
  SECRET_KEY — секретный ключ для вашего проекта Django
  ALLOWED_HOSTS — доменные имена и ip-адреса, по которым будет доступен проект.
                  **Пример: ALLOWED_HOSTS=127.0.0.1,localhost,server_ip,domain_name**
  DEBUG - False, если хотите запустить сервис в контейнерах! True, если просто хотите 
            запустить API без фронтенда!
 ```
- перейдите в рабочую директорию проекта:
 ```shell
  cd Grocery_Store
 ```
- установите и активируйте виртуальное окружение:
 ```shell
  python3 -m venv venv
  source venv/bin/activat
 ```
- установите зависимости:
 ```shell
  pip install --upgrade pip
  pip install -r requirements.txt
 ```
- перейдите в папку grocery_store:
 ```shell
  cd grocery_store
 ```
- примените миграции:
 ```shell
  python3 manage.py migrate
 ```
- создайте суперпользователя:
 ```shell
  python3 manage.py createsuperuser
 ```
- запустите проект:
 ```shell
  python3 manage.py runserver
 ```
- создайте через админку как минимум одну категорию, одну подкатегорию, и несколько товаров.


### Документация к API:
* http://127.0.0.1:8000/redoc/

***
    
### <b> Стек технологий: </b>

![Python](https://img.shields.io/badge/-Python_3.9-df?style=for-the-badge&logo=Python&labelColor=yellow&color=blue)
![Django](https://img.shields.io/badge/-Django-df?style=for-the-badge&logo=Django&labelColor=darkgreen&color=blue)
![REST](https://img.shields.io/badge/-REST-df?style=for-the-badge&logo=Django&labelColor=darkgreen&color=blue)
![Postman](https://img.shields.io/badge/-Postman-df?style=for-the-badge&logo=Postman&labelColor=black&color=blue)
![GitHub](https://img.shields.io/badge/-GitHub-df?style=for-the-badge&logo=GitHub&labelColor=black&color=blue)
![Djoser](https://img.shields.io/badge/-Djoser-df?style=for-the-badge&logo=Djoser&labelColor=black&color=blue)
***
### Автор проекта: 
[![GitHub](https://img.shields.io/badge/-Андрей_Петров-df?style=for-the-badge&logo=GitHub&labelColor=black&color=blue)](https://github.com/PetrovKRS)
***
