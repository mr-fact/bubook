from django.db import models
from bubook.common.models import BaseModel
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin

from bubook.users.validators import phone_validator


class BaseUserManager(BUM):
    def create_user(self, phone, email=None, is_active=True, is_admin=False, password=None):
        if not phone:
            raise ValueError("Users must have an phone number")

        user = self.model(phone=phone, email=self.normalize_email(email.lower()) if email else None,
                          is_active=is_active, is_admin=is_admin)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, email=None, password=None):
        user = self.create_user(
            phone=phone,
            email=email,
            is_active=True,
            is_admin=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(
        _("phone"),
        max_length=15,
        unique=True,
        help_text=_(
            "Phone number must be in the format +989*********."
        ),
        validators=[phone_validator],
        error_messages={
            "unique": _("A user with that phone already exists."),
        },
    )
    email = models.EmailField(_("email address"), blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = "phone"

    def __str__(self):
        return self.phone

    @property
    def is_staff(self):
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} >> {self.bio}"
