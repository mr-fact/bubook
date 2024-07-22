from mongoengine import QuerySet

from bubook.post.models import Post


def get_all_posts(**kwargs) -> QuerySet:
    return Post.objects.filter(**kwargs)


def get_published_posts(**kwargs) -> QuerySet:
    return Post.objects.filter(published=True, **kwargs)
