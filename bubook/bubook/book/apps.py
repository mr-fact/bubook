from django.apps import AppConfig


class BookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bubook.book'

    def ready(self):
        import bubook.book.signals
