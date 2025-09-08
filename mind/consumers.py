# mind/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message
from .utils.pseudonyms import anon_id, pseudonym_for

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        # Use the name with an underscore consistently
        self.room_group_name = f'chat_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data.get('message', '').strip()
        if not message_text:
            return

        user = self.scope["user"]
        if not user.is_authenticated:
            return

        user_anon_id = anon_id(user.id)
        user_pseudonym = pseudonym_for(user.id, "chat")

        room = await database_sync_to_async(Room.objects.get)(id=self.room_id)
        message = await database_sync_to_async(Message.objects.create)(
            room=room,
            pseudonym=user_pseudonym,
            anon_id=user_anon_id,
            text=message_text
        )

        # This sends the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message.text,
                'pseudonym': message.pseudonym,
                'created_at': message.created_at.strftime("%H:%M"),
                'anon_id': message.anon_id
            }
        )

    # This receives the message from the group and sends it to the client
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'pseudonym': event['pseudonym'],
            'created_at': event['created_at'],
            'anon_id': event['anon_id']
        }))