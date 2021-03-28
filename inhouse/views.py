from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
from .helpers import *
from random import randint
from datetime import datetime
from django.core.paginator import Paginator
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
        age = getAge(request.POST["theid"])
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
            caseCode =  f"9{randint(100000,999999)}"
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
        age = getAge(request.POST["theid"])
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
            caseCode =  f"1{randint(100000,999999)}"
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
        elif len(nationalid) == 7 and nationalid[0] == '9':
            isExist = Cases.objects.filter(caseCode = nationalid)
            if isExist:
                return HttpResponseRedirect(f"q/{nationalid}")
            else:
                return render(request, "inhouse/search.html",{
                    "message" : "برجاء التأكد من الرقم المدخل"
                })
        elif len(nationalid) == 7 and nationalid[0] == '1':
            isExist = Jobs.objects.filter(jobCode = nationalid)  
            if isExist:
                return HttpResponseRedirect(f"q/{nationalid}")
        else:
            return render(request, "inhouse/search.html",{
                    "message" : "برجاء التأكد من الرقم المدخل"
                })        




# If the user serached by PhoneNumber   
    #        elif len(nationalid) == 11:
    #            isExist = Person.objects.filter(personPhoneNum = nationalid)
    #            if isExist:
    #                isExist = Person.objects.get(personPhoneNum = nationalid)
    #                return render(request, "inhouse/searched.html",{
    #                    "personInfo" : Person.objects.get(personPhoneNum = nationalid),
    #                    "familiyInfo" : isExist.relatives.all(),
    #                    "cases": isExist.complain.all(),
    #                    "jobs": isExist.applicants.all(),
    #                })
    #            else:
    #                return render(request, "inhouse/search.html",{
    #                    "message" : "برجاء التأكد من الرقم المدخل"
    #                })              

# Getting a case by link
def getCase(request,casecode):
# Make Sure the user logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
# Check if it's a case of job request
    case = Cases.objects.filter(caseCode=casecode)
    if case:
        case = Cases.objects.get(caseCode=casecode)
        person = case.casePersonaId
        updates = case.caseUpdates.all()
        return render(request, "inhouse/thecase.html",
        {
            "case" : case,
            "person" : person,
            "family" : person.relatives.all(),
            "type" : "case",
            "file" : case.caseScannedDocs,
            "users" : User.objects.all(),
            "updates" : updates
        })
    else:
        case = Jobs.objects.filter(jobCode=casecode) 
        if case:
            case = Jobs.objects.get(jobCode=casecode)
            person = case.jobPersonaId
            updates = case.jobUpdates.all()
            return render(request, "inhouse/thecase.html",
            {
                "case" : case,
                "person" : person,
                "family" : person.relatives.all(),
                "type" : "job",
                "file" : case.jobCV,
                "users" : User.objects.all(),
                "updates" : updates
            })
        else:
            return render(request, "inhouse/index.html")


# Changing the responsible
def changer(request):
# Make Sure the user logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":     
        gottenUser = request.POST["userChanger"]
        caseCodeforchange = request.POST["caseCodeforchange"]
        if caseCodeforchange[0] == '9':
            update = Cases.objects.filter(caseCode=caseCodeforchange).update(caseResponsible=User.objects.get(id=gottenUser))
        elif caseCodeforchange[0] == '1':
            update = Jobs.objects.filter(jobCode=caseCodeforchange).update(JobResponsible=User.objects.get(id=gottenUser))    
        return HttpResponseRedirect(f"q/{caseCodeforchange}")


# Adding a comment
def comment(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":     
        gottenUser =  request.user
        text = request.POST["addedcomment"]
        caseCodeforchange = request.POST["caseCodeforchange"]
        if caseCodeforchange[0] == '9':
            commentt = caseComments.objects.create(CommentCode=Cases.objects.get(caseCode=caseCodeforchange),CommentText=text,CommentWriter=User.objects.get(id=gottenUser.id))
            update = Cases.objects.filter(caseCode=caseCodeforchange).update(caseStatus="ongoing")
        elif caseCodeforchange[0] == '1':
            commentt = jobComments.objects.create(CommentCode=Jobs.objects.get(jobCode=caseCodeforchange),CommentText=text,CommentWriter=User.objects.get(id=gottenUser.id))
            update = Jobs.objects.filter(jobCode=caseCodeforchange).update(jobStatus="ongoing")
        return HttpResponseRedirect(f"q/{caseCodeforchange}")

# Close A case
def close(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":     
        caseCodeforchange = request.POST["caseCodeforchange"]
        newstatus = "closed"
        if caseCodeforchange[0] == '9':
            update = Cases.objects.filter(caseCode=caseCodeforchange).update(caseStatus=newstatus)
        elif caseCodeforchange[0] == '1':
            update = Jobs.objects.filter(jobCode=caseCodeforchange).update(jobStatus=newstatus)
        return HttpResponseRedirect(f"q/{caseCodeforchange}")

# My cases
def mycases(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    gottenUser =  request.user
    theirCases = gottenUser.responsible.all()
    return render(request, "inhouse/mycases.html", {
        "cases" : theirCases
    })        

# My Jobs
def myjobs(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    gottenUser =  request.user
    theirCases = gottenUser.hr.all()
    return render(request, "inhouse/myjobs.html", {
        "cases" : theirCases
    })        

# All New Cases
def allnewcases(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    cases_list = Cases.objects.all().order_by('-id')   
    paginator = Paginator(cases_list, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1    

    try:
        cases = paginator.page(page)
    except(EmptyPage, InvalidPage):
        cases = paginator.page(paginator.num_pages)
    return render(request, "inhouse/allcases.html", {
        "cases" : cases
    })

# All ongoing Cases
def ongoingcases(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    cases_list = Cases.objects.all().order_by('-id')   
    paginator = Paginator(cases_list, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1    

    try:
        cases = paginator.page(page)
    except(EmptyPage, InvalidPage):
        cases = paginator.page(paginator.num_pages)
    return render(request, "inhouse/ongoingcases.html", {
        "cases" : cases
    })    

# All closed Cases
def closedcases(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    cases_list = Cases.objects.all().order_by('-id')   
    paginator = Paginator(cases_list, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1    

    try:
        cases = paginator.page(page)
    except(EmptyPage, InvalidPage):
        cases = paginator.page(paginator.num_pages)
    return render(request, "inhouse/closedcases.html", {
        "cases" : cases
    })        
    
# All new jobs
def allnewjobs(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    cases_list = Jobs.objects.all().order_by('-id')   
    paginator = Paginator(cases_list, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1    

    try:
        cases = paginator.page(page)
    except(EmptyPage, InvalidPage):
        cases = paginator.page(paginator.num_pages)
    return render(request, "inhouse/alljobs.html", {
        "cases" : cases
    })            

# All ongoing jobs
def ongoingjobs(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    cases_list = Jobs.objects.all().order_by('-id')   
    paginator = Paginator(cases_list, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1    

    try:
        cases = paginator.page(page)
    except(EmptyPage, InvalidPage):
        cases = paginator.page(paginator.num_pages)
    return render(request, "inhouse/ongoingjobs.html", {
        "cases" : cases
    })                

# All closed jobs
def closedjobs(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    cases_list = Jobs.objects.all().order_by('-id')   
    paginator = Paginator(cases_list, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1    

    try:
        cases = paginator.page(page)
    except(EmptyPage, InvalidPage):
        cases = paginator.page(paginator.num_pages)
    return render(request, "inhouse/closedjobs.html", {
        "cases" : cases
    })            