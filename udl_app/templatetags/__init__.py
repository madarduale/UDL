# templatetags/__init__.py

from django import template
from .class_name import register 
# from .custom_filters import register 

register = template.Library()


# Optionally, load other tags or filters here
