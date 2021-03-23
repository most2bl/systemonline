from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Person)
admin.site.register(Families)
admin.site.register(Cases)
admin.site.register(Jobs)
admin.site.register(caseComments)
admin.site.register(jobComments)
