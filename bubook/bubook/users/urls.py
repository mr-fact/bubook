from django.urls import path
from .apis import UserApi, RegisterApi, PasswordRecoveryApi, SendOtpApi

urlpatterns = [
    path('register/', RegisterApi.as_view(), name="register_api"),
    path('user/', UserApi.as_view(), name="user_api"),
    path('send-otp/', SendOtpApi.as_view(), name="send_otp_api"),
    path('password-recovery/', PasswordRecoveryApi.as_view(), name="password_recovery_api"),
]
