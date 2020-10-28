from django.db import models

class Products(models.Model):
    name=models.CharField(max_length=255)
    description = models.CharField(max_length=2083)
    seller = models.CharField(max_length=255)
    price = models.FloatField()
    category = models.CharField(max_length=255)
    status = models.IntegerField(default=0)
    sell = models.CharField(max_length=255, default='sell')
    image_url = models.CharField(max_length=2083)
    Img1 = models.ImageField(upload_to='images/', default='String')
    Img2 = models.ImageField(upload_to='images/', default='String')
    Img3 = models.ImageField(upload_to='images/', default='String')

class Wishlist(models.Model):
    username = models.CharField(max_length=255)
    pid = models.IntegerField()
