from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home_redirect(request):
    return render(request, "frontend/items.html")

def signup(request):
    return render(request, "frontend/signup.html")

def login(request):
    return render(request, "frontend/login.html")

def items(request):
    return render(request, "frontend/items.html")

def reports(request):
    return render(request, "frontend/reports.html")
