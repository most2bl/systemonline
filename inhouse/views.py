from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
from .helpers import *
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
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "GET":    
        return render(request, "inhouse/newcase.html")
    else:
        # Persona information
        name = request.POST["thename"]
        nationalId = request.POST["theid"]
        if not nationalId.isdigit():
            return render(request, "inhouse/newcase.html", {
                "message" : "برجاء إدخال رقم بطاقة صالح"
            })   
        age = getAge(int(request.POST["theid"]))
        socialState = request.POST["thesocialstate"]
        healthState = request.POST["thehealthstate"]
        personPhoneNum = request.POST["thephone"]
        if not personPhoneNum.isdigit():
            return render(request, "inhouse/newcase.html", {
                "message" : "برجاء إدخال رقم هاتف صالح"
            })    
        personAddress = request.POST["theaddress"]
        nationaldExpiryDate = request.POST["thedate"]
        idDistrict = request.POST["theplace"]
        job = request.POST["TheJob"]
        salary = int(request.POST["thesalaryy"])
        if not salary.isdigit():
            return render(request, "inhouse/newcase.html", {
                "message" : "برجاء إدخال ارقام فقط في خانة راتب  مقدم الطلب "
            }) 
        degree = request.POST["thedegree"]
        #Insert into persona info
        theperson = Person.objects.create(socialState=socialState, healthState=healthState, age=age, nationalId=nationalId, personName=name, personPhoneNum=personPhoneNum, personAddress=personAddress,nationaldExpiryDate=nationaldExpiryDate, idDistrict=idDistrict, personJob=job,personSalary=salary, personEducationLevel=degree)
        return render(request, "inhouse/newcase.html", {
                "message" : "تم إدخال البيانات بنجاح"
            })        
    
