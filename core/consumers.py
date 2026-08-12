import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from .models import ChatConversation, ChatMessage


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]

        self.room_group_name = f"chat_{self.conversation_id}"

        self.user = self.scope["user"]

        # Don't allow unauthenticated users
        if self.user.is_anonymous:
            self.close()
            return

        # Get conversation
        try:
            self.conversation = ChatConversation.objects.get(
                id=self.conversation_id
            )
        except ChatConversation.DoesNotExist:
            self.close()
            return

        # Make sure the user belongs to this conversation
        if self.user not in [
            self.conversation.participant1,
            self.conversation.participant2
        ]:
            self.close()
            return

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        print(f"Connected to {self.room_group_name}")

    def disconnect(self, close_code):

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        print(f"Disconnected from {self.room_group_name}")

    def receive(self, text_data):
        
        data = json.loads(text_data)

        message = data.get("message", "").strip()

        if not message:
            return

        # Determine receiver
        if self.conversation.participant1 == self.user:
            receiver = self.conversation.participant2
        else:
            receiver = self.conversation.participant1

        # Save message to database
        chat_message = ChatMessage.objects.create(
            conversation=self.conversation,
            sender=self.user,
            receiver=receiver,
            message=message
        )

        # Update conversation
        self.conversation.last_message = message
        self.conversation.save()

        # Send message to everyone in this conversation
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": self.user.id,
                "sender_username": self.user.username,
                "created_at": chat_message.created_at.strftime("%H:%M"),
                "message_id": chat_message.id,
            }
        )

    def chat_message(self, event):

        self.send(text_data=json.dumps({
            "message": event["message"],
            "sender_id": event["sender_id"],
            "sender_username": event["sender_username"],
            "created_at": event["created_at"],
            "message_id": event["message_id"],
        }))