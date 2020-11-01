from django.shortcuts import render, redirect
from django.http import *
from django.contrib.auth import authenticate, login
from products.models import Products
from .forms import *
from products.models import Wishlist
from django.core.mail import send_mail


def home(request):
    user = request.user
    pro = Products.objects.order_by('-id')[:8]
    wish_list = Wishlist.objects.filter(username=user.username)
    ids = list()
    for item in wish_list:
        ids.append(item.pid)
    if user is not None:
        if user.is_active:
            return render(request, 'auth/home.html', {'products': pro, 'ids': ids})
        return redirect('login')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', {'form': form})


def aboutus(request):
    user = request.user
    if user is not None:
        if user.is_active:
            return render(request, 'aboutus.html')
        return redirect('login')


def profile(request):
    user = request.user
    if user is not None:
        if user.is_active:
            return render(request, 'profile.html')
        return redirect('login')


def editprofile(request):
    user = request.user
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user.email = form.email
            user.save()
            return render(request, 'profile.html')
    return redirect('profile')


def contactus(request):
    user = request.user
    if user is not None:
        if user.is_active:
            if request.method == 'POST':
                form = ContactForm(request.POST)
                if form.is_valid():
                    name = form.cleaned_data.get("name")
                    email = form.cleaned_data.get("email")
                    message = form.cleaned_data.get("message")
                    subject = form.cleaned_data.get("subject")
                    message = name + " with the email, " + email + ", sent the following message:\n\n" + message
                    send_mail(subject, message, 'honeycomb.iiti@gmail.com', ['honeycomb.iiti@gmail.com'])
                    return redirect('contactus')
                else:
                    form = ContactForm()
                    return redirect('home')
            else:
                form = ContactForm()
                return render(request, 'contact-us.html', {'form': form})
        return redirect('login')

