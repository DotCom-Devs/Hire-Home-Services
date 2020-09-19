# Hire-Home-Services
Web app that helps people to find handymen like plumber, electrician, etc in their nearby area based on their
availability.
- Hosted on [Hire Home services](https://hire-services-sj.herokuapp.com/ "Hire Home Services Home page")

## Software Requirements
- Python 3.6 or higher 

## Setup
clone repo
```bash
#setup the virtual environment
$ python3 -m venv hire-home-services
#activate virtual environment
$ source hire-home-services/bin/activate
#go to cloned repo
$ cd Hire-Home-Services
#install requirements
$ pip install -r requirements.txt
#create database (using SQLite by default)
$ python manage.py makemigrations
$ python manage.py migrate
#populate cities, areas and professions (important)
$ python populate_cities.py 
#populate fake service-providers like plumbers,carpenters etc.
#not mandatory 
$ python populate_data.py
# to run server
$ python manage.py runserver
```
Now go to http://127.0.0.1:8000/

## How to Use
### As normal user
- Register as User and fill details.
- Select any service you want (currently there are four services avaliable Plumber, Carpenter, Pest-control, Electrician)
- By default it will show list of handymans in your registered Area, City. 
- You can select any available cities from dropdown list and area to find list of available handyman and  see their complete Profile.

### As Service-Provider (Handyman)
- Register as Service and fill details.
- You can change your Availability Status by clicking toggle button.
