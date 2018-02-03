from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from .choices import STATUSES, EVENT_TOPICS, EVENT_TYPES


def upload_location(instance, filename):
    return "event/{}/{}".format(instance.slug, filename)


class EventManager(models.Manager):
    def active(self):
        return self.filter(status='live').filter(end__gte=timezone.now())

    def draft(self):
        return self.filter(status='draft')

    def past(self):
        return self.filter(end__lte=timezone.now())


class Event(models.Model):

    organizer = models.ForeignKey('accounts.User', related_name='organizer_events')
    attendees = models.ManyToManyField('accounts.User', blank=True, related_name='registered_events')

    title = models.CharField(max_length=255, verbose_name="Event Title")
    location = models.CharField(max_length=200)
    online = models.BooleanField(default=False)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = RichTextField(null=True, blank=True)
    image = models.FileField(upload_to=upload_location, null=True, blank=True)
    capacity = models.IntegerField()
    organizer_name = models.CharField(max_length=250)

    event_type = models.CharField(max_length=200, choices=EVENT_TYPES, blank=True)
    event_topic = models.CharField(max_length=200, choices=EVENT_TOPICS, blank=True)

    status = models.CharField(max_length=10, choices=STATUSES)
    slug = models.SlugField(unique=True)

    objects = EventManager()

    def get_absolute_url(self):
        return reverse('event:detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ["end"]

    def __str__(self):
        return self.title + " - " + self.organizer_name


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug

    qs = Event.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "{}-{}".format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *arg, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Event)


# class TicketType(models.Model):
#     eb_id = models.CharField(max_length=255, unique=True, verbose_name='Eventbrite ID')
#     name = models.CharField(max_length=255)
#     description = models.TextField(null=True)
#     cost = MoneyField(max_digits=10, decimal_places=2, default_currency=DEFAULT_CURRENCY)
#     fee = MoneyField(max_digits=10, decimal_places=2, default_currency=DEFAULT_CURRENCY)
#     donation = models.BooleanField(default=False)
#     free = models.BooleanField(default=False)
#     event = models.ForeignKey('Event', related_name='tickets')
#     quantity_sold = models.IntegerField()
#
#     def __str__(self):
#         return self.name



