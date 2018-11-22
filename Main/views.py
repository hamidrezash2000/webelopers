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
    user = User()
    error = False

    if request.POST:
        user_exists = False
        email_exists = False
        password_rematch = False
        user.username = request.POST.get("username")
        if User.objects.filter(username=user.username).exists():
            user_exists = True

        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 != password2:
            password_rematch = True
        user.password = password1
        user.email = request.POST.get("email")
        if User.objects.filter(password=user.email).exists():
            email_exists = True
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.save()

        if user is not None:
            login(request)
            return HttpResponseRedirect("/")
        else:
            error = True
    return render(request, "signup.html", {
        "user": request.user,
        "pass_rematch":password_rematch,
        "email_exists":email_exists,
        "user_exists":user_exists
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
        "user": request.user
    })



def logout_(request):
    logout(request)
    return HttpResponseRedirect("/")

