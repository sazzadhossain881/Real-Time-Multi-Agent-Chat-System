import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from chat.models import ChatSession, Message
from chat.services import assign_agent
import time


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope['user']

        self.session_id = None
        self.room_group_name = None

        if not self.user.is_authenticated:
            self.close()
            return

        self.user.is_available = True
        self.user.save()

        self.accept()

        if self.user.role == 'visitor':

            session = assign_agent(self.user)

            if session:
                self.session_id = str(session.id)
                self.room_group_name = f"chat_{self.session_id}"

                async_to_sync(self.channel_layer.group_add)(
                    self.room_group_name,
                    self.channel_name
                )

                if session.agent:
                    async_to_sync(self.channel_layer.group_send)(
                        f"user_{session.agent.id}",
                        {
                            "type": "join_session",
                            "session_id": self.session_id,
                        }
                    )

                self.send(json.dumps({
                    "type": "session_assigned",
                    "session_id": self.session_id
                }))

        elif self.user.role == 'agent':

            async_to_sync(self.channel_layer.group_add)(
                f"user_{self.user.id}",
                self.channel_name
            )

            sessions = ChatSession.objects.filter(agent=self.user, is_active=True)

            for session in sessions:
                room_group_name = f"chat_{session.id}"

                async_to_sync(self.channel_layer.group_add)(
                    room_group_name,
                    self.channel_name
                )

                self.session_id = str(session.id)
                self.room_group_name = room_group_name


    def join_session(self, event):
        session_id = event["session_id"]
        room_group_name = f"chat_{session_id}"

        async_to_sync(self.channel_layer.group_add)(
            room_group_name,
            self.channel_name
        )

        self.session_id = session_id
        self.room_group_name = room_group_name

        pending_message = event.get("pending_message")
        if pending_message:
            async_to_sync(self.channel_layer.group_send)(
                room_group_name,
                {
                    "type": "chat_message",
                    "message": pending_message,
                    "sender": event.get("sender_username")
                }
            )


    def receive(self, text_data):
        if not self.user.is_authenticated:
            return

        data = json.loads(text_data)
        message_text = data.get("message")
        if not message_text:
            return

        try:
            session = ChatSession.objects.get(id=self.session_id, is_active=True)
        except ChatSession.DoesNotExist:
            return

        if self.user.role == 'visitor':
            agent = session.agent

            if not agent or not agent.is_available:
                new_session = assign_agent(self.user)
                if new_session and new_session.agent:
                    session.agent = new_session.agent
                    session.save()
                    agent = new_session.agent

                    async_to_sync(self.channel_layer.group_send)(
                        f"user_{agent.id}",
                        {
                            "type": "join_session",
                            "session_id": str(session.id),
                            "pending_message": message_text,
                            "sender_username": self.user.username
                        }
                    )
                    return

        Message.objects.create(
            session=session,
            sender=self.user,
            content=message_text
        )

        async_to_sync(self.channel_layer.group_send)(
            f"chat_{session.id}",
            {
                "type": "chat_message",
                "message": message_text,
                "sender": self.user.username
            }
        )
    
    def chat_message(self, event):
        self.send(text_data=json.dumps(event))


    def disconnect(self, code):

        if not self.user.is_authenticated:
            return

        self.user.is_available = False
        self.user.save()

        if self.room_group_name:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )

        async_to_sync(self.channel_layer.group_discard)(
            f"user_{self.user.id}",
            self.channel_name
        )
