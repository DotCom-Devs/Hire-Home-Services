from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


from .models import LastUpdated

def customer_profile(sender, instance, created, **kwargs):
	if created:
		LastUpdated.objects.create(
			user=instance,
			)
		print('Profile created!')

post_save.connect(customer_profile, sender=User)
