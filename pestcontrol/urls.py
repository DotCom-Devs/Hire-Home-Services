from django.urls import path
from .views import createOrUpdateProfile,viewProfile,hirePestcontrol,pestcontrolHomePage,toggle
app_name = 'pestcontrol'

urlpatterns = [
        path('updateprofile/',createOrUpdateProfile,name='updateprofile'),
        path('profile/<int:pk>',viewProfile,name='profile'),
        path('profile/',viewProfile,name='profile'),
        path('hirepestcontrol/',hirePestcontrol,name='hirePestcontrol'),
        path('',pestcontrolHomePage,name='home'),
        path('toggle/',toggle,name='toggle'),

]
