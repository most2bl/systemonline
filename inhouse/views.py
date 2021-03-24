from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
from .helpers import *
from random import randint
from datetime import datetime

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
# Persona information handling
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
        salary = request.POST["thesalaryy"]
        if not salary.isdigit():
            return render(request, "inhouse/newcase.html", {
                "message" : "برجاء إدخال ارقام فقط في خانة راتب  مقدم الطلب "
            }) 
        salary = int(request.POST["thesalaryy"])    
        degree = request.POST["thedegree"]

# Family information handling
        numOfForms = request.POST["formsnum"]
        isExist = Person.objects.filter(nationalId = nationalId)
        if not isExist:
            for i in range(int(numOfForms)):
                ftheName = request.POST[f"thename{i}[]"]
                if ftheName: 
                    ftheAge = request.POST[f"age{i}[]"]
                    frelationship = request.POST[f"relationship{i}[]"]
                    fsocialstate = request.POST[f"socialstate{i}[]"]
                    fhealthstate = request.POST[f"healthstate{i}[]"]
                    fdegree = request.POST[f"degree{i}[]"]
                    fjob = request.POST[f"job{i}"]
                    if not fjob:
                        fjob = "بدون وظيفة"
                    fsalary = request.POST[f"salary{i}"]
                    if not fsalary:
                        fsalary = 0
                    if not fsalary.isdigit() or not ftheAge.isdigit():
                        return render(request, "inhouse/newcase.html", {
                        "message" : "برجاء إدخال جميع بيانات العائلة بشكل صحيح"
                         }) 

# Title and case content handling
        cTitle = request.POST["title"]
        cContent = request.POST["subject"]
        if not cContent:
            return render(request, "inhouse/newcase.html", {
                        "message" : "برجاء إدخال تفاصيل المشكلة"
                         }) 
        uploadedfile = request.POST["uploadedfile"]
        while True:
            caseCode =  f"9{randint(1,999999)}"
            caseExist = Cases.objects.filter(caseCode = caseCode)
            if not caseExist:
                break
        caseStatus = "new"
        now = datetime.now()
        xZDate = now.strftime('%Y-%m-%d %H:%M:%S')
        current_user = request.user
#Insert into persona info
        if not isExist:
            theperson = Person.objects.create(socialState=socialState, healthState=healthState, age=age, nationalId=nationalId, personName=name, personPhoneNum=personPhoneNum, personAddress=personAddress,nationaldExpiryDate=nationaldExpiryDate, idDistrict=idDistrict, personJob=job,personSalary=salary, personEducationLevel=degree)
   
# Inserting into families info
        if not isExist:
            for i in range(int(numOfForms)):
                ftheName = request.POST[f"thename{i}[]"]
                if ftheName: 
                    ftheAge = int(request.POST[f"age{i}[]"])
                    frelationship = request.POST[f"relationship{i}[]"]
                    fsocialstate = request.POST[f"socialstate{i}[]"]
                    fhealthstate = request.POST[f"healthstate{i}[]"]
                    fdegree = request.POST[f"degree{i}[]"]
                    fjob = request.POST[f"job{i}"]
                    if not fjob:
                        fjob = "بدون وظيفة"
                    fsalary = request.POST[f"salary{i}"]
                    if not fsalary:
                        fsalary = 0
                    fthePerson = Families.objects.create(personaId=Person.objects.get(nationalId = nationalId), individualName=ftheName, individualAge=ftheAge, individualJob=fjob, individualHealthState=fhealthstate,individualSocialState=fsocialstate, individualEduLevel=fdegree, individualSalary=fsalary)
# Inserting into Cases
        if uploadedfile:
            cTheCase = Cases.objects.create(caseCode=caseCode,casePersonaId=Person.objects.get(nationalId = nationalId),caseScannedDocs=uploadedfile,caseTitle=cTitle,caseDetails=cContent,caseStatus=caseStatus,caseDate=xZDate, caseResponsible = User.objects.get(id = current_user.id))
        else:
            cTheCase = Cases.objects.create(caseCode=caseCode,casePersonaId=Person.objects.get(nationalId = nationalId),caseTitle=cTitle,caseDetails=cContent,caseStatus=caseStatus,caseDate=xZDate, caseResponsible = User.objects.get(id = current_user.id))
           
        
        return render(request, "inhouse/newcase.html", {
                "message" : f"تم إدخال البيانات بنجاح, كود متابعة الطلب هو {caseCode}"
            })     

def applyingjob(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "GET":    
        return render(request, "inhouse/jobs.html")
    else:
# Persona information handling
        name = request.POST["thename"]
        nationalId = request.POST["theid"]
        if not nationalId.isdigit():
            return render(request, "inhouse/jobs.html", {
                "message" : "برجاء إدخال رقم بطاقة صالح"
            })   
        age = getAge(int(request.POST["theid"]))
        socialState = request.POST["thesocialstate"]
        healthState = request.POST["thehealthstate"]
        personPhoneNum = request.POST["thephone"]
        if not personPhoneNum.isdigit():
            return render(request, "inhouse/jobs.html", {
                "message" : "برجاء إدخال رقم هاتف صالح"
            })    
        personAddress = request.POST["theaddress"]
        nationaldExpiryDate = request.POST["thedate"]
        idDistrict = request.POST["theplace"]
        job = request.POST["TheJob"]
        salary = request.POST["thesalaryy"]
        if not salary.isdigit():
            return render(request, "inhouse/jobs.html", {
                "message" : "برجاء إدخال ارقام فقط في خانة راتب  مقدم الطلب "
            }) 
        salary = int(request.POST["thesalaryy"])    
        degree = request.POST["thedegree"]            
# Family information handling
        numOfForms = request.POST["formsnum"]
        isExist = Person.objects.filter(nationalId = nationalId)
        if not isExist:
            for i in range(int(numOfForms)):
                ftheName = request.POST[f"thename{i}[]"]
                if ftheName: 
                    ftheAge = request.POST[f"age{i}[]"]
                    frelationship = request.POST[f"relationship{i}[]"]
                    fsocialstate = request.POST[f"socialstate{i}[]"]
                    fhealthstate = request.POST[f"healthstate{i}[]"]
                    fdegree = request.POST[f"degree{i}[]"]
                    fjob = request.POST[f"job{i}"]
                    if not fjob:
                        fjob = "بدون وظيفة"
                    fsalary = request.POST[f"salary{i}"]
                    if not fsalary:
                        fsalary = 0
                    if not fsalary.isdigit() or not ftheAge.isdigit():
                        return render(request, "inhouse/jobs.html", {
                        "message" : "برجاء إدخال جميع بيانات العائلة بشكل صحيح"
                         }) 
# Title and case content handling
        jUniversity = request.POST["university"]
        jDepartment = request.POST["department"]
        cContent = request.POST["subject"]
        if not cContent:
            return render(request, "inhouse/jobs.html", {
                        "message" : "برجاء إدخال تفاصيل المشكلة"
                         }) 
        uploadedfile = request.POST["uploadedfile"]
        while True:
            caseCode =  f"1{randint(1,999999)}"
            caseExist = Cases.objects.filter(caseCode = caseCode)
            if not caseExist:
                break
        caseStatus = "new"
        now = datetime.now()
        xZDate = now.strftime('%Y-%m-%d %H:%M:%S')
        current_user = request.user
#Insert into persona info
        if not isExist:
            theperson = Person.objects.create(socialState=socialState, healthState=healthState, age=age, nationalId=nationalId, personName=name, personPhoneNum=personPhoneNum, personAddress=personAddress,nationaldExpiryDate=nationaldExpiryDate, idDistrict=idDistrict, personJob=job,personSalary=salary, personEducationLevel=degree)

# Inserting into families info
        if not isExist:
            for i in range(int(numOfForms)):
                ftheName = request.POST[f"thename{i}[]"]
                if ftheName: 
                    ftheAge = int(request.POST[f"age{i}[]"])
                    frelationship = request.POST[f"relationship{i}[]"]
                    fsocialstate = request.POST[f"socialstate{i}[]"]
                    fhealthstate = request.POST[f"healthstate{i}[]"]
                    fdegree = request.POST[f"degree{i}[]"]
                    fjob = request.POST[f"job{i}"]
                    if not fjob:
                        fjob = "بدون وظيفة"
                    fsalary = request.POST[f"salary{i}"]
                    if not fsalary:
                        fsalary = 0
                    fthePerson = Families.objects.create(individualRole=frelationship,personaId=Person.objects.get(nationalId = nationalId), individualName=ftheName, individualAge=ftheAge, individualJob=fjob, individualHealthState=fhealthstate,individualSocialState=fsocialstate, individualEduLevel=fdegree, individualSalary=fsalary)
 # Inserting into Jobs
        if uploadedfile:
            cTheCase = Jobs.objects.create(jobCode=caseCode,jobPersonaId=Person.objects.get(nationalId = nationalId),jobCV=uploadedfile,jobUniversity=jUniversity,jobExtraDetails=cContent,jobStatus=caseStatus,jobDate=xZDate, JobResponsible = User.objects.get(id = current_user.id),jobEduMajor=jDepartment)
        else:
            cTheCase = Jobs.objects.create(jobCode=caseCode,jobPersonaId=Person.objects.get(nationalId = nationalId),jobUniversity=jUniversity,jobExtraDetails=cContent,jobStatus=caseStatus,jobDate=xZDate, JobResponsible = User.objects.get(id = current_user.id), jobEduMajor=jDepartment)
           
        
        return render(request, "inhouse/jobs.html", {
                "message" : f"تم تقديم طلب توظيف بنجاح, كود متابعة الطلب هو {caseCode}"
            })         

# Query function
def query(request):
# Make Sure the user logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
# If the page method is GET
    if request.method == "GET":    
        return render(request, "inhouse/search.html")
# If the page method is POST    
    else:
        nationalid = request.POST['nationalid']
# If the user serached by ID    
        if len(nationalid) == 14:
            isExist = Person.objects.filter(nationalId = nationalid)
            if isExist:
                isExist = Person.objects.get(nationalId = nationalid)
                return render(request, "inhouse/searched.html",{
                    "personInfo" : Person.objects.get(nationalId = nationalid),
                    "familiyInfo" : isExist.relatives.all(),
                    "cases": isExist.complain.all(),
                    "jobs": isExist.applicants.all(),
                })
            else:
                return render(request, "inhouse/search.html",{
                    "message" : "برجاء التأكد من الرقم المدخل"
                })

# If the user serached by PhoneNumber    
        elif len(nationalid) == 11:
            isExist = Person.objects.filter(personPhoneNum = nationalid)
            if isExist:
                isExist = Person.objects.get(personPhoneNum = nationalid)
                return render(request, "inhouse/searched.html",{
                    "personInfo" : Person.objects.get(personPhoneNum = nationalid),
                    "familiyInfo" : isExist.relatives.all(),
                    "cases": isExist.complain.all(),
                    "jobs": isExist.applicants.all(),
                })
            else:
                return render(request, "inhouse/search.html",{
                    "message" : "برجاء التأكد من الرقم المدخل"
                })              
