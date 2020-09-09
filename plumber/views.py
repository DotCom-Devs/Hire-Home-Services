from django.shortcuts import render,redirect,get_object_or_404
from .models import PlumberProfile
from .forms import PlumberProfileForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from .decorators import allowed_users
from django.contrib.auth.models import User
# Create your views here.

#@unauthenticated_user
@allowed_users(['plumber',])
@login_required
def createOrUpdateProfile(request):
    if request.user.lastupdated.update_date:
        return updateBasicProfile(request)
    else:
        return createBasicProfile(request)

@login_required
def createBasicProfile(request):
    form = PlumberProfileForm()
    if request.method == 'POST':
        form = PlumberProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.user = request.user

            profile.save()
            lastUpdateEntry = request.user.lastupdated
            lastUpdateEntry.update_date=timezone.now().date()
            lastUpdateEntry.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'plumber/updateprofile.html', context)

@login_required
def updateBasicProfile(request):
    obj = get_object_or_404(PlumberProfile,user = request.user)
    form = PlumberProfileForm(instance = obj)
    if request.method == 'POST':
        form = PlumberProfileForm(request.POST,instance = obj)
        if form.is_valid():
            profile = form.save(commit=False)

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.user = request.user

            profile.save()
            lastUpdateEntry = request.user.lastupdated
            lastUpdateEntry.update_date=timezone.now().date()
            lastUpdateEntry.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'plumber/updateprofile.html', context)


@login_required
def viewProfile(request,pk=None):
    if pk!=None:
        user_profile = get_object_or_404(User,pk=pk)
        if 'plumber' not in (group.name for group in user_profile.groups.all()):
            return HttpResponse('Not Exist')
    else:
        user_profile = request.user
    return render(request,'plumber/profiletemplate.html',{'user_profile':user_profile})
