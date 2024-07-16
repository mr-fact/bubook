from django.urls import path

from bubook.post.apis import PostApi

urlpatterns = [
    path('post/', PostApi.as_view(), name="post_api"),
]
