from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms



class CreateUserForm(UserCreationForm):
	first_name = forms.CharField(required=True)
	email = forms.CharField(required=True)
	class Meta:
		model = User
		fields = ['first_name','last_name','username', 'email', 'password1', 'password2',]


class UserTypeForm(forms.Form):
	CHOICES = [('plumber', 'Plumber'), ('electrician', 'Electrician'),('carpenter','Carpenter')]
	choice_field = forms.ChoiceField(choices=CHOICES)
