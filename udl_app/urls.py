
from django.urls import path
from .views import (
   home,
   jitsi_meet,
   send_message,
   inbox,
)

urlpatterns = [
   path('', home, name='home'),
   path('meet/',jitsi_meet, name='jitsi_meeting'),
   path('send/', send_message, name='send_message'),
   path('inbox/', inbox, name='inbox'),
]
