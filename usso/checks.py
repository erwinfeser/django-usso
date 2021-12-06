from django.conf import settings
from django.core.checks import Error, register, Tags


@register(Tags.database)
def usso_settings_check(app_configs, **kwargs):
    errors = []
    usso_settings = getattr(settings, 'USSO_SETTINGS')

    if not usso_settings:
        errors.append(
            Error(
                'USSO_SETTINGS not defined',
                hint='Please define USSO_SETTINGS in your settings.',
                obj=settings,
            )
        )

    if not isinstance(usso_settings, dict):
        errors.append(
            Error(
                'USSO_SETTINGS is not a dictionary',
                hint='Please define USSO_SETTINGS as a dictionary.',
                obj=settings,
            )
        )

    users_database_name = getattr(usso_settings, 'USERS_DATABASE_NAME')

    if not users_database_name:
        errors.append(
            Error(
                'USERS_DATABASE_NAME not defined in USSO_SETTINGS',
                hint='Please define USERS_DATABASE_NAME in USSO_SETTINGS variable.',
                obj=usso_settings,
            )
        )

    if not isinstance(users_database_name, str):
        errors.append(
            Error(
                'USERS_DATABASE_NAME is not a string',
                hint='Please define USERS_DATABASE_NAME as a valid string.',
                obj=usso_settings,
            )
        )

    databases = getattr(settings, 'DATABASES', {})

    if not databases.get(users_database_name):
        errors.append(
            Error(
                f'"{users_database_name}" not found in DATABASES settings',
                hint=f'Please add {users_database_name} to DATABASES settings.',
                obj=settings,
            )
        )

    return errors
