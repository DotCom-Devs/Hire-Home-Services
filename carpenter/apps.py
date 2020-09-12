from django.apps import AppConfig


class CarpenterConfig(AppConfig):
    name = 'carpenter'

    def ready(self):
    	import carpenter.signals
