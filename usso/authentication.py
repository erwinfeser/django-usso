# pylint: disable=broad-except
import logging
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import check_password
from usso.settings import USSO_SETTINGS

LOGGER = logging.getLogger(__name__)
USERS_DATABASE_NAME = USSO_SETTINGS['USERS_DATABASE_NAME']
CLONE_GROUPS = USSO_SETTINGS['CLONE_GROUPS']
AUTH_USER_FIELD = USSO_SETTINGS['AUTH_USER_FIELD']
USER_MODEL = get_user_model()


class UssoModelBackend(ModelBackend):
    def update_user_data(self, user, remote_user):
        user.set_unusable_password()
        user.email = remote_user.email.lower()
        user.first_name = remote_user.first_name
        user.last_name = remote_user.last_name
        user.is_staff = remote_user.is_staff
        user.is_superuser = remote_user.is_superuser
        user.is_active = remote_user.is_active
        user.save()

    def clone_groups(self, user, remote_user):
        group_names = set(remote_user.groups.all().values_list('name', flat=True))
        already_created_group_names = set(Group.objects.filter(name__in=group_names).values_list('name', flat=True))
        for group_name in list(group_names.difference(already_created_group_names)):
            group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(*Group.objects.filter(name__in=group_names))

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username and password:
            remote_user = USER_MODEL.objects.using(USERS_DATABASE_NAME).filter(
                **{AUTH_USER_FIELD: username, 'is_active': True}
            ).first()
            if remote_user and check_password(password, remote_user.password):
                user, _ = USER_MODEL.objects.get_or_create(username=remote_user.username)
                self.update_user_data(user, remote_user)
                if CLONE_GROUPS:
                    self.clone_groups(user, remote_user)
                return user
