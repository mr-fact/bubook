from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

import re

from config.otp import OTP_LENGTH


def number_validator(password):
    regex = re.compile('[0-9]')
    if regex.search(password) is None:
        raise ValidationError(
            _("password must include number"),
            code="password_must_include_number"
        )


def letter_validator(password):
    regex = re.compile('[a-zA-Z]')
    if regex.search(password) is None:
        raise ValidationError(
            _("password must include letter"),
            code="password_must_include_letter"
        )


def special_char_validator(password):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(password) is None:
        raise ValidationError(
            _("password must include special char"),
            code="password_must_include_special_char"
        )


def phone_validator(phone_number):
    regex = re.compile(r'^\+989\d{9}$')
    if not regex.match(phone_number):
        raise ValidationError(
            _("Phone number must be in the format +989*********"),
            code="invalid_phone_number"
        )


def otp_code_validator(otp_code):
    regex = re.compile(r'^\d{4}$')
    if not regex.match(otp_code):
        raise ValidationError(
            _("otp code must be in the format 1111")
        )
