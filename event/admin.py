from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "start", "end", "status"]
    list_filter = ["status", "capacity", "end"]
    search_fields = ["title", "description", "location"]
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ('Event Details', {'fields': ('organizer', 'title', 'location', 'start', 'end', 'description', 'image', 'status', 'slug')}),
        ('Create Tickets', {'fields': ('capacity',)}),
        ('Additional Settings', {'fields': ('event_type', 'event_topic')}),
        ('Attendees', {'fields': ('attendees',)})
    )

    class Meta:
        model = Event

admin.site.register(Event, EventAdmin)
