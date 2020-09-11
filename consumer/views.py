from django.shortcuts import render,redirect,get_object_or_404
from .models import BasicProfile
from .forms import BasicProfileForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from .decorators import allowed_users,allowed_usersprofile
# Create your views here.

#@unauthenticated_user

@login_required
@allowed_users(['consumer',])
def createOrUpdateProfile(request):
    if request.user.lastupdated.update_date:
        return updateBasicProfile(request)
    else:
        return createBasicProfile(request)

@login_required
def createBasicProfile(request):
    form = BasicProfileForm()
    if request.method == 'POST':
        form = BasicProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.user = request.user

            profile.save()
            #lastUpdateEntry = request.user.lastupdated
            #lastUpdateEntry.update_date=timezone.now().date()
            #lastUpdateEntry.save()
            return HttpResponseRedirect(reverse('home'))
    context = {'form':form}
    return render(request, 'consumer/register.html', context)

@login_required
def updateBasicProfile(request):
    obj = get_object_or_404(BasicProfile,user = request.user)
    form = BasicProfileForm(instance = obj)
    if request.method == 'POST':
        form = BasicProfileForm(request.POST,instance = obj)
        if form.is_valid():
            profile = form.save(commit=False)

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.user = request.user

            profile.save()
            #lastUpdateEntry = request.user.lastupdated
            #lastUpdateEntry.update_date=timezone.now().date()
            #lastUpdateEntry.save()
            return  HttpResponseRedirect(reverse('home'))
    context = {'form':form}
    return render(request, 'consumer/register.html', context)

@login_required
def crateOrUpdateBasicProfile(request):
    obj = BasicProfile.objects.get_or_create(user = request.user)[0]
    form = BasicProfileForm(instance = obj)
    if request.method == 'POST':
        form = BasicProfileForm(request.POST,instance = obj)
        if form.is_valid():
            profile = form.save(commit=False)

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.user = request.user

            profile.save()
            lastUpdateEntry = request.user.lastupdated
            lastUpdateEntry.update_date=timezone.now().date()
            lastUpdateEntry.save()
            return HttpResponseRedirect(reverse('home'))
    context = {'form':form}
    return render(request, 'consumer/register.html', context)

@login_required
@allowed_usersprofile(['consumer',])
def viewProfile(request):
    user_profile = request.user
    return render(request,'consumer/profiletemplate.html',{'user_profile':user_profile})

@login_required
@allowed_usersprofile(['consumer',])
def homePageConsumers(request):
    applist = ['plumber:home',]
    return render(request,'consumer/consumer_home_page.html',{'services':applist})
