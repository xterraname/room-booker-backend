from django.db import models

from .managers import CustomManager


class CustomModel(models.Model):

    objects = CustomManager()

    class Meta:
        abstract = True


class CreatedModified(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
