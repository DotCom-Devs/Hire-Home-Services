from django.urls import path
from .views import (createBasicProfile,updateBasicProfile,createOrUpdateProfile,
                    crateOrUpdateBasicProfile,viewProfile)
app_name = 'consumer'

urlpatterns =[
        path('',createBasicProfile,name='updateprofile'),
        path('up/',updateBasicProfile),
        path('cr/',createOrUpdateProfile,name='updateprofile'),
        path('cou/',crateOrUpdateBasicProfile),
        path('profile/',viewProfile,name='profile'),
]
