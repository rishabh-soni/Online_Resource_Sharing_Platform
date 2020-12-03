from django.shortcuts import render, redirect
from django.http import *
from .models import *
from django.contrib import messages
from authen.models import *
from .forms import *
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Count


def product(request, myid):
    user = request.user
    pro = Products.objects.filter(id=myid)
    wish_list = Wishlist.objects.filter(username=user.username)
    ids = list()
    for item in wish_list:
        ids.append(item.pid)
        return render(request, 'item.html', {'product': pro, 'ids': ids})


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
    pro = Products.objects.filter(id__in=ids).filter(status=0)
    return render(request, 'wishlist.html', {'wishlist': wish_list, 'product': pro})


def yourads(request):
    user = request.user
    username = user.username
    pro = Products.objects.filter(seller=username)
    requests = Requests.objects.filter(seller=username)
    count = Requests.objects.values('pid').annotate(pcount=Count('pid'))
    prolist = list()
    for x in count:
        if x['pcount'] > 0:
            prolist.append(x['pid'])
    return render(request, 'yourads.html', {'product': pro, 'requests': requests, 'prolist': prolist})


def yourorders(request):
    user = request.user
    username = user.username
    orders = Transaction.objects.filter(buyer=username)
    ids = list()
    for x in orders:
        ids.append(x.pid)
    pro = Products.objects.filter(id__in=ids)
    return render(request, 'yourorders.html', {'product': pro})


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


def buy(request, category):
    user = request.user
    if category == "all":
        pro = Products.objects.all().filter(status=0)
    elif category == "books":
        pro = Products.objects.filter(category='Books/Notes').filter(status=0)
    elif category == "stationery":
        pro = Products.objects.filter(category='Stationery/Equipments').filter(status=0)
    elif category == "sports":
        pro = Products.objects.filter(category='Sports, Fitness and Outdoors').filter(status=0)
    elif category == "electronics":
        pro = Products.objects.filter(category='Electronics').filter(status=0)
    elif category == "household":
        pro = Products.objects.filter(category='Household').filter(status=0)
    elif category == "others":
        pro = Products.objects.filter(category='Others').filter(status=0)
    reco1 = Products.objects.order_by('-id').filter(status=0)[:3]
    reco2 = Products.objects.order_by('-id').filter(status=0)[3:6]
    wish_list = Wishlist.objects.filter(username=user.username)
    ids = list()
    for item in wish_list:
        ids.append(item.pid)
    return render(request, 'buy.html', {'products': pro, 'ids': ids, 'reco1': reco1, 'reco2': reco2})


def sendrequest(request, myid):
    user = request.user
    if user is not None:
        if user.is_active:
            pro = Products.objects.filter(id=myid).first()
            prodname = pro.name
            seller = pro.seller
            sellerinfo = CustomUser.objects.filter(username=seller).first()
            email = sellerinfo.email
            message = user.full_name + " has sent you a buy request for the product- " + prodname
            notif = "We have notified " + sellerinfo.full_name + " about your request for the product- " + prodname + " You can also contact him through his Phone Number: " + sellerinfo.phone_no
            send_mail("New buy request", message, 'honeycomb.iiti@gmail.com', [email])
            send_mail("Seller notified", notif, 'honeycomb.iiti@gmail.com', [user.email])
            requestp = Requests(pid=myid, buyer=user.username, seller=seller)
            requestp.save()
            return redirect('/buy/category/all')
            # return redirect('home')
        return redirect('login')


def confirm(request, pid):
    user = request.user
    if request.method == 'POST':
        seller = user.username
        buyer = request.POST['buyer']
        pro = Products.objects.filter(id=pid).first()
        pro.status = 1
        pro.save()
        transaction = Transaction(seller=seller, buyer=buyer, pid=pid, pname=pro.name)
        transaction.save()
        Requests.objects.filter(pid=pid).delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def search(request):
    user = request.user
    if request.method == 'POST':
        search = request.POST['search']
        result = list()
        words = search.split()
        for x in words:
            result += Products.objects.filter(name__icontains=x) | Products.objects.filter(
                description__icontains=x) | Products.objects.filter(category__icontains=x).filter(status=0)
        wish_list = Wishlist.objects.filter(username=user.username)
        ids = list()
        reco1 = Products.objects.order_by('-id').filter(status=0)[:3]
        reco2 = Products.objects.order_by('-id').filter(status=0)[3:6]
        for item in wish_list:
            ids.append(item.pid)
        return render(request, 'search.html',
                      {'products': result, 'ids': ids, 'reco1': reco1, 'reco2': reco2, 'search': search})
    return render(request, 'search.html')
