from django.conf import settings

DEFAULT_USSO_SETTINGS = {
    'CLONE_GROUPS': True,
    'AUTH_USER_FIELD': 'username',  # 'email' should work too
}

DEFAULT_USSO_SETTINGS.update(getattr(settings, 'USSO_SETTINGS', {}))

USSO_SETTINGS = DEFAULT_USSO_SETTINGS
