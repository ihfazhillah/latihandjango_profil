from django.db import models
from django.core.exceptions import ValidationError

from .validators import (numeric_validation,)

# Create your models here.

TIPE_CHOICE = (
               ('p', 'primary'),
               ('s', 'secondary')
               )

class UserProfile(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)

    def __str__(self):
        return self.firstname

class Phone(models.Model):
    user = models.ForeignKey(UserProfile, 
                             related_name='phone')
    nomor = models.CharField(max_length=20,
                             validators=[numeric_validation])
    tipe = models.CharField(choices=TIPE_CHOICE, max_length=1,)

    def __str__(self):
        return self.nomor



class Website(models.Model):
    user = models.ForeignKey(UserProfile,
                             related_name='website')
    tipe = models.CharField(choices=TIPE_CHOICE,
                            max_length=1)
    url = models.URLField()

    def __str__(self):
        return self.url
