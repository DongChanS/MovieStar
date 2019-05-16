from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    nickname = models.CharField(max_length=40, blank=True)
    description = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(blank=True)