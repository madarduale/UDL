from django.contrib import admin
from .models import BaseUser, Profile
# Register your models here.

admin.site.register(BaseUser)
admin.site.register(Profile)