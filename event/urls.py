from django.conf.urls import url
from .views import *

app_name = "event"

urlpatterns = [

    url(r'^$', home_view, name='home'),

    # /events/
    url(r'^events/$', event_index, name='index'),

    # /myevents/
    url(r'^myevents/$', event_index_user, name='user_index'),

    # /notifications/
    url(r'^notifications/$', list_notifications, name='notification'),

    # /event/create/
    url(r'^event/create/$', event_create, name='add'),

    # /event/slug/
    url(r'^event/(?P<slug>[\w-]+)/$', event_detail, name='detail'),

    # /event/slug/edit/
    url(r'^event/(?P<slug>[\w-]+)/edit/$', event_update, name='edit'),

    # /event/slug/delete/
    url(r'^event/(?P<slug>[\w-]+)/delete/$', event_delete, name='delete'),

    # /event/slug/register
    url(r'^event/(?P<slug>[\w-]+)/register/$', event_register, name='register'),
]

