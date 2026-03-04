from django.urls import path
from chat import views

urlpatterns = [
    path("my-message/", views.MessagesAPIView.as_view(), name='my-messages'),
    path("my-message/<str:session_id>/", views.MessageRetrieveAPIView.as_view(), name='my-message')
]
