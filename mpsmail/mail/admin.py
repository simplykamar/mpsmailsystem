from django.contrib import admin
from mail.models import Inbox,Sentmail,Notification
# Register your models here.
admin.site.register(Inbox)
admin.site.register(Notification)
admin.site.register(Sentmail)