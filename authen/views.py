from django.shortcuts import render, redirect
from django.http import *
from django.contrib.auth import authenticate, login
from products.models import Products
from .forms import SignUpForm


def home(request):
    user = request.user
    pro = Products.objects.all()
    if user is not None:
        if user.is_active:
            return render(request, 'auth/home.html',{'products': pro})
        return HttpResponseRedirect('login')


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
