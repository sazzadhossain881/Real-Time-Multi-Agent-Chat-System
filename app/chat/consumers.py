import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from chat.models import ChatSession, Message
from chat.services import assign_agent


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope['user']
        print(self.user.email)
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

                self.send(json.dumps({
                    "type":"session_assigned",
                    "session_id": self.session_id
                }))

        elif self.user.role == 'agent':
            sessions = ChatSession.objects.filter(agent=self.user)
            for session in sessions:
                self.session_id = str(session.id)
                self.room_group_name = f"chat_{self.session_id}"

                async_to_sync(self.channel_layer.group_add)(
                    self.room_group_name,
                    self.channel_name
                )

        
    def receive(self, text_data):
        print(text_data)
        data = json.loads(text_data)
        message = data['message']

        session = ChatSession.objects.get(id=self.session_id)
        message = Message(session=session, sender=self.user, content=message)
        message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                "type": "chat_message",
                "message": message.content,
                "sender": self.user.username
            }
        )

    def chat_message(self, event):
        print(event)
        self.send(text_data=json.dumps(event))


        
        
