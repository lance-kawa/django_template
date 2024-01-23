
from django.db import models
from django.contrib.auth.models import AbstractUser
from .client import *

class User(AbstractUser):
    profil_picture = models.ImageField(upload_to='media/profil_pictures/', blank=True, null=True)