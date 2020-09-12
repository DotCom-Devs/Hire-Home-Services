from django.shortcuts import render,redirect,get_object_or_404,reverse
from .models import BasicProfile
from .forms import BasicProfileForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from .decorators import allowed_users,check_profile_exist
# Create your views here.

#@unauthenticated_user

@login_required
@allowed_users(['consumer',],'updateprofile')
def createOrUpdateProfile(request):
    if request.user.lastupdated.update_date or BasicProfile.objects.filter(user=request.user).exists():
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
@check_profile_exist
@allowed_users(['consumer',],'profile')
def viewProfile(request):
    user_profile = request.user
    return render(request,'consumer/profiletemplate.html',{'user_profile':user_profile})

@login_required
@check_profile_exist
@allowed_users(['consumer',],'home')
def homePageConsumers(request):
    applist = ['plumber:hirePlumber','electrician:hireElectrician','carpenter:hireCarpenter',]
    return render(request,'consumer/consumer_home_page.html',{'services':applist})
