from django.contrib import admin
from .models import HostList, Message

# Register your models here.
admin.site.register(HostList)

admin.site.register(Message)
