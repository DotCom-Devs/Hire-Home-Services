from django.urls import path
from .views import registerPage,loginPage,logoutUser,index,serviceRegisterPage,updateProfile,profile

app_name = 'accounts'

urlpatterns = [
        path('',index,name='index'),
        path('login/',loginPage,name='user_login'),
        path('register/',registerPage,name='register'),
        path('logout/',logoutUser,name='logout'),
        path('registerservice/',serviceRegisterPage,name='registerservice'),
        path('updateprofile/',updateProfile,name='updateprofile'),
        path('profile/',profile,name='profile')
]
