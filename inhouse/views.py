from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# The Index page
def index(request):
    return render(request, "inhouse/index.html")

# Sign in function here

# Sign up function here

# Handling apply to a job url