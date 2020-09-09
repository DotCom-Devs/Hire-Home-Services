from django import forms
from .models import PlumberProfile
from accounts.models import City,Area
from django.core import validators

def isphonenumber(value):
    if  value.isdigit()==False or len(value)!=10:
        raise forms.ValidationError('Invalid Phone Number')
def isamount(value):
    if value.isdigit()==False:
        raise forms.ValidationError('Invalid Amount')

class PlumberProfileForm(forms.ModelForm):
    phone = forms.CharField(validators=[isphonenumber],required = True)
    charges = forms.CharField(validators=[isamount],required = True)
    class Meta:
        model = PlumberProfile
        fields = ['phone','city','area','address','charges','profile_pic','timeopen','timeclose','is_avaliable']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['area'].queryset = Area.objects.none()

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['area'].queryset = Area.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['area'].queryset = self.instance.city.area_set.order_by('name')
