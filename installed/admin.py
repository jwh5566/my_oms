from django.contrib import admin

from .models import SystemInstall, InstallRecord

admin.site.register(SystemInstall)
admin.site.register(InstallRecord)
