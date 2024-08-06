import subprocess
import logging
import json
# from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
import asyncio

logger = logging.getLogger(__name__)

# class VideoCallConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.professor_id = self.scope['url_route']['kwargs']['professor_id']
#         self.room_group_name = f"video_call_{self.professor_id}"

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()
#         print(f"New connection in room: {self.room_group_name}")
#         logger.info(f"WebSocket connected for professor_id: {self.professor_id}")

#     async def disconnect(self, code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#         print(f"Connection closed in room: {self.room_group_name}")
#         logger.info(f"WebSocket disconnected for professor_id: {self.professor_id}")

#     async def receive(self, text_data=None, bytes_data=None):
#         data = json.loads(text_data)
#         print(f"Received data: {data}")

#         if 'type' in data:
#             if data['type'] == 'offer':
#                 await self.channel_layer.group_send(
#                     self.room_group_name,
#                     {
#                         'type': 'signaling_message',
#                         'data': data
#                     }
#                 )
#             elif data['type'] == 'answer':
#                 await self.channel_layer.group_send(
#                     self.room_group_name,
#                     {
#                         'type': 'signaling_message',
#                         'data': data
#                     }
#                 )
#             elif data['type'] == 'candidate':
#                 await self.channel_layer.group_send(
#                     self.room_group_name,
#                     {
#                         'type': 'signaling_message',
#                         'data': data
#                     }
#                 )
#             else:
#                 # Handle other message types (e.g., chat)
#                 pass

#         else:
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'video_data',
#                     'data': data 
#                 }
#             )

#     async def signaling_message(self, event):
#         await self.send(text_data=json.dumps(event['data']))

#     async def video_data(self, event):
#         video_data = event['data'] 

#         process = await asyncio.create_subprocess_exec(
#             'ffmpeg',
#             '-i', '-', 
#             '-c:v', 'libx264', 
#             '-c:a', 'aac', 
#             '-f', 'mpegts', 
#             '-',
#             stdout=subprocess.PIPE, 
#             stderr=subprocess.PIPE
#         )


#         while True:
#             data = await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'video_data',
#                     'data': None
#                 }
#             )

#             if data['data']:

#                 process.stdin.write(data['data'])

#             output = await process.stdout.read(1024) 
#             if output:
#                 await self.send(bytes_data=output)
            
#             await asyncio.sleep(0.01) 



class VideoCallConsumer(WebsocketConsumer):
    def connect(self):
        self.professor_id = self.scope['url_route']['kwargs']['professor_id']
        self.room_group_name = f"video_call_{self.professor_id}"

        # Join the room group
        self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave the room group
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type in ['offer', 'answer', 'candidate']:
            # Forward signaling data to the room group
            self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'forward_message',
                    'message': data
                }
            )
        elif message_type == 'join':
            # Handle student join and notify the teacher
            self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'student_join',
                    'message': data
                }
            )

    def forward_message(self, event):
        # Send signaling data to the client
        self.send(text_data=json.dumps(event['message']))

    def student_join(self, event):
        # Notify the teacher of a new student joining
        self.send(text_data=json.dumps(event['message']))