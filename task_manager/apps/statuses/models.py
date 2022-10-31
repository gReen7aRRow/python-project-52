from django.db import models
from django.db.models import Model
from django.utils.translation import gettext


class Status(Model):
    name = models.CharField(
        max_length=100,
        verbose_name=gettext('StatusName'),
        unique=True,
    )

    def __str__(self):
        return self.name
