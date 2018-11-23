import os

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from Main.models import Person
from webelopers import settings


def index(request):
    if request.user.groups.filter(name="استاد"):
        group = "استاد"
    else:
        group = "دانشجو"
    return render(request, "index.html", {
        "user": request.user,
        "group": group
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
            person = Person()
            person.user = user
            person.save()
            mygrp = Group.objects.get(name=request.POST.get("group", "استاد"))
            mygrp.user_set.add(user)
            return HttpResponseRedirect("/")

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


def contact(request):
    message = ""
    if request.POST:
        title = request.POST.get("title")
        text = request.POST.get("text")
        email = request.POST.get("email")
        # send_mail(subject=title, message=text, from_email=email, recipient_list=["ostadju@fastmail.com"])
        message = "درخواست شما ثبت شد"
    return render(request, "contactus.html", {
        "user": request.user,
        "message": message
    })


def profile(request):
    if request.user.groups.filter(name="استاد"):
        group = "استاد"
    else:
        group = "دانشجو"
    person = Person.objects.get(user=request.user)
    return render(request, "profile.html", {
        "user": request.user,
        "person": person,
        "group": group
    })


def editprofile(request):
    if request.POST:
        user = request.user
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.save()

        person = Person.objects.get(user=request.user)
        person.bio = request.POST.get("bio")
        person.gender = request.POST.get("gender")
        if request.FILES["picture"]:
            save_path = os.path.join(settings.STATIC_URL, 'pictures', request.FILES['picture'])
            path = default_storage.save(save_path, request.FILES['picture'])
            person.picture = default_storage.path(path)
        person.save()

        return HttpResponseRedirect("/profile")
    return render(request, "editprofile.html", {
        "user": request.user,
        "person": Person.objects.get(user=request.user),
    })
