from celery import shared_task


@shared_task
def send_otp_message(phone: str, code: str):
    print(f'sms sent. [{phone}->{code}]')
