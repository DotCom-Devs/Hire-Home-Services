from django.apps import AppConfig


class PestcontrolConfig(AppConfig):
    name = 'pestcontrol'

    def ready(self):
    	import pestcontrol.signals
