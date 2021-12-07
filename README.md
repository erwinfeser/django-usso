# django-usso
Ugly single sign-on for django projects only.
Do you have many django apps with different users?
Do you want to use only one of those apps for authentication?
So I have an easy (and ugly) solution for you! I say it is ugly because it is using a direct DB connection and that is not the best approach, but it works great.

### Considerations:
- The users database is never written
- `last_login` value is updated in your current application instead of that one storing the users.
- Authenticated users are replicated locally with an unusable password
- `groups` are replicated too if you set `CLONE_GROUPS` as `True`. You can modify the permissions related to those groups locally and those will not be overrwritten.

## Installation:
1. Add `usso` to your `INSTALLED_APPS`
2. Define `AUTHENTICATION_BACKENDS` in `settings`:
```
AUTHENTICATION_BACKENDS = [
    'usso.authentication.UssoModelBackend',
]
```
3. Modify your `DATABASES` dictionary by adding a new connection for users. It has to be a connection to another django project database. We will use it as source of users and groups! For instance:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mydb',
        'USER': 'myuser',
        'HOST': 'myhost',
        'PORT': '5432',
        'PASSWORD': 'mypassword',
    },
    'users': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'users_db',
        'USER': 'users_user',
        'HOST': 'users_host',
        'PORT': '5432',
        'PASSWORD': 'users_password',
    },
}
```
4. Add `USSO_SETTINGS` to your `settings`:
```
USSO_SETTINGS = {
    'CLONE_GROUPS': True,  # It replicates external groups locally. Default True.
    'AUTH_USER_FIELD': 'username',  # It can be 'email' or 'username'. Default username.
    'USERS_DATABASE_NAME': 'users'  # The extra database name that you added to DATABASES
}
```
