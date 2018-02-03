from django import template
from django.core import urlresolvers

register = template.Library()


@register.simple_tag
def active(request, pattern):
    if request.path == pattern:
        return 'active'
    return ''
