from django.db import models


class NotificationManager(models.Manager):
    def read(self):
        return self.filter(read=True)

    def unread(self):
        return self.filter(read=False)


class Notification(models.Model):
    actor = models.ForeignKey('event.Event')
    receiver = models.ForeignKey('accounts.User', related_name='notifications')

    message = models.CharField(max_length=256)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = NotificationManager()

    def __str__(self):
        return '{} - {}'.format(self.receiver.get_full_name(), self.message)

    @staticmethod
    def send(actor, receiver, message):
        obj = Notification.objects.create(actor=actor, receiver=receiver, message=message)
        return obj
