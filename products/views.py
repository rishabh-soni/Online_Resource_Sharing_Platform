from django.shortcuts import render, redirect
from django.http import *
from .models import Products


def product(request, myid):
    user = request.user
    pro = Products.objects.filter(id=myid)
    if user is not None:
        if user.is_active:
            return render(request, 'item.html', {'product': pro})
        return HttpResponseRedirect('login')