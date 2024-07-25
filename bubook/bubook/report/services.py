from django.utils import timezone
from mongoengine import get_db

from bubook.post.models import Post
from bubook.users.models import BaseUser


def create_new_technical_report(user: BaseUser, tag: str, title: str, description: str):
    db = get_db()
    collection = db['technical_reports']
    document = collection.insert_one(
        {'user_id': user.id, 'tag': tag, 'title': title, 'description': description, 'created_at': timezone.now(),
         'status': 'created'})
    return document.inserted_id
