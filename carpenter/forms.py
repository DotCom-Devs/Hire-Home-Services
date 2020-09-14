from django import forms
from .models import CarpenterProfile
from accounts.models import City,Area
from django.core import validators
from django.contrib.auth.models import User

class UpdateUser(forms.ModelForm):
    first_name = forms.CharField(required = True)
    email = forms.EmailField(required = True)
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

def isphonenumber(value):
    if  value.isdigit()==False or len(value)!=10:
        raise forms.ValidationError('Invalid Phone Number')
def isamount(value):
    if value.isdigit()==False:
        raise forms.ValidationError('Invalid Amount')

class CarpenterProfileForm(forms.ModelForm):
    phone = forms.CharField(validators=[isphonenumber],required = True)
    charges = forms.CharField(validators=[isamount],required = True)
    class Meta:
        model = CarpenterProfile
        fields = ['phone','city','area','address','charges','profile_pic','timeopen','timeclose','is_avaliable']

        widgets = {
          'address': forms.Textarea(attrs={'rows':2, 'cols':15}),
        }

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



class carpenterFilter(forms.Form):
    city = forms.ModelChoiceField(label='City :',required=False,queryset=City.objects.all())
    area = forms.ModelChoiceField(label='Area :',required=False,queryset = Area.objects.all())
    sort_by = forms.ChoiceField(label='Sort By :',required=False)

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sort_by'].choices = [('none','----'),('inc','Price Low to High'),('dec','Price High to Low')]
        #self.fields['city'].choices = [('none','----')]+[(city.id,city.name) for city in City.objects.all()]
        #self.fields['area'].

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        if 'city' in self.data:
            try:
                city_id = (self.data.get('city'))
                if city_id!='':
                    city_id = int(city_id)
                    self.fields['area'].queryset = Area.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                print('error')
                raise forms.ValidationError('select valid options')
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        else:
            self.fields['area'].queryset = Area.objects.all()

    def clean(self):
        all_clean_data = super().clean()
        if all_clean_data['city']==None and all_clean_data['area']:
            raise forms.ValidationError('Select Valid City')
        elif all_clean_data['city']==None and all_clean_data['area']==None and all_clean_data['sort_by']=='none':
            raise forms.ValidationError('No options selected')
