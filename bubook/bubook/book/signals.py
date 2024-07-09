from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from bubook.book.models import Tag


@receiver(post_save, sender=Tag)
def update_tag_cache(sender, instance, **kwargs):
    cache_keys = cache.keys('all_tasks_*')
    for key in cache_keys:
        cache.delete(key)
