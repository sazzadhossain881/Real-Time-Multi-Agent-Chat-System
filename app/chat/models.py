from django.db import models
import uuid
from django.conf import settings
from user.models import User

# Create your models here.
class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    visitor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='visitor_sessions',
        on_delete=models.CASCADE
    )
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='agent_sessions',
        on_delete=models.SET_NULL,
        null=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

