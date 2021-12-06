# pylint: disable=broad-except
import logging
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import check_password
from django.db import connections

from usso.settings import USSO_SETTINGS

LOGGER = logging.getLogger(__name__)

USERS_DATABASE_NAME = USSO_SETTINGS['USERS_DATABASE_NAME']
CLONE_GROUPS = USSO_SETTINGS['CLONE_GROUPS']
AUTH_USER_FIELD = USSO_SETTINGS['AUTH_USER_FIELD']

NAME = 0
USERNAME = 0
PASSWORD = 1
EMAIL = 2
FIRST_NAME = 3
LAST_NAME = 4
IS_ACTIVE = 5
EXTERNAL_ID = 6
IS_STAFF = 7
IS_SUPERUSER = 8

SELECT_USER_SQL = f'''
SELECT
auth_user.username,
auth_user.password,
auth_user.email,
auth_user.first_name,
auth_user.last_name,
auth_user.is_active,
auth_user.id,
auth_user.is_staff,
auth_user.is_superuser
FROM auth_user
WHERE UPPER(auth_user.{AUTH_USER_FIELD}::text) = UPPER(%s)
'''

SELECT_GROUPS_SQL = f'''
SELECT auth_group.name
FROM auth_user
LEFT OUTER JOIN auth_user_groups ON (auth_user.id = auth_user_groups.user_id)
LEFT OUTER JOIN auth_group ON (auth_user_groups.group_id = auth_group.id)
WHERE UPPER(auth_user.{AUTH_USER_FIELD}::text) = UPPER(%s)
'''

USER_MODEL = get_user_model()


def clone_groups(user, cursor):
    cursor.execute(SELECT_GROUPS_SQL, [getattr(user, AUTH_USER_FIELD)])
    group_names = [r[NAME] for r in cursor.fetchall()]
    for group_name in group_names:
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)


class UssoModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username and password:
            conn = connections[USERS_DATABASE_NAME]
            try:
                cursor = conn.cursor()
                cursor.execute(SELECT_USER_SQL, [username], )
                row = cursor.fetchone()
                if row and row[IS_ACTIVE] and check_password(password, row[PASSWORD]):
                    user, _ = USER_MODEL.objects.get_or_create(
                        username=row[USERNAME])
                    user.set_unusable_password()
                    email = row[EMAIL]
                    if email:
                        user.email = email.lower()
                    user.first_name = row[FIRST_NAME]
                    user.last_name = row[LAST_NAME]
                    user.is_staff = row[IS_STAFF]
                    user.is_superuser = row[IS_SUPERUSER]
                    user.is_active = True
                    user.save()
                    user.refresh_from_db()
                    user.usso.external_id = row[EXTERNAL_ID]
                    user.usso.save()
                    if CLONE_GROUPS:
                        clone_groups(user, cursor)
                    return user
            except Exception as exc:
                LOGGER.error(exc)

