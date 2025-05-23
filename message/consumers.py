# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async
# from .models import Message
# from django.contrib.auth import get_user_model

# User = get_user_model()



# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['user']
#         self.other_user_id = self.scope['urls_route']['kwargs']['user_id']
#         self.room_name = f"chat_{min(self.user.id, int(self.other_user_id))}_{max(self.user.id, int(self.other_user_id))}"
#         self.room_group_name = f"chat_{self.room_name}"

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']

#         await sync_to_async(Message.objects.create)(
#             sender=self.user,
#             receiver_id = int(self.other_user_id),
#             content = message
#         )

#         await self.channel_layer.group_send(
#             self.room_group_name,{
#                 'type':'chat_message',
#                 'message':message,
#                 'sender': self.user.username
#             }
#         )

#     async def chat_message(self, event):
#         message = event['message']
#         sender = event['sender']

#         await self.send(text_data=json.dumps({
#             'message':message,
#             'sender':sender
#         }))
    
