from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from bubook.book.models import Tag, Category, Book


@receiver(post_save, sender=Tag)
def update_tag_cache(sender, instance, **kwargs):
    cache_keys = cache.keys('all_tasks_*')
    for key in cache_keys:
        cache.delete(key)


@receiver(post_save, sender=Category)
def update_category_cache(sender, instance, **kwargs):
    cache_keys = cache.keys('all_categories_*')
    for key in cache_keys:
        cache.delete(key)


@receiver(post_save, sender=Book)
def update_category_cache(sender, instance, **kwargs):
    if kwargs.get('created', False):
        instance.slug = slugify(instance.name)
        instance.save()
