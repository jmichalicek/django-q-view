from django.apps import AppConfig


class DjangoQViewerConfig(AppConfig):
    name = 'django_q_view'
    verbose_name = "Django Q View"

    def ready(self):
        from django_q_view import signal_handlers  # noqa
