from django import forms
from .models import *


class Products(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'description', 'price', 'category', 'Img1', 'Img2', 'Img3', 'sell']