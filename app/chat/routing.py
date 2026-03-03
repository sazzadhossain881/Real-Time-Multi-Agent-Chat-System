from django.urls import path
from chat.consumers import ChatConsumer


ASGI_urlpatterns = [
    path("ws/chat/", ChatConsumer.as_asgi())
]
