from django.db import models

class User(models.Model):
    uid = models.IntegerField()
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    photo = models.CharField(max_length=200)
    photo_big = models.CharField(max_length=200)