from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from django.template import loader
# Create your views here.

def index(request):
    return HttpResponse("reached a profile")

def view_id(request, user_id):
    return HttpResponse("<h2>user id: " + str(user_id) + "</h2>")

def view_users(request):
    return HttpResponse("nothing yet")