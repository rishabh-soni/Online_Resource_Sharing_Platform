from django.shortcuts import render
from django.http import HttpResponse


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')