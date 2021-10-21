from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
import json
from api.models import Slots
import os

from rest_framework import status

from django.db import connection
from .utility import dictfetchAll

from rest_framework.decorators import api_view


# Create your views here.

@api_view(['GET'])
def get_all_classes(request):
  with connection.cursor() as cursor:
    request.GET
    cursor.execute("SELECT * FROM `class` where status = 'active'")
    row = dictfetchAll(cursor)
  return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data': row}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_subject(request):
  with connection.cursor() as cursor:
    id=request.GET['id']
    count = cursor.execute("SELECT id,name,c_id,status FROM `subject` where c_id = %s",[id])
    if(count>0):
      row = dictfetchAll(cursor)
      return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data': row}, status=status.HTTP_200_OK)
    else:
      return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':[]}, status=status.HTTP_200_OK)

@api_view(['GET'])
def terms_and_condition(request):
  with connection.cursor() as cursor:
    request.GET
    cursor.execute("SELECT id,terms_condition_tutor,privacy_policy_tutor,terms_condition_stud,privacy_policy_stud,about_us,status FROM `pages` where status = 'active'")
    row = dictfetchAll(cursor)[0]
  return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data': row}, status=status.HTTP_200_OK) 

@api_view(['GET'])
def get_all_day(request):
  with connection.cursor() as cursor:
    request.GET
    cursor.execute("SELECT id,day,status FROM `day` where status =  'active'")
    row = dictfetchAll(cursor)
  return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data': row}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_banner(request):
  with connection.cursor() as cursor:
    request.GET
    cursor.execute("SELECT id,name,status FROM `banner` where status =  'active'")
    row = dictfetchAll(cursor)
  return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data': row}, status=status.HTTP_200_OK)

# @api_view(['GET'])
# def get_subject(request):
#   with connection.cursor() as cursor:
#     id=request.GET['id']
#     count = cursor.execute("SELECT id,name,c_id,status FROM `subject` where c_id = %s",[id])
#     if(count>0):
#       row = dictfetchAll(cursor)
#       return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data': row}, status=status.HTTP_200_OK)
#     else:
#       return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':[]}, status=status.HTTP_200_OK)
