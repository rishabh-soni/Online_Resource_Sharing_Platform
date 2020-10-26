from django.db import models

class Products(models.Model):
    name=models.CharField(max_length=255)
    description = models.CharField(max_length=2083)
    seller = models.CharField(max_length=255)
    price = models.FloatField()
    category = models.CharField(max_length=255)
    status = models.IntegerField()
    image_url = models.CharField(max_length=2083)

class Wishlist(models.Model):
    username = models.CharField(max_length=255)
    pid = models.IntegerField()
