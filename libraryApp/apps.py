from django.apps import AppConfig


class LibraryappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'libraryApp'
    def ready(self):
        import libraryApp.signals  # Pastikan signals terdaftar
