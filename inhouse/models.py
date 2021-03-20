from django.db import models

# Create your models here.
class Users(models.Model):
    userId = models.AutoField()	
    userName = models.CharField(Max_length=64)
    realName = models.CharField(Max_length=64)
    phoneNum = models.CharField(Max_length=12)
    userPassword = models.CharField(Max_length=64)


class Person(models.Model):
    socialState = models.CharField(max_length=12)
    healthState = models.CharField(max_length=12)
    age = models.IntegerField()	
    personId = models.AutoField()
    nationalId = models.BigIntegerField()
    personName = models.CharField(Max_length=64)
    personPhoneNum = models.CharField(Max_length=12)
    personAddress = models.TextField()
    nationaldExpiryDate = models.DateField()
    idDistrict = models.CharField(Max_length=64)
    scannedId = models.BinaryField()
    personSalary = models.IntegerField()	
    personJob = models.CharField(Max_length=64)
    personEducationLevel = models.CharField(Max_length=64)

class Families(models.Model):
    personaId = models.ForeignKey(Person, on_delete=models.CASCADE)     
    individualName = models.CharField(Max_length=64)
    individualAge = models.IntegerField()
    individualJob = models.CharField(max_length=64)
    individualHealthState = models.CharField(max_length=12)
    individualSocialState = models.CharField(max_length=12)
    individualEduLevel = models.CharField(max_length=12)
    individualSalary = models.IntegerField()

class Cases(models.Model):
    caseCode = models.CharField(Max_length=12)
    casePersonaId = models.ForeignKey(Person, on_delete=models.CASCADE)
    casdId = models.AutoField()
    caseScannedDocs = models.BinaryField()
    caseTitle = models.CharField(max_length=64)
    caseDetails = models.TextField()
    caseStatus = models.CharField(Max_length=12)
    caseDate = models.DateTimeField()
    caseResponsible = models.ForeignKey(Users, on_delete=models.CASCADE)


class Jobs(models.Model):
    jobCode = models.CharField(Max_length=12)
    jobPersonaId = models.ForeignKey(Person, on_delete=models.CASCADE)
    jobId = models.AutoField()
    jobDate = models.DateTimeField()
    jobStatus = models.CharField(Max_length=12)
    jobEduLevel = models.CharField(max_length=64)
    jobEduMajor = models.CharField(max_length=64)
    JobResponsible = models.ForeignKey(Users, on_delete=models.CASCADE)
    jobScannedDocs = models.BinaryField()
    jobCV = models.BinaryField()


class Experience(models.Model):
    startingDate = models.IntegerField()
    endingDate = models.IntegerField()
    companyName = models.CharField(max_length=64)
    role = models.CharField(max_length=64)
    personaId = models.ForeignKey(Person, on_delete=models.CASCADE)     

    

class caseComments(models.Model):
    caseCommentId = models.AutoField()
    caseCommentCode = models.ForeignKey(Cases, on_delete=models.CASCADE)
    caseCommentText = models.TextField()
    caseCommentDate = models.DateTimeField()
    caseCommentWriter = models.ForeignKey(Users, on_delete=models.CASCADE)

class jobComments(models.Model):
    jobCommentId = models.AutoField()
    jobCommentCode = models.ForeignKey(Cases, on_delete=models.CASCADE)
    jobCommentText = models.TextField()
    jobCommentDate = models.DateTimeField()
    JobCommentWriter = models.ForeignKey(Users, on_delete=models.CASCADE)


