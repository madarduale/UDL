
from django import template

register = template.Library()

@register.filter
def class_name(value):
    return value.__class__.__name__


@register.filter
def has_profile(user):
    return hasattr(user, 'profile')

@register.filter
def endswith(value, arg):
    return value.lower().endswith(arg.lower())


@register.filter
def first_line(value):
    return value.split('\n')[0] if value else ''