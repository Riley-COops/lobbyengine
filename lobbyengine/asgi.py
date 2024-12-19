"""
ASGI config for lobbyengine project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolaTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lobbyengine.settings')

django_asgi_app = get_asgi_application()

application = ProtocolaTypeRouter({
    'http': django_asgi_app
})