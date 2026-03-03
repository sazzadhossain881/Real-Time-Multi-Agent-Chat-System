from django.contrib import admin
from chat.models import ChatSession, Message

# Register your models here.
@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['id']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id']
