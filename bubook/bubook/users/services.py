from django.core.cache import cache
from django.db import transaction
from django.utils.timezone import now

from config.otp import OTP_LENGTH, OTP_EX_TIME, OTP_EX_CACHE
from .models import BaseUser, Profile
from .tasks import send_otp_message
from ..utils.random import random_int


def create_profile(*, user: BaseUser) -> Profile:
    return Profile.objects.create(user=user)


def create_user(*, phone: str, email: str, password: str) -> BaseUser:
    return BaseUser.objects.create_user(phone=phone, email=email, password=password)


@transaction.atomic
def register(*, phone: str, email: str, password: str) -> BaseUser:
    user = create_user(phone=phone, email=email, password=password)
    create_profile(user=user)
    return user


def create_new_otp(*, phone: str) -> None:
    available_valid_code = cache.get(f'valid_otp_{phone}')
    if available_valid_code:
        raise Exception('valid otp already exists')
    else:
        new_otp = random_int(OTP_LENGTH)
        cache.set(f'valid_otp_{phone}', f'{new_otp}:{0}', OTP_EX_TIME)
        cache.set(f'all_otp_{phone}_{new_otp}', now(), OTP_EX_CACHE)
        send_otp_message.delay(phone=phone, code=new_otp)


def validate_otp(*, phone: str, code: str) -> (bool, str):
    available_otp = cache.get(f'valid_otp_{phone}')
    if available_otp:
        available_code, trys = available_otp.split(':')
        if available_code == code:
            cache.delete(f'valid_otp_{phone}')
            return True, 'Success'
        else:
            trys = int(trys)
            if trys > 5:
                cache.delete(f'valid_otp_{phone}')
            else:
                cache.set(f'valid_otp_{phone}', f'{available_code}:{trys + 1}', OTP_EX_CACHE)
            return False, 'Wrong otp code'
    else:
        return False, 'Valid otp code not found'
