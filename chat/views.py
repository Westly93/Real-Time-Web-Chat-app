from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chat, ChatRoom


class Index(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		return render(request, 'chat/index.html')

class Room(LoginRequiredMixin, View):
	def get(self, request, room_name, *args, **kwargs):
		chat_room= ChatRoom.objects.filter(room_name= room_name).first()
		chats= []
		if chat_room:
			chats= Chat.objects.filter(chat_room= chat_room)
		else:
			room= ChatRoom(room_name= room_name)
			room.save()

		context= {
			'room_name': room_name,
			'chats': chats
		}
		return render(request, 'chat/room.html', context)
