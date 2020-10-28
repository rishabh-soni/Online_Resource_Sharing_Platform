from django.shortcuts import render, redirect
from django.http import *
from .models import Products
from .models import Wishlist
from django.contrib import messages


def product(request, myid):
    user = request.user
    pro = Products.objects.filter(id=myid)
    wish_list = Wishlist.objects.filter(username=user.username)
    ids = list()
    for item in wish_list:
        ids.append(item.pid)
    if user is not None:
        if user.is_active:
            return render(request, 'item.html', {'product': pro, 'ids': ids })
        return redirect('login')


def create_wishlist(request, pid):
    user = request.user
    username = user.username
    wishlisted = Wishlist.objects.filter(username=user.username).filter(pid=pid)
    if len(wishlisted) != 0:
        Wishlist.objects.filter(username=user.username).filter(pid=pid).delete()
    else:
        wish_list = Wishlist(username=username, pid=pid)
        wish_list.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def wishlist(request):
    user = request.user
    username = user.username
    wish_list = Wishlist.objects.filter(username=username)
    ids = list()
    for item in wish_list:
        ids.append(item.pid)
    pro = Products.objects.filter(id__in=ids)
    return render(request, 'wishlist.html', {'wishlist': wish_list, 'product': pro})


def sell(request):
    user = request.user
    if user is not None:
        if user.is_active:
            return render(request, 'sell.html')
        return redirect('login')
