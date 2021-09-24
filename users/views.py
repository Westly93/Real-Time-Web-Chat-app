from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import UserRegistrationForm


class UserRegistrationView(View):
	def get(self, request, *args, **kwargs):
		form = UserRegistrationForm()
		context= {
			'form': form
		}
		return render(request, 'users/register.html', context)
	def post(self, request, *args, **kwargs):
		form= UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'You are successfully registered you can now lopgin')
			return redirect('login')
		return render(request, 'users/register.html', context)

