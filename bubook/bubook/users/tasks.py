from celery import shared_task
from django.core.cache import cache

from bubook.users.models import OtpRecord


@shared_task
def send_otp_message(phone: str, code: str):
    print(f'sms sent. [{phone}->{code}]')


@shared_task
def backup_otps_to_db_task():
    keys = cache.keys('all_otp_*')
    otp_records = []
    for key in keys:
        print(f'backup otp {key} to db')
        otp_records.append(
            OtpRecord(
                phone=key.split('_')[-2],
                code=key.split('_')[-1],
                created_at=cache.get(key)
            )
        )
        cache.delete(key)
    OtpRecord.objects.bulk_create(otp_records)
