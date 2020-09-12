from django.apps import AppConfig


class ElectricianConfig(AppConfig):
    name = 'electrician'

    def ready(self):
    	import electrician.signals
