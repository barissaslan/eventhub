from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, Http404
from django.contrib.auth.decorators import login_required
from .forms import EventCreateForm, EventRegisterForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Event
from django.contrib import messages
from datetime import datetime, timedelta
from django.conf import settings
from notification.models import Notification


def home_view(request):
    return render(request, "home.html")


def event_index(request):
    event_list = Event.objects.active()
    events = pagination(request, event_list)
    return render(request, "event/index.html", {"events": events})


def event_index_user(request):
    events = Event.objects.filter(organizer=request.user)
    return render(request, "event/index.html", {"events": events})


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)

    notify = request.GET.get('notify')
    if notify and request.user == event.organizer:
        notification = Notification.objects.get(id=notify)
        notification.read = True
        notification.save()

    return render(request, "event/detail.html", {'event': event})


def event_create(request):
    organizer_name = request.user.get_full_name()
    start = (datetime.today() + timedelta(days=7)).replace(hour=13, minute=0)
    end = start + timedelta(hours=3)

    form = EventCreateForm(request.POST or None, request.FILES or None,
                           initial={
                                'organizer_name': organizer_name,
                                'start': start,
                                'end': end
                           })
    if form.is_valid():
        event = form.save(commit=False)
        event.organizer = request.user
        if 'draft' in request.POST:
            event.status = "draft"
        else:
            event.status = "live"
        event.save()
        messages.success(request, "Event successfully created.")

        return HttpResponseRedirect(event.get_absolute_url())

    context = {
        'form': form,
        'title': 'Create An Event',
        'primary': 'Create Event',
    }
    return render(request, 'event/event_create.html', context)


def event_update(request, slug):
    event = get_object_or_404(Event, slug=slug)

    if event.status == 'draft':
        primary = 'Make Live'
    else:
        primary = 'Update Event'

    if request.user != event.organizer:
        raise Http404

    form = EventCreateForm(request.POST or None, request.FILES or None, instance=event)
    if form.is_valid():
        event = form.save(commit=False)
        if 'draft' in request.POST:
            event.status = "draft"
        elif 'live' in request.POST:
            event.status = "live"
        else:
            return HttpResponseRedirect(event.get_absolute_url())
        event.save()

        messages.success(request, "Changes has been saved.")
        return HttpResponseRedirect(event.get_absolute_url())

    context = {
        'form': form,
        'title': 'Edit Event',
        'primary': primary,
        'status': event.status,
    }
    return render(request, "event/event_create.html", context)


def event_delete(request, slug):
    event = get_object_or_404(Event, slug=slug)
    event.delete()
    return redirect("event:user_index")


def event_register(request, slug):
    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format(settings.LOGIN_URL, request.path))

    attendee_name = request.user.first_name
    attendee_surname = request.user.last_name
    attendee_email = request.user.email

    form = EventRegisterForm(request.POST or None, request.FILES or None,
                                initial={
                                    'first_name': attendee_name,
                                    'last_name': attendee_surname,
                                    'email': attendee_email,
                                })
    if form.is_valid():
        # name = form.cleaned_data.get('first_name')
        # surname = form.cleaned_data.get('last_name')
        # email = form.cleaned_data.get('email')
        event = get_object_or_404(Event, slug=slug)
        request.user.registered_events.add(event)
        Notification.send(actor=event, receiver=event.organizer, message='Your event has a new attendee.')
        messages.success(request, "You have successfuly registered the event.")
        return HttpResponseRedirect(event.get_absolute_url())
    return render(request, "crispy/form.html", {"form": form, "title": "Register Event"})


def list_notifications(request):
    notifys = request.user.notifications.unread()
    return render(request, 'notifications/index.html', {'notifications': notifys})


def pagination(request, obj_list):
    query = request.GET.get('q')
    if query:
        if query.strip():
            obj_list = obj_list.filter(
                Q(title__icontains=query)
            ).distinct()

    paginator = Paginator(obj_list, 5)  # Show 5 posts per page

    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return objects
