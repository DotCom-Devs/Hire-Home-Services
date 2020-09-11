from django.shortcuts import render,redirect,get_object_or_404
from .models import PlumberProfile
from .forms import PlumberProfileForm, plumberFilter
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from .decorators import allowed_users
from django.contrib.auth.models import User
# Create your views here.

#@unauthenticated_user

@login_required
@allowed_users(['plumber',])
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
            #lastUpdateEntry = request.user.lastupdated
            #lastUpdateEntry.update_date=timezone.now().date()
            #lastUpdateEntry.save()
            return  HttpResponseRedirect(reverse('home'))
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
            #lastUpdateEntry = request.user.lastupdated
            #lastUpdateEntry.update_date=timezone.now().date()
            #lastUpdateEntry.save()
            return  HttpResponseRedirect(reverse('home'))
    context = {'form':form}
    return render(request, 'plumber/updateprofile.html', context)


@login_required
def viewProfile(request,pk=None):
    if pk!=None:

        user_profile = get_object_or_404(User,pk=pk)
        if 'plumber' not in (group.name for group in user_profile.groups.all()):
            return HttpResponse('Not Exist')
    else:
        if 'plumber' not in (group.name for group in request.user.groups.all()):
            return HttpResponse('Not Exist')
        user_profile = request.user
    return render(request,'plumber/profiletemplate.html',{'user_profile':user_profile})



@login_required
def plumberHomePage(request):
    context={
        'plumber':request.user.plumber
    }
    return render(request,'plumber/plumber_home_page.html',context)

@login_required
@allowed_users(['plumber',])
def toggle(request):
    w = PlumberProfile.objects.get(id=request.POST['id'])
    print('hell    ',request.POST['isworking'])
    w.is_avaliable = request.POST['isworking'] == 'true'
    w.save()
    return HttpResponse('success')




@login_required
def hirePlumber(request):
    form = plumberFilter()
    if request.method=='POST':
        form = plumberFilter(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data['city'])


    user_data = request.user.consumer
    user_city = user_data.city
    user_area = user_data.area

    plumber_list = PlumberProfile.objects.filter(city=user_city).filter(is_avaliable=True)
    plumber_list_same_area = plumber_list.filter(area=user_area)
    plumber_list_diff_area = plumber_list.exclude(area=user_area)

    return render(request,'plumber/plumber_list.html',{'plumber_same_area':plumber_list_same_area,
                                                        'plumber_same_city':plumber_list_diff_area,
                                                        'user_city':user_city,
                                                        'user_area':user_area,
                                                        'form':form})
