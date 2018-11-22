from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "index.html", {
        "user": request.user
    })


def signup(request):
    user_exists = False
    email_exists = False
    password_rematch = False
    if request.POST:
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        if User.objects.filter(username=username).exists():
            user_exists = True
        if User.objects.filter(email=email).exists():
            email_exists = True
        if password1 != password2:
            password_rematch = True

        if user_exists is False and password_rematch is False and email_exists is False:
            user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password1)
            return HttpResponseRedirect("/login")

    return render(request, "signup.html", {
        "user": request.user,
        "pass_rematch": password_rematch,
        "email_exists": email_exists,
        "user_exists": user_exists
    })


def login_(request):
    error = False
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")

    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            error = True
    return render(request, "login.html", {
        "error": error,
    })



def logout_(request):
    logout(request)
    return HttpResponseRedirect("/")

