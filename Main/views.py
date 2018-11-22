from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "index.html")

def signup(request):
    user = User()
    error = False
    if request.POST:
        user.username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 != password2:
            return HttpResponseRedirect("/")
        user.password = password1
        user.email = request.POST.get("email")
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.save()

        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            error = True
    return render(request, "login_form.html", {
        "error": error
    })


def login(request):
    pass