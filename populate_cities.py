import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','hire_services.settings')

import django
django.setup()

from accounts.models import City,Area
from django.contrib.auth.models import Group


cities ={}

cities['Delhi'] = ['Chanakya Puri','Delhi Cantonment',"Vasant Vihar","Model Town","Narela","Alipur",
        "Rohini","Khanjhawala","Saraswati Vihar","Patel Nagar","Rajouri Garden","Punjabi Bagh",
        "Dwarka",'Najafgarh','Kapashera','Saket','Hauz Khas','Mehrauli','Defence Colony',
        'Kalkaji','Sarita Vihar','Civil Lines','Kotwali','Karol Bagh','Seelam Pur',
        'Yamuna Vihar','Karawal Nagar','Shahdara','Seema Puri','Vivek Vihar','Gandhi Nagar',
        'Preet Vihar','Mayur Vihar']


cities['Mumbai'] = ['Andheri','Andheri East','Andheri West' ,'Anushakti Nagar' ,'Bhandup West' ,'Borivali' ,
          'Byculla', 'Chandivali' ,'Charkop ','Chembur ','Chinchpokli ','Colaba ','Dadar ',
          'Dahisar ','Dharavi ','Dindoshi ','Ghatkopar East ','Ghatkopar West ','Goregaon ',
          'Jogeshwari East','Kalina','Kandivali East' ,'Kurla' ,'Magathane' ,'Mahim' ,
          'Malabar Hill' ,'Malad West','Mankhurd Shivaji Nagar' ,'Mulund ','Mumbadevi ',
          'Opera House ','Parel ','Shivadi' ,'Sion Koliwada' ,'Vandre East ','Vandre West' ,
          'Versova' ,'Vikhroli ','Vile Parle ','Wadala ','Worli ',]


cities['Bangalore'] = ['Hoskote','Devanahalli','Doddaballapur','Nelamangala','Yelahanka','Krishnarajapuram',
             'Byatarayanapura','Yeshwantpur','Rajarajeshwarinagar','Dasarahalli','Mahalakshmi Layout',
             'Malleshwaram','Hebbal','Pulakeshinagar','Sarvagnanagar','C. V. Raman Nagar','Shivajinagar',
             'Shanti Nagar','Gandhi Nagar','Rajaji Nagar','Govindraj Nagar','Vijay Nagar','Chamrajpet',
             'Chickpet','Basavanagudi','Padmanabhanagar','B.T.M. Layout','Jayanagar','Mahadevapura',
             'Bommanahalli','Bangalore South','Anekal']

def populate_cities(cities):
    for city_name in cities:
        city = City.objects.get_or_create(name=city_name.strip())[0]
        city.save()
        for area_name in cities[city_name]:
            area = Area.objects.get_or_create(name=area_name.strip(),city=city)
            #area.city = city
            #area.save()
    print('success')

groups = ['plumber', 'electrician', 'carpenter', 'pestcontrol']

def populate_services(groups):
    for service_name in groups:
        service = Group.objects.get_or_create(name=service_name)[0]
    print('success')

if __name__=='__main__':
    print('populating services')
    populate_services(groups)
    print('successfully populated Groups(services)')

    print('populating Cities')
    populate_cities(cities)
    print('successfully populated Cities')
