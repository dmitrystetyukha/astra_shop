from django.contrib.auth.models import *
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, null=True, blank=True)
