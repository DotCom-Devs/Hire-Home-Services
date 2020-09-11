from django.db.models.signals import post_save
from .models import PlumberProfile
from django.utils import timezone

def profile_last_updated(sender, instance, created, **kwargs):

	t = instance.user.lastupdated
	t.update_date=timezone.now().date()
	t.save()
	print('Profile Updated!')

post_save.connect(profile_last_updated, sender=PlumberProfile)
