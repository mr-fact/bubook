from django.urls import path
from .apis import UserApi, RegisterApi

urlpatterns = [
    path('register/', RegisterApi.as_view(), name="register_api"),
    path('user/', UserApi.as_view(), name="user_api"),
]
