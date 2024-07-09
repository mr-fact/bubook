from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from bubook.book.models import Tag, Category


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
