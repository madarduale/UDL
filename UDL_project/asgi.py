"""
ASGI config for UDL_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from your_app.routing import websocket_urlpatterns
import udl_app.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UDL_project.settings')

application = get_asgi_application()



application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            udl_app.routing.websocket_urlpatterns
        )
    ),
})