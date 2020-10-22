from django.contrib import admin
from .models import Products

class ProductsAdmin(admin.ModelAdmin):
    list_display=('name', 'price')


admin.site.register(Products, ProductsAdmin)
