from django.db import models
from django import forms

CATEGORY_CHOICES = [
    ('Books/Notes', 'Books/Notes'),
    ('Household', 'Household'),
    ('Electronics', 'Electronics'),
    ('Stationery/Equipments', 'Stationery/Equipments'),
    ('Sports, Fitness and Outdoors', 'Sports, Fitness and Outdoors'),
    ('Others', 'Others'),
]


class Products(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2083)
    seller = models.CharField(max_length=255)
    price = models.FloatField()
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    status = models.IntegerField(default=0)
    sell = models.CharField(max_length=255, default='sell')
    Img1 = models.ImageField(upload_to='images/', default='images/no-image.jpg')
    Img2 = models.ImageField(upload_to='images/', default='images/no-image.jpg')
    Img3 = models.ImageField(upload_to='images/', default='images/no-image.jpg')


class Wishlist(models.Model):
    username = models.CharField(max_length=255)
    pid = models.IntegerField()
