from django.urls import path
from .views import createOrUpdateProfile,viewProfile,hireElectrician,electricianHomePage,toggle
app_name = 'electrician'

urlpatterns = [
        path('updateprofile/',createOrUpdateProfile,name='updateprofile'),
        path('profile/<int:pk>',viewProfile,name='profile'),
        path('profile/',viewProfile,name='profile'),
        path('hireelectrician/',hireElectrician,name='hireElectrician'),
        path('',electricianHomePage,name='home'),
        path('toggle/',toggle,name='toggle'),

]
