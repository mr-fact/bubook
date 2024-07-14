from django.contrib import admin

from bubook.users.models import BaseUser, OtpRecord


@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    pass


@admin.register(OtpRecord)
class OtpRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'phone', 'code', )
