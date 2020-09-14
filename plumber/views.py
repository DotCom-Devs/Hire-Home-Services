from django.shortcuts import render,redirect,get_object_or_404,reverse
from .models import PlumberProfile
from .forms import PlumberProfileForm, plumberFilter, UpdateUser
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from .decorators import allowed_users,check_profile_exist
from django.contrib.auth.models import User
# Create your views here.

#@unauthenticated_user

@login_required
@allowed_users(['plumber',],'updateprofile')
def createOrUpdateProfile(request):
    if request.user.lastupdated.update_date or PlumberProfile.objects.filter(user=request.user).exists():
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
    userobj = get_object_or_404(User,pk = request.user.pk)
    userform = UpdateUser(instance = userobj)
    if request.method == 'POST':
        form = PlumberProfileForm(request.POST,instance = obj)
        userform = UpdateUser(request.POST,instance = userobj)
        if form.is_valid() and userform.is_valid():
            profile = form.save(commit=False)
            userform.save()
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.user = request.user

            profile.save()
            #lastUpdateEntry = request.user.lastupdated
            #lastUpdateEntry.update_date=timezone.now().date()
            #lastUpdateEntry.save()
            return  HttpResponseRedirect(reverse('home'))
    context = {'form':form,'userform':userform}
    return render(request, 'plumber/updateprofile.html', context)


@login_required
@check_profile_exist
def viewProfile(request,pk=None):
    user_groups = list(group.name for group in request.user.groups.all()) #groups name for requesting user
    if pk!=None:
        if 'consumer' not in user_groups:
            return redirect( user_groups[0]+':profile')
        user_profile = get_object_or_404(User,pk=pk)
        if 'plumber' not in (group.name for group in user_profile.groups.all()): #groups name for pk user
            return render(request,'unauthorised_access.html',{'message':'Not Exist'})
    else:
        if 'plumber' not in user_groups:
            return redirect( user_groups[0]+':profile')
        user_profile = request.user
    return render(request,'plumber/profiletemplate.html',{'user_profile':user_profile})



@login_required
@check_profile_exist
@allowed_users(['plumber'],'home')
def plumberHomePage(request):
    context={
        'plumber':request.user.plumber
    }
    return render(request,'plumber/plumber_home_page.html',context)


@login_required
@allowed_users(['plumber',])
def toggle(request):
    if request.user.is_authenticated==False:
        return HttpResponse('Not Authorised')
    w = PlumberProfile.objects.get(id=request.POST['id'])
    print('hell    ',request.POST['isworking'])
    w.is_avaliable = request.POST['isworking'] == 'true'
    w.save()
    if w.is_avaliable:
        return HttpResponse('Status :  Avaliable')
    else:
        return HttpResponse('Status :  Not Avaliable')





@login_required
@check_profile_exist
@allowed_users(['consumer'])
def hirePlumber(request):
    form = plumberFilter()
    show_area = True
    orderfilter=False
    plumber_list_same_area = []
    plumber_list_diff_area = []
    plumber_list=[]
    user_city = ''
    user_area = ''
    if request.method=='POST':
        form = plumberFilter(data=request.POST)
        if form.is_valid():
            city=form.cleaned_data['city']
            area=form.cleaned_data['area']
            order=form.cleaned_data['sort_by']
            print(city,area,order)
            if order in ('inc','dec'):
                orderfilter=True
                if order=='inc':
                    order = 'charges'
                else:
                    order = '-charges'
            if area==None and city:
                show_area = False
                plumber_list = PlumberProfile.objects.filter(city=city).filter(is_avaliable=True)
                user_city = city.name
                if orderfilter:
                    plumber_list = plumber_list.order_by(order)
            elif area and city:
                plumber_list = PlumberProfile.objects.filter(city=city).filter(is_avaliable=True)
                plumber_list_same_area = plumber_list.filter(area=area)
                plumber_list_diff_area = plumber_list.exclude(area=area)
                user_city = city.name
                user_area = area.name
                if orderfilter:
                    plumber_list_same_area = plumber_list_same_area.order_by(order)
                    plumber_list_diff_area = plumber_list_diff_area.order_by(order)
            elif area==None and city==None and orderfilter:
                user_data = request.user.consumer
                user_city = user_data.city
                user_area = user_data.area

                plumber_list = PlumberProfile.objects.filter(city=user_city).filter(is_avaliable=True)
                plumber_list_same_area = plumber_list.filter(area=user_area)
                plumber_list_diff_area = plumber_list.exclude(area=user_area)

                if orderfilter:
                    plumber_list_same_area = plumber_list_same_area.order_by(order)
                    plumber_list_diff_area = plumber_list_diff_area.order_by(order)
        else:
            user_data = request.user.consumer
            user_city = user_data.city
            user_area = user_data.area

            plumber_list = PlumberProfile.objects.filter(city=user_city).filter(is_avaliable=True)
            plumber_list_same_area = plumber_list.filter(area=user_area)
            plumber_list_diff_area = plumber_list.exclude(area=user_area)


    else:

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
                                                        'form':form,
                                                        'show_area':show_area,
                                                        'plumber_list':plumber_list})
