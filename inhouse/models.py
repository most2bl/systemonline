from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class Person(models.Model):
    socialState = models.CharField(max_length=12)
    healthState = models.CharField(max_length=12)
    age = models.IntegerField()	
    nationalId = models.BigIntegerField()
    personName = models.CharField(max_length=64)
    personPhoneNum = models.CharField(max_length=12)
    personAddress = models.TextField()
    nationaldExpiryDate = models.CharField(max_length=32)
    idDistrict = models.CharField(max_length=64)
    personSalary = models.IntegerField()	
    personJob = models.CharField(max_length=64)
    personEducationLevel = models.CharField(max_length=64)

class Families(models.Model):
    personaId = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="relatives")     
    individualName = models.CharField(max_length=64)
    individualAge = models.IntegerField()
    individualJob = models.CharField(max_length=64)
    individualHealthState = models.CharField(max_length=12)
    individualSocialState = models.CharField(max_length=12)
    individualEduLevel = models.CharField(max_length=12)
    individualSalary = models.IntegerField()
    individualRole = models.CharField(max_length=32, blank=True)

class Cases(models.Model):
    caseCode = models.CharField(max_length=12)
    casePersonaId = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="complain")
    caseScannedDocs = models.FileField()
    caseTitle = models.CharField(max_length=64)
    caseDetails = models.TextField()
    caseStatus = models.CharField(max_length=20)
    caseDate = models.DateTimeField(auto_now_add=True, blank=True)
    caseResponsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="responsible")
    


class Jobs(models.Model):
    jobCode = models.CharField(max_length=12)
    jobPersonaId = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="applicants")
    jobDate = models.DateTimeField(auto_now_add=True, blank=True)
    jobStatus = models.CharField(max_length=20)
    jobUniversity = models.CharField(max_length=64)
    jobEduMajor = models.CharField(max_length=64)
    jobExtraDetails = models.TextField(blank=True)
    JobResponsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="hr")
    jobCV = models.FileField()
    

class caseComments(models.Model):
    CommentCode = models.ForeignKey(Cases, on_delete=models.CASCADE, related_name="caseUpdates")
    CommentText = models.TextField()
    CommentDate = models.DateTimeField(auto_now_add=True, blank=True)
    CommentWriter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="caseCommentOwner")

class jobComments(models.Model):
    CommentCode = models.ForeignKey(Jobs, on_delete=models.CASCADE, related_name="jobUpdates")
    CommentText = models.TextField()
    CommentDate = models.DateTimeField(auto_now_add=True, blank=True)
    CommentWriter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jobCommentOwner")


