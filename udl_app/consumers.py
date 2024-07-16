# # consumers.py
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class VideoCallConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope["user"]
#         self.room_group_name = f'video_call_{self.user.id}'

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         professor_id = data.get('professor_id')
#         message = data.get('message')

#         if professor_id:
#             room_group_name = f'video_call_{professor_id}'
#             await self.channel_layer.group_send(
#                 room_group_name,
#                 {
#                     'type': 'video_call_message',
#                     'message': message
#                 }
#             )

#     async def video_call_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))


import json
from channels.generic.websocket import WebsocketConsumer

class VideoCallConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        professor_id = data.get('professor_id')
        message_type = data.get('type')

        if professor_id:
            self.send_to_professor(data)
        else:
            self.send_to_student(data)

    def send_to_student(self, data):
        # Logic to send signaling data to student
        self.send(text_data=json.dumps(data))

    def send_to_professor(self, data):
        # Logic to send signaling data to professor
        self.send(text_data=json.dumps(data))
