from django.conf import settings


DEFAULT_USSO_SETTINGS = {
    'CLONE_GROUPS': True,
    'AUTH_USER_FIELD': 'username',  # 'email' should work too
}

USSO_SETTINGS = DEFAULT_USSO_SETTINGS.update(settings.USSO_SETTINGS)

AUTHENTICATION_BACKENDS = [
    'usso.authentication.UssoModelBackend',
]
