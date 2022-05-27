from re import T
from django.db import models

# Create your models here.
class SpofityToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=150)
    refresh_token= models.CharField(max_length=150)
    token_type = models.CharField(max_length=50)
    expires_in = models.DateTimeField()
