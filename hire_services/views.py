from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import Area, City

def load_cities(request):
    city_id = request.GET.get('city_id')
    areas = Area.objects.filter(city_id=city_id).all()
    return render(request, 'accounts/city_dropdown_list_options.html', {'areas': areas})
