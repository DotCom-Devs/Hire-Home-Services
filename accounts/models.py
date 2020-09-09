from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class LastUpdated(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name = 'lastupdated')
    update_date = models.DateField(auto_now=False,default = None,null=True,blank=True)

    def __str__(self):
        return self.user.username+' '+str(self.update_date)

class City(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Area(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name
