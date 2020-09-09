from django.urls import path
from .views import createOrUpdateProfile,viewProfile
app_name = 'plumber'

urlpatterns = [
        path('updateprofile/',createOrUpdateProfile,name='updateprofile'),
        path('profile/<int:pk>',viewProfile,name='profile'),
        path('profile/',viewProfile,name='profile'),
]
