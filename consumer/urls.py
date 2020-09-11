from django.urls import path
from .views import (createBasicProfile,updateBasicProfile,createOrUpdateProfile,
                    viewProfile,homePageConsumers)
app_name = 'consumer'

urlpatterns =[
        path('',homePageConsumers,name='home'),

        path('updateprofile/',createOrUpdateProfile,name='updateprofile'),

        path('profile/',viewProfile,name='profile'),
]
