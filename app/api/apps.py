from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    default_site = "accounting.admin.MyAdminSite"
    name = 'api'

    def ready(self):
        import api.signals  # noqa