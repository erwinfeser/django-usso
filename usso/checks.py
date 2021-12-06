from django.conf import settings
from django.core.checks import Error, register, Tags
from usso.settings import USSO_SETTINGS


@register(Tags.database)
def authentication_backends_check(app_configs, **kwargs):
    errors = []
    authentication_backends = settings.AUTHENTICATION_BACKENDS

    if not authentication_backends:
        errors.append(
            Error(
                'AUTHENTICATION_BACKENDS is not defined',
                hint='Please define AUTHENTICATION_BACKENDS.',
                obj=settings,
            )
        )

    else:
        if not isinstance(authentication_backends, list):
            errors.append(
                Error(
                    'AUTHENTICATION_BACKENDS is not a list',
                    hint='Please define AUTHENTICATION_BACKENDS as a list.',
                    obj=settings,
                )
            )

        if len(authentication_backends) > 1:
            errors.append(
                Error(
                    'Only one backend is supported in AUTHENTICATION_BACKENDS if you use django-usso',
                    hint='Please define just one backend in AUTHENTICATION_BACKENDS.',
                    obj=settings,
                )
            )

        if authentication_backends[0] != 'usso.authentication.UssoModelBackend':
            errors.append(
                Error(
                    '"usso.authentication.UssoModelBackend" not found in AUTHENTICATION_BACKENDS',
                    hint='Please add "usso.authentication.UssoModelBackend" to AUTHENTICATION_BACKENDS.',
                    obj=settings,
                )
            )
    return errors


@register(Tags.database)
def usso_settings_check(app_configs, **kwargs):
    errors = []

    if not isinstance(USSO_SETTINGS, dict):
        errors.append(
            Error(
                'USSO_SETTINGS is not a dictionary',
                hint='Please define USSO_SETTINGS as a dictionary.',
                obj=settings,
            )
        )
    else:
        users_database_name = USSO_SETTINGS.get('USERS_DATABASE_NAME')
        if not users_database_name:
            errors.append(
                Error(
                    'USERS_DATABASE_NAME not defined in USSO_SETTINGS',
                    hint='Please define USERS_DATABASE_NAME in USSO_SETTINGS dictionary.',
                    obj=USSO_SETTINGS,
                )
            )
        else:
            if not isinstance(users_database_name, str):
                errors.append(
                    Error(
                        f'"{users_database_name}" is not a string',
                        hint='Please define USERS_DATABASE_NAME as a valid string.',
                        obj=users_database_name,
                    )
                )
            databases = getattr(settings, 'DATABASES', {})
            if not databases.get(users_database_name):
                errors.append(
                    Error(
                        f'"{users_database_name}" not found in DATABASES settings',
                        hint=f'Please add "{users_database_name}" to DATABASES settings.',
                        obj=settings,
                    )
                )
    return errors
