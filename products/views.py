from django.shortcuts import render, redirect
from django.http import *
from .models import Products
from .models import Wishlist

def product(request, myid):
    user = request.user
    pro = Products.objects.filter(id=myid)
    if user is not None:
        if user.is_active:
            return render(request, 'item.html', {'product': pro})
        return redirect('login')

def wishlist(request,pid):
        user = request.user
        username=user.username
        wish_list=Wishlist(username=username,pid=pid)
        wish_list.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





