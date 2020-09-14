from django.shortcuts import render,redirect,get_object_or_404,reverse
from .models import ElectricianProfile
from .forms import ElectricianProfileForm, electricianFilter, UpdateUser
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from .decorators import allowed_users,check_profile_exist
from django.contrib.auth.models import User
# Create your views here.

#@unauthenticated_user

@login_required
@allowed_users(['electrician',],'updateprofile')
def createOrUpdateProfile(request):
    if request.user.lastupdated.update_date or ElectricianProfile.objects.filter(user=request.user).exists():
        return updateBasicProfile(request)
    else:
        return createBasicProfile(request)

@login_required
def createBasicProfile(request):
    form = ElectricianProfileForm()
    if request.method == 'POST':
        form = ElectricianProfileForm(request.POST)
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
    return render(request, 'electrician/updateprofile.html', context)

@login_required
def updateBasicProfile(request):
    obj = get_object_or_404(ElectricianProfile,user = request.user)
    form = ElectricianProfileForm(instance = obj)
    userobj = get_object_or_404(User,pk = request.user.pk)
    userform = UpdateUser(instance = userobj)
    if request.method == 'POST':
        form = ElectricianProfileForm(request.POST,instance = obj)
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
    return render(request, 'electrician/updateprofile.html', context)


@login_required
@check_profile_exist
def viewProfile(request,pk=None):
    user_groups = list(group.name for group in request.user.groups.all()) #groups name for requesting user
    if pk!=None:
        if 'consumer' not in user_groups:
            return redirect( user_groups[0]+':profile')
        user_profile = get_object_or_404(User,pk=pk)
        if 'electrician' not in (group.name for group in user_profile.groups.all()): #groups name for pk user
            return render(request,'unauthorised_access.html',{'message':'Not Exist'})
    else:
        if 'electrician' not in user_groups:
            return redirect( user_groups[0]+':profile')
        user_profile = request.user
    return render(request,'electrician/profiletemplate.html',{'user_profile':user_profile})



@login_required
@check_profile_exist
@allowed_users(['electrician'],'home')
def electricianHomePage(request):
    context={
        'electrician':request.user.electrician
    }
    return render(request,'electrician/electrician_home_page.html',context)


@login_required
@allowed_users(['electrician',])
def toggle(request):
    if request.user.is_authenticated==False:
        return HttpResponse('Not Authorised')
    w = ElectricianProfile.objects.get(id=request.POST['id'])
    print('hell    ',request.POST['isworking'])
    w.is_avaliable = request.POST['isworking'] == 'true'
    w.save()
    if w.is_avaliable:
        return HttpResponse('Status :  Avaliable')
    else:
        return HttpResponse('Status :  Not Avaliable')





@login_required
@check_profile_exist
@allowed_users(['consumer',])
def hireElectrician(request):
    form = electricianFilter()
    show_area = True
    orderfilter=False
    electrician_list_same_area = []
    electrician_list_diff_area = []
    electrician_list=[]
    user_city = ''
    user_area = ''
    if request.method=='POST':
        form = electricianFilter(data=request.POST)
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
                electrician_list = ElectricianProfile.objects.filter(city=city).filter(is_avaliable=True)
                user_city = city.name
                if orderfilter:
                    electrician_list = electrician_list.order_by(order)
            elif area and city:
                electrician_list = ElectricianProfile.objects.filter(city=city).filter(is_avaliable=True)
                electrician_list_same_area = electrician_list.filter(area=area)
                #print(electrician_list,'ahsdfhjaksdfhkjdashfk',electrician_list_same_area)
                electrician_list_diff_area = electrician_list.exclude(area=area)
                user_city = city.name
                user_area = area.name
                if orderfilter:
                    electrician_list_same_area = electrician_list_same_area.order_by(order)
                    electrician_list_diff_area = electrician_list_diff_area.order_by(order)
            elif area==None and city==None and orderfilter:
                user_data = request.user.consumer
                user_city = user_data.city
                user_area = user_data.area

                electrician_list = ElectricianProfile.objects.filter(city=user_city).filter(is_avaliable=True)
                electrician_list_same_area = electrician_list.filter(area=user_area)
                electrician_list_diff_area = electrician_list.exclude(area=user_area)

                if orderfilter:
                    electrician_list_same_area = electrician_list_same_area.order_by(order)
                    electrician_list_diff_area = electrician_list_diff_area.order_by(order)
        else:
            user_data = request.user.consumer
            user_city = user_data.city
            user_area = user_data.area

            electrician_list = ElectricianProfile.objects.filter(city=user_city).filter(is_avaliable=True)
            electrician_list_same_area = electrician_list.filter(area=user_area)
            electrician_list_diff_area = electrician_list.exclude(area=user_area)


    else:

        user_data = request.user.consumer
        user_city = user_data.city
        user_area = user_data.area

        electrician_list = ElectricianProfile.objects.filter(city=user_city).filter(is_avaliable=True)
        electrician_list_same_area = electrician_list.filter(area=user_area)
        electrician_list_diff_area = electrician_list.exclude(area=user_area)

    return render(request,'electrician/electrician_list.html',{'electrician_same_area':electrician_list_same_area,
                                                        'electrician_same_city':electrician_list_diff_area,
                                                        'user_city':user_city,
                                                        'user_area':user_area,
                                                        'form':form,
                                                        'show_area':show_area,
                                                        'electrician_list':electrician_list})
