from django.db import models
from django.contrib.auth.models import User

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

class Cases(models.Model):
    caseCode = models.CharField(max_length=12)
    casePersonaId = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="complain")
    caseScannedDocs = models.BinaryField()
    caseTitle = models.CharField(max_length=64)
    caseDetails = models.TextField()
    caseStatus = models.CharField(max_length=12)
    caseDate = models.DateTimeField()
    caseResponsible = models.OneToOneField(User, on_delete=models.CASCADE, related_name="responsible")


class Jobs(models.Model):
    jobCode = models.CharField(max_length=12)
    jobPersonaId = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="applicants")
    jobDate = models.DateTimeField()
    jobStatus = models.CharField(max_length=12)
    jobEduLevel = models.CharField(max_length=64)
    jobEduMajor = models.CharField(max_length=64)
    JobResponsible = models.OneToOneField(User, on_delete=models.CASCADE, related_name="hr")
    jobScannedDocs = models.BinaryField()
    jobCV = models.BinaryField()


class Experience(models.Model):
    startingDate = models.IntegerField()
    endingDate = models.IntegerField()
    companyName = models.CharField(max_length=64)
    role = models.CharField(max_length=64)
    personaId = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="experiences")     

    

class caseComments(models.Model):
    caseCommentCode = models.ForeignKey(Cases, on_delete=models.CASCADE, related_name="caseUpdates")
    caseCommentText = models.TextField()
    caseCommentDate = models.DateTimeField()
    caseCommentWriter = models.OneToOneField(User, on_delete=models.CASCADE, related_name="caseCommentOwner")

class jobComments(models.Model):
    jobCommentCode = models.ForeignKey(Cases, on_delete=models.CASCADE, related_name="jobUpdates")
    jobCommentText = models.TextField()
    jobCommentDate = models.DateTimeField()
    JobCommentWriter = models.OneToOneField(User, on_delete=models.CASCADE, related_name="jobCommentOwner")


