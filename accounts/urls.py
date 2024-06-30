
from django.urls import path, include
from .views import (
    UserSingUpView
)
urlpatterns = [
  path('signup/', UserSingUpView.as_view(), name='signup')
]
