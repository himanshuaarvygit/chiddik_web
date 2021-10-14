from django.contrib.auth.models import User
from backend.EmailBackEnd import EmailBackEnd
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from backend.models import Pages, Class, Subject
from django.db import connection
from .utility import dictfetchAll


# Create your views here.

def showlogin(request):
   # if request.user!=None:
   #    return redirect('dashboard')
   # else:
   return render(request,'backend/login.html')

def login1(request):
   if request.method == "POST":
      user=EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
      if user!=None:
         login(request, user)
         if user.user_type=="1":
         # request.session['user']=request.POST.get("email") 
            return redirect('dashboard')
   else:
      messages.error(request, 'invalide Credentials, Please try again')
      return HttpResponse('invalid') 

def logout_admin(request):
   # print(request.user)
   logout(request)
   # return HttpResponse(request.user)
   return redirect('showlogin')

@login_required
def dashboard(request):
   if request.user!=None:
      return render(request,'backend/dashboard.html')
   else:
      return HttpResponse("please login first")

@login_required   
def terms_condition_tutor(request,id):
   term_t=Pages.objects.get(id=1)
   # print(term_t)
   if request.method=='POST':
      term_t.terms_condition_tutor = request.POST['terms_condition_tutor']
      term_t.save()
      messages.success(request,"Update successfully.")
      # return redirect('terms_condition_tutor')
   return render(request,'backend/terms_condition_tutor.html',{'terms':term_t})

@login_required
def privacy_policy_tutor(request,id):
   term_p=Pages.objects.get(id=1)
   # print(term_p)
   if request.method=='POST':
      term_p.privacy_policy_tutor = request.POST['privacy_policy_tutor']
      term_p.save()
      messages.success(request,"Update successfully.")
   return render(request,'backend/privacy_policy_tutor.html',{'terms':term_p})

@login_required
def terms_condition_stud(request,id):
   term_s=Pages.objects.get(id=1)
   # print(term_s)
   if request.method=='POST':
      term_s.terms_condition_stud = request.POST['terms_condition_stud']
      term_s.save()
      messages.success(request,"Update successfully.")
   return render(request,'backend/terms_condition_stud.html',{'terms':term_s})

@login_required
def privacy_policy_stud(request,id):
   term_sp=Pages.objects.get(id=1)
   # print(term_sp)
   if request.method=='POST':
      term_sp.privacy_policy_stud = request.POST['privacy_policy_stud']
      term_sp.save()
      messages.success(request,"Update successfully.") 
   return render(request,'backend/privacy_policy_stud.html',{'terms':term_sp})

@login_required
def about_us(request,id):
   about=Pages.objects.get(id=1)
   # print(about)
   if request.method=='POST':
      about.about_us = request.POST['about_us']
      about.save()
      messages.success(request,"Update successfully.")
   return render(request,'backend/about_us.html',{'terms':about})

@login_required
def add_class(request):
   if request.method=='POST':
      cls = Class()
      cls.name = request.POST['name']
      cls.save()
      messages.success(request,"Class Added successfully.")
      return redirect('list_class')
   return render(request,'backend/add_class.html')

@login_required
def list_class(request):
   with connection.cursor() as cursor:
      cursor.execute("SELECT * FROM `class`")
      row = dictfetchAll(cursor)
      return render(request,'backend/list_class.html',{'cls_list':row})

@login_required
def edit_class(request, id):
   cls_edit= Class.objects.get(id=id)
   # print(cls_edit)
   if request.method=='POST':
      cls_edit.name = request.POST['name']
      cls_edit.save()
      messages.success(request,"Update successfully.")
   return render(request,'backend/edit_class.html',{'cls_edit':cls_edit})

@login_required
def delete_class(request,id):
   cls_delete= Class.objects.filter(id=id)
   cls_delete.delete()
   messages.success(request,"Delete successfully.")
   return redirect('list_class')

@login_required
def add_subject(request):
   cls_d= Class.objects.all()
   # print(cls_d)
   if request.method=='POST':
      sub = Subject()
      sub.c_id = request.POST['c_id']
      sub.name = request.POST['name']
      sub.save()
      messages.success(request,"Class Added successfully.")
      return redirect('add_subject')
   return render(request,'backend/add_subject.html',{'cld':cls_d})

@login_required
def list_subject(request):
   with connection.cursor() as cursor:
      cursor.execute("SELECT subject.*,class.name AS class FROM `subject` JOIN class ON subject.c_id=class.id")
      row = dictfetchAll(cursor)
      return render(request,'backend/list_subject.html',{'sub_list':row})

@login_required
def edit_subject(request, id):
   clss_d= Class.objects.all()
   sub_edit= Subject.objects.get(id=id)
   # print(sub_edit)
   if request.method=='POST':
      sub_edit.c_id = request.POST['c_id']
      sub_edit.name = request.POST['name']
      # sub_edit.updated_at = date['Y-m-d']
      sub_edit.save()
      messages.success(request,"Update successfully.")
   context = {
      'sub_edit':sub_edit,
      'clss_d':clss_d,
   }
   return render(request,'backend/edit_subject.html',context)

@login_required
def delete_subject(request,id):
   sub_delete= Subject.objects.filter(id=id)
   sub_delete.delete()
   messages.success(request,"Delete successfully.")
   return redirect('list_subject')

@login_required
def class_request(request):
   with connection.cursor() as cursor:
      cursor.execute("SELECT class_request.*,tutor.name AS tutor FROM `class_request` JOIN tutor ON class_request.t_id=tutor.id")
      row = dictfetchAll(cursor)
      return render(request,'backend/class_request.html',{'request':row})

   




