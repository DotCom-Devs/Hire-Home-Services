import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','hire_services.settings')

import django
django.setup()

from accounts.models import City,Area
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from carpenter.models import CarpenterProfile
from electrician.models import ElectricianProfile
from plumber.models import PlumberProfile
from pestcontrol.models import PestcontrolProfile
from random import shuffle, seed
from faker.providers.person.en import Provider
from django.db import IntegrityError

import random
from faker import Faker
import random
fake = Faker()


def get_name():
    first_names = list(set(Provider.first_names))
    seed(4321)
    shuffle(first_names)
    for i in first_names:
        yield i

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)


def populate_service_person(service,city,area,username):
    first_name = username
    last_name = fake.last_name_male()
    email = fake.ascii_free_email()
    password = 'q1eer433'

    try:
        user = User.objects.create_user(first_name = first_name,last_name = last_name,
                                          username = username.lower(), email = email,
                                          password=password)
    except IntegrityError:
        print(username ,"user already exists.")
        return

    user.groups.add(service)
    user.save()

    phone = '912'+str(random_with_N_digits(7))
    address = fake.street_address()

    if service.name == 'plumber':
        charges = random.randint(200, 350)
        plumber_profile = PlumberProfile.objects.get_or_create(user=user,phone=phone,city=city,
                                                               area=area,address=address,
                                                               charges=charges)
    elif service.name == 'carpenter':
        charges = random.randint(250, 350)
        carpenter_profile = CarpenterProfile.objects.get_or_create(user=user,phone=phone,city=city,
                                                               area=area,address=address,
                                                               charges=charges)
    elif service.name == 'electrician':
        charges = random.randint(200, 300)
        electrician_profile = ElectricianProfile.objects.get_or_create(user=user,phone=phone,city=city,
                                                               area=area,address=address,
                                                               charges=charges)

    elif service.name == 'pestcontrol':
        charges = random.randint(200, 300)
        company = [first_name +' '+fake.company_suffix(),'']
        company = company[random.randint(0,1)]
        pestcontrol_profile = PestcontrolProfile.objects.get_or_create(user=user,company_name=company,phone=phone,city=city,
                                                               area=area,address=address,
                                                               charges=charges)

def populate_service_providers(fname,n=2):
    groups = Group.objects.exclude(name = 'consumer')
    for service in groups:
        print('start populating ',service.name)
        cities = City.objects.all()
        for city in cities:
            print('start populating ',service.name,city.name)
            areas = Area.objects.filter(city=city)
            for area in areas:
                for i in range(n):
                    populate_service_person(service,city,area,username = next(fname))
            print('success Populated ',service.name,city.name)
        print('success Populated ',service.name)


if __name__=="__main__":
    fname = get_name()
    print("Starting Populating...")
    populate_service_providers(fname=fname)
    print("SuccessFully Populated..............")
