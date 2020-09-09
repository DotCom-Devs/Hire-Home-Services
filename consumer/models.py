from django.db import models
from django.contrib.auth.models import User
from accounts.models import City,Area
# Create your models here.
class BasicProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name = 'consumer')
    phone = models.BigIntegerField()

    #city = models.CharField(max_length=100)
    #area = models.CharField(max_length=100)
    #address = models.TextField(max_length=200)
    
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=False, null=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, blank=False, null=True)
    address = models.TextField(max_length=200, blank=False)

    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)


    def __str__(self):
        return self.user.username +' '+self.city
