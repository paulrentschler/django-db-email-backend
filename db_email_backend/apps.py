from django.apps import AppConfig


class DbEmailBackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'db_email_backend'
    verbose_name = 'Email'
