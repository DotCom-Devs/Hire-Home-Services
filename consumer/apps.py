from django.apps import AppConfig


class ConsumerConfig(AppConfig):
    name = 'consumer'

    def ready(self):
        import consumer.signals
