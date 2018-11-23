import os
from itertools import chain

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework import serializers

from Main.models import Person
from webelopers import settings


def index(request):
    usersSearched = []
    if request.user.groups.filter(name="استاد"):
        group = "استاد"
    else:
        group = "دانشجو"

    if request.GET:
        usersSearched = User.objects.filter(username__contains=request.GET.get("search"), groups__name__icontains="استاد")
        usersSearched |= User.objects.filter(first_name__contains=request.GET.get("search"), groups__name__icontains="استاد")
        usersSearched |= User.objects.filter(last_name__contains=request.GET.get("search"), groups__name__icontains="استاد")
        # list(set(chain(usersSearched1, usersSearched2, usersSearched3)))
        if request.GET.get("search") == '':
            usersSearched = []
    return render(request, "index.html", {
        "user": request.user,
        "group": group,
        "usersSearched": usersSearched
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

            login(request, user)
            return HttpResponseRedirect("/")

    return render(request, "signup.html", {
        "user": request.user,
        "pass_rematch": password_rematch,
        "email_exists": email_exists,
        "user_exists": user_exists
    })


def login_(request):
    error = False
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect("/")

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


def profile(request, username=""):
    if username == "":
        username = request.user.username
    user = User.objects.filter(username=username)[0]
    if request.user.groups.filter(name="استاد"):
        group = "استاد"
    else:
        group = "دانشجو"
    person = Person.objects.get(user=user)
    return render(request, "profile.html", {
        "user": user,
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

        person.picture = request.FILES.get("picture")
        print(request.FILES)
        person.save()

        return HttpResponseRedirect("/profile")
    return render(request, "editprofile.html", {
        "user": request.user,
        "person": Person.objects.get(user=request.user),
    })

def setmeeting():
    pass


def removeuser(request):
    request.user.delete()
    return HttpResponseRedirect("/login")


class TeacherView(object):
    def __init__(self, username, fn, ln):
        self.first_name = fn
        self.last_name = ln
        self.profile_url = "/profile/" + username


class TeacherViewSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    profile_url = serializers.CharField(max_length=256)
    # def __init__(self, username, fn, ln):
    #     self.first_name = fn
    #     self.last_name = ln
    #     self.profile_url = "/profile/" + username


def json_query(request):
    q = request.GET.get("query")
    usersSearched1 = User.objects.filter(username__contains=q, groups__name__icontains="استاد")
    usersSearched2 = User.objects.filter(first_name__contains=q, groups__name__icontains="استاد")
    usersSearched3 = User.objects.filter(last_name__contains=q, groups__name__icontains="استاد")
    usersSearched = list(set(chain(usersSearched1, usersSearched2, usersSearched3)))
    if request.GET.get("query") == '':
        usersSearched = []
    resultList = []
    for teacher in usersSearched:
        resultList.append(TeacherView(teacher.username, teacher.first_name, teacher.last_name))
    serializer = TeacherViewSerializer(resultList)
    return HttpResponse(serializer.data)
    return JsonResponse(resultList, safe=False)
