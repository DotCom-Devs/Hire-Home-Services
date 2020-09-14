from django import forms
from .models import BasicProfile
from django.core import validators
from accounts.models import Area,City
from django.contrib.auth.models import User

class UpdateUser(forms.ModelForm):
    first_name = forms.CharField(required = True)
    email = forms.EmailField(required = True)
    class Meta:
        model = User
        fields = ['first_name','last_name','email']


def isphonenumber(value):
    if value.isdigit()==False or len(value)!=10:
        raise forms.ValidationError('Invalid Phone Number')


class BasicProfileForm(forms.ModelForm):
    phone = forms.CharField(validators=[isphonenumber],required = True)
    class Meta:
        model = BasicProfile
        fields = ['phone','city','area','address','profile_pic',]

        widgets = {
          'address': forms.Textarea(attrs={'rows':2, 'cols':15}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['area'].queryset = Area.objects.none()

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                print(city_id)
                self.fields['area'].queryset = Area.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['area'].queryset = self.instance.city.area_set.order_by('name')
