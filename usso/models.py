from django.db import models
from django.contrib.auth import get_user_model

USER = get_user_model()


class Usso(models.Model):
    user = models.OneToOneField(USER, models.CASCADE, related_name='usso')
    external_id = models.IntegerField()
