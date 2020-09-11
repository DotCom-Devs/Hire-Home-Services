from django.urls import path
from .views import (createBasicProfile,updateBasicProfile,createOrUpdateProfile,
                    crateOrUpdateBasicProfile,viewProfile,homePageConsumers)
app_name = 'consumer'

urlpatterns =[
        path('',homePageConsumers,name='home'),
        path('up/',updateBasicProfile),
        path('cr/',createOrUpdateProfile,name='updateprofile'),
        path('cou/',crateOrUpdateBasicProfile),
        path('profile/',viewProfile,name='profile'),
]
