from celery import shared_task

from bubook.book.models import Book
from bubook.book.services import create_tag


@shared_task
def log(text):
    result = create_tag(text)
    print(f'{result} created')
    return result
