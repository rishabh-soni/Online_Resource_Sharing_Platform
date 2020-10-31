from django.shortcuts import render, redirect
from django.http import *
from .models import *
from django.contrib import messages
from .forms import *


def product(request, myid):
    user = request.user
    pro = Products.objects.filter(id=myid)
    wish_list = Wishlist.objects.filter(username=user.username)
    ids = list()
    for item in wish_list:
        ids.append(item.pid)
    if user is not None:
        if user.is_active:
            return render(request, 'item.html', {'product': pro, 'ids': ids})
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


def yourads(request):
    user = request.user
    username = user.username
    pro = Products.objects.filter(seller=username)
    return render(request, 'yourads.html', {'product': pro})


def deletead(request, pid):
    user = request.user
    username = user.username
    Products.objects.filter(id=pid).filter(seller=username).delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def editad(request, pid):
    user = request.user
    if request.method == 'POST':
        editform = Edit_Item(request.POST)
        if editform.is_valid():
            item = Products.objects.filter(id=pid).first()
            item.name = editform.cleaned_data.get('name')
            item.description = editform.cleaned_data.get('description')
            item.sell = editform.cleaned_data.get('sell')
            item.price = editform.cleaned_data.get('price')
            item.category = editform.cleaned_data.get('category')
            item.save()
    else:
        pro = Products.objects.filter(id=pid).values().first()
        editform = Edit_Item(initial=pro)
        return render(request, 'editad.html', {'form': editform})
    return redirect('yourads')


def sell(request):
    user = request.user
    if user is not None:
        if user.is_active:
            if request.method == 'POST':
                form = Item(request.POST, request.FILES)
                if form.is_valid():
                    item = form.save()
                    item.seller = user.username
                    item.save()
                    return redirect('sell')
            else:
                form = Item()
                return render(request, 'sell.html', {'form': form})

        return redirect('login')


def buy(request, category):
    user = request.user
    if category == "all":
        pro = Products.objects.all()
    elif category == "books":
        pro = Products.objects.filter(category='Books/Notes')
    elif category == "stationery":
        pro = Products.objects.filter(category='Stationery/Equipments')
    elif category == "cycle":
        pro = Products.objects.filter(category='Cycles')
    elif category == "others":
        pro = Products.objects.filter(category='Others')
    reco1 = Products.objects.order_by('-id')[:3]
    reco2 = Products.objects.order_by('-id')[3:6]
    wish_list = Wishlist.objects.filter(username=user.username)
    ids = list()
    for item in wish_list:
        ids.append(item.pid)
    return render(request, 'buy.html', {'products': pro, 'ids': ids, 'reco1': reco1, 'reco2': reco2})
