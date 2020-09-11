from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from accounts.models import Area, City

def load_cities(request):
    #print(request.GET.get('city_id'))
    city_id = request.GET.get('city_id')
    if city_id.isdigit()==False:
        return HttpResponse('<option value="">---------</option>')
    areas = Area.objects.filter(city_id=city_id).all()
    print(areas)
    return render(request, 'accounts/city_dropdown_list_options.html', {'areas': areas})
