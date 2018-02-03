from django.conf.urls import url
from .views import *

app_name = 'accounts'

urlpatterns = [
    # /accounts/login
    url(r'^login/$', login_view, name='login'),

    # /accounts/logout
    url(r'^logout/$', logout_view, name='logout'),

    # /accounts/register
    url(r'^register/$', register_view, name='signup'),

    # /accounts/myprofile
    url(r'^myprofile/$', profile_view, name='profile'),
]

