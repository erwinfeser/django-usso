INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'usso',
)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
    'users': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}
SECRET_KEY = "secret_key_for_testing"
USSO_SETTINGS = {
    'CLONE_GROUPS': True,
    'AUTH_USER_FIELD': 'username',
    'USERS_DATABASE_NAME': 'users',
}
