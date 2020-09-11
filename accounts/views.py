
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user
# Create your views here.
from .models import *
from .forms import CreateUserForm,UserTypeForm

from django.contrib.auth.models import Group

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get_or_create(name ='consumer')[0]
			user.groups.add(group)

			messages.success(request, 'Account was created for ' + username)

			return HttpResponseRedirect(reverse('accounts:user_login'))


	context = {'form':form}
	return render(request, 'accounts/register.html', context)

@unauthenticated_user
def serviceRegisterPage(request):

	form = CreateUserForm()
	type = UserTypeForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		type_form = UserTypeForm(request.POST)
		if form.is_valid() and type_form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			messages.success(request, 'Account was created for ' + username)
			service_type = type_form.cleaned_data['choice_field']
			print(service_type)

			group = Group.objects.get_or_create(name =service_type)[0]
			user.groups.add(group)
			return HttpResponseRedirect(reverse('accounts:user_login'))



	context = {'form':form,'typeservice':type}
	return render(request, 'accounts/serviceRegister.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			#if 'consumer' in (group.name for group in user.groups.all()):

			return redirect('accounts:index')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)


@login_required
def logoutUser(request):
	logout(request)
	return HttpResponseRedirect(reverse('accounts:user_login'))

def index(request):
    return render(request,'accounts/index.html')

@login_required
def updateProfile(request):

	if len(request.user.groups.all())!=0:

		if request.user.groups.all()[0].name=='consumer':
			return redirect('consumer:updateprofile')
		elif request.user.groups.all()[0].name == 'plumber':
			return redirect('plumber:updateprofile')
	else:
		return redirect('home')
