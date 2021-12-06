from django.apps import AppConfig


class UssoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usso'

    def ready(self):
        # Add System checks
        from .checks import usso_settings_check  # NOQA
