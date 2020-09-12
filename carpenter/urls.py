from django.urls import path
from .views import createOrUpdateProfile,viewProfile,hireCarpenter,carpenterHomePage,toggle
app_name = 'carpenter'

urlpatterns = [
        path('updateprofile/',createOrUpdateProfile,name='updateprofile'),
        path('profile/<int:pk>',viewProfile,name='profile'),
        path('profile/',viewProfile,name='profile'),
        path('hirecarpenter/',hireCarpenter,name='hireCarpenter'),
        path('',carpenterHomePage,name='home'),
        path('toggle/',toggle,name='toggle'),

]
