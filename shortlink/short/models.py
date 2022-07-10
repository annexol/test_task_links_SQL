from django.contrib.auth.models import AbstractUser
from django.db import models
from autoslug import AutoSlugField


# Create your models here.

class User(AbstractUser):
    slug = AutoSlugField(populate_from='username', default='', unique=True)


class Links(models.Model):
    your_link = models.CharField(max_length=2000)
    new_link = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    user_name = models.ForeignKey('User', on_delete=models.PROTECT)

    class Meta:
        ordering = ['-date', 'user_name']
