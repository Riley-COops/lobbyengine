import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolaTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from message.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lobbyengine.settings')

django_asgi_app = get_asgi_application()

application = ProtocolaTypeRouter({
    'http': django_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})