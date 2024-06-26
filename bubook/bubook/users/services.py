from django.db import transaction
from .models import BaseUser, Profile


def create_profile(*, user: BaseUser) -> Profile:
    return Profile.objects.create(user=user)


def create_user(*, phone: str, email: str, password: str) -> BaseUser:
    return BaseUser.objects.create_user(phone=phone, email=email, password=password)


@transaction.atomic
def register(*, phone: str, email: str, password: str) -> BaseUser:
    user = create_user(phone=phone, email=email, password=password)
    create_profile(user=user)
    return user
