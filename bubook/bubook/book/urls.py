from django.urls import path

from bubook.book.apis import CategoryApi, TagApi, BookApi, BookDetailApi, BookPublishApi

urlpatterns = [
    path('category/', CategoryApi.as_view(), name="category_api"),
    path('tag/', TagApi.as_view(), name="tag_api"),
    path('book/', BookApi.as_view(), name="book_api"),
    path('book/<str:book_slug>/', BookDetailApi.as_view(), name="book_detail_api"),
    path('book/<str:book_slug>/publish/', BookPublishApi.as_view(), name="book_publish_api"),
]
