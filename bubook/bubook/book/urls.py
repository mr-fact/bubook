from django.urls import path

from bubook.book.apis import CategoryApi, TagApi

urlpatterns = [
    path('category/', CategoryApi.as_view(), name="category_api"),
    path('tag/', TagApi.as_view(), name="tag_api"),
]
