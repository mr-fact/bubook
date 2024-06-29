from django.urls import path

from bubook.book.apis import CategoryApi

urlpatterns = [
    path('category/', CategoryApi.as_view(), name="category_api"),
]
