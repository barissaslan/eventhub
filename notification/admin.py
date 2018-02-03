from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ["receiver", "actor", "read", "timestamp"]

    class Meta:
        model = Notification

admin.site.register(Notification, NotificationAdmin)

