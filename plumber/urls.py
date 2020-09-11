from django.urls import path
from .views import createOrUpdateProfile,viewProfile,hirePlumber,plumberHomePage,toggle
app_name = 'plumber'

urlpatterns = [
        path('updateprofile/',createOrUpdateProfile,name='updateprofile'),
        path('profile/<int:pk>',viewProfile,name='profile'),
        path('profile/',viewProfile,name='profile'),
        path('hireplumber/',hirePlumber,name='hirePlumber'),
        path('',plumberHomePage,name='home'),
        path('toggle/',toggle,name='toggle')
]
