from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib import messages

# Create your views here.

def index(request):
   return render(request,'index.html')


