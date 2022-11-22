from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as authlogin
from django.contrib.auth import logout as authlogout
from django.conf import settings
# Create your views here.

# Create your views here.
def index(request):
    return HttpResponse("<h2>Invalid Entry point </h2>")
# home
def home(request):
    errorResponse = {
        "success": True,
        "message": ""
          }
    if request.method == 'GET':
        return render(request, "login.html")
    else:
      inputUsername = request.POST["inputUsername"]
      inputPassword = request.POST["inputPassword"]
      #############################################
      if not inputUsername:
        errorResponse = {
        "success": False,
        "message": "Username are required"
          }
      elif not inputPassword:
        errorResponse = {
        "success": False,
        "message": "Pssword are required"
          }
      else:
          user = authenticate(request, username=inputUsername, password=inputPassword)
          if user is not None:
            authlogin(request, user)
            return redirect('dashboard')
          else:
              errorResponse = {
              "success": False,
              "message": "Invalid login details"
               }
    return render(request, "login.html", errorResponse)


# login
def logout(request):
    authlogout(request)
    return redirect('home')

def dashboard(request):
#   if not request.user.is_authenticated:
#     return redirect('/?error=Invalid entry, please login first')
  return render(request, "dashboard.html")