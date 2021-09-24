import json
from .models import ChatRoom, Chat
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name= self.scope['url_route']['kwargs']['room_name']
		self.room_group_name= 'chat_%s' % self.room_name 
		# join room group
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)
		await self.accept()

	async def disconnect(self, close_code):
		# Leave room group
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	#receive message from the websocket
	async def receive(self, text_data):
		self.user_id= self.scope['user'].id
		text_data_json= json.loads(text_data)
		message= text_data_json['message']

		# find the room object
		room= await database_sync_to_async(ChatRoom.objects.get)(room_name= self.room_name)

		# Create the chat object
		chat= Chat(
			content= message,
			user= self.scope['user'],
			chat_room= room
		)
		await database_sync_to_async(chat.save)()

		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'chat_message', 
				'message': message, 
				'user_id': self.user_id
			}
		)
	# Receive message from the room group
	async def chat_message(self, event):
		message= event['message']
		user_id= event['user_id']

		#send message to the websocket
		await self.send(text_data= json.dumps({
			'message': message,
			'user_id': user_id
		}))