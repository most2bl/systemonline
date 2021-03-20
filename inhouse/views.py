from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
# Create your views here.

# The Index page
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "inhouse/index.html")

# Sign in function here
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "inhouse/login.html", {
                "message" : "تسجيل دخول غير مقبول, يرجى التحقق من اسم المستخدم وكلمة السر"
            })    
    return render(request, "inhouse/login.html")  

# logout function here
def logout_view(request):
    logout(request)
    return render(request, "inhouse/login.html")
    

# New case
def newcase(request):
    return render(request, "inhouse/newcase.html")
# Handling apply to a job url