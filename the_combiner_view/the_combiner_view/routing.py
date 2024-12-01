from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from websocket_monitor.consumers import TokenConsumer
from trading.routing import websocket_urlpatterns as trading_websocket_urlpatterns

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            re_path(r'ws/tokens/$', TokenConsumer.as_asgi()),
        ] + trading_websocket_urlpatterns)
    ),
}) 