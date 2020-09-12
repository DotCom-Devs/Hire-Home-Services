"""hire_services URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from accounts.views import index
from django.conf import settings
from django.conf.urls.static import static


from .views import load_cities

urlpatterns = [
    path('',index,name='home'),
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('site/',include('consumer.urls')),
    path('plumber/',include('plumber.urls')),
    path('electrician/',include('electrician.urls')),
    path('carpenter/',include('carpenter.urls')),


    path('ajax/load-cities/', load_cities, name='ajax_load_cities'),
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
