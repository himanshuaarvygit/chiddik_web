from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from urllib.parse import urlsplit, urlunsplit, SplitResult
from urllib.parse import urljoin
import os

from rest_framework import status

from django.db import connection
from .utility import dictfetchAll

from rest_framework.decorators import api_view


@api_view(['POST'])
def tutor_details(request):
      with connection.cursor() as cursor:
        id = request.POST['id']

        count = cursor.execute("SELECT * FROM `tutor` WHERE id = %s", [id])
        # row = cursor.fetchone()
        # log.debug(dictfetchall(cursor))
        if (count>0):
            row = dictfetchAll(cursor)[0] 
            return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':row}, status=status.HTTP_200_OK)   
        else:
            return JsonResponse({'status': True, 'msg': 'Fetched not Successfully','data':None}, status=status.HTTP_200_OK)

@api_view(['POST'])
def tutor_validate(request):
      with connection.cursor() as cursor:
         phone = request.POST['phone']
         count = cursor.execute("SELECT * FROM `tutor` WHERE phone = %s", [phone])
         if (count>0):
            row = dictfetchAll(cursor)[0] 
            return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':row,'valid':1}, status=status.HTTP_200_OK)   
         else:
            return JsonResponse({'status': True, 'msg': 'Fetched not Successfully','valid':0}, status=status.HTTP_200_OK)

@api_view(['POST'])
def tutor_register(request):
      with connection.cursor() as cursor:
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        location = request.POST['location']
        long_tb = request.POST['long_tb']
        lat_tb = request.POST['lat_tb']
        education_cer = request.FILES['education_cer']
        id_proof = request.FILES['id_proof']

        count = cursor.execute("SELECT * FROM `tutor` WHERE phone = %s", [phone])
        if(count>0):
          row = dictfetchAll(cursor)[0] 
          return JsonResponse({'status': True, 'msg': 'User already exists'}, status=status.HTTP_200_OK)   
        else:
          edu_cert_name = f'media/tutor_certificate/edu_cert/{education_cer.name}'
          handle_uploaded_file(education_cer, edu_cert_name)
          
          id_proof_name = f'media/tutor_certificate/id_proof/{id_proof.name}'
          handle_uploaded_file(id_proof, id_proof_name) 

          result = cursor.execute ("INSERT INTO `tutor`(name, email, phone, location, long_tb, lat_tb, education_cer,id_proof) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",[name,email,phone,location,long_tb,lat_tb,edu_cert_name,id_proof_name])
          if (result>0):
            cursor.execute("SELECT * FROM `tutor` WHERE phone = %s", [phone])
            row = dictfetchAll (cursor)[0]
            return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':row}, status=status.HTTP_200_OK)   
          else:
            return JsonResponse({'status': True, 'msg': 'User not register'}, status=status.HTTP_200_OK)

def handle_uploaded_file(file, path):
    destination = open(path, 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()

@api_view(['POST'])
def tutor_edit_details(request):
  with connection.cursor() as cursor:
    try:
      # _json = request.json
      # id = _json['id']
      id = request.POST['id']
      name = request.POST['name']
      location = request.POST['location']
      long_tb = request.POST['long_tb']
      lat_tb = request.POST['lat_tb']
      pic = request.FILES.get('pic','')
      bio =request.POST['bio']
      video_link = request.POST['video_link']

      if pic != '':
        profile_pic = f'media/tutor/{pic.name}'
        handle_uploaded_file(pic, profile_pic)	

        sqlQuery = "UPDATE tutor SET name=%s,location=%s,long_tb=%s,lat_tb=%s,pic=%s,bio=%s,video_link=%s WHERE id=%s"
        # print(name)
        data = (name, location, long_tb, lat_tb,profile_pic,bio,video_link, id)
        result = cursor.execute(sqlQuery, data)
        if (result>0):
          cursor.execute("SELECT * FROM `tutor` where id =%s", [id])
          row = dictfetchAll (cursor)[0]
          return JsonResponse({'status': True, 'msg': 'Updated Successfully','data':row}, status=status.HTTP_200_OK)   
      elif name and location and long_tb and lat_tb and bio and video_link and  id:
        sqlQuery = "UPDATE tutor SET name=%s,location=%s,long_tb=%s,lat_tb=%s,bio=%s,video_link=%s WHERE id=%s"
        data = (name, location, long_tb, lat_tb,bio,video_link, id)
        result = cursor.execute(sqlQuery, data)
        if (result>0):
          cursor.execute("SELECT * FROM `tutor` where id =%s", [id])
          row = dictfetchAll (cursor)[0]
          return JsonResponse({'status': True, 'msg': 'Updated Successfully','data':row}, status=status.HTTP_200_OK)   
      else:
        return JsonResponse({'status': False, 'msg': 'Tutor not update'}, status=status.HTTP_200_OK)
    except Exception as e:
      print(e)
      return JsonResponse({'status': False, 'msg': 'Tutor not update here'}, status=status.HTTP_200_OK)
    finally:
      cursor.close() 

def handle_uploaded_file(file, path):
    destination = open(path, 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()

@api_view(['POST'])
def search_tutor(request):
  with connection.cursor() as cursor:
    name = request.POST.get('name', '')
    location = request.POST.get('location','')
    c_id = request.POST.get('c_id','')
    s_id = request.POST.get('s_id','')
    # clas_type = request.POST['class_type']
    # min_price = request.POST['min_price']
    # max_price = request.POST['max_price']
    print(s_id)

    
    # count = cursor.execute("SELECT tutor.*,services.c_id,services.s_id FROM `tutor` JOIN services ON services.t_id=tutor.id WHERE name=%s ORDER BY RAND() limit 20 offset 0 ", [name])
    if name:
      cursor.execute("SELECT tutor.*,services.c_id,services.s_id FROM `tutor` JOIN services ON services.t_id=tutor.id WHERE name=%s ORDER BY RAND() LIMIT 20 OFFSET 0 ", [name])
      row = dictfetchAll(cursor)
      return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':row}, status=status.HTTP_200_OK)
    elif location: 
      cursor.execute("SELECT tutor.*,services.c_id,services.s_id FROM `tutor` JOIN services ON services.t_id=tutor.id WHERE location=%s ORDER BY RAND() limit 20 offset 0 ", [location])
      row = dictfetchAll(cursor)
      return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':row}, status=status.HTTP_200_OK)
    elif c_id and s_id: 
      cursor.execute("SELECT tutor.*,services.c_id,services.s_id FROM `tutor` JOIN services ON services.t_id=tutor.id WHERE c_id=%s and s_id=%s ORDER BY RAND() limit 20 offset 0 ", [c_id,s_id])
      row = dictfetchAll(cursor)
      return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':row}, status=status.HTTP_200_OK)
    else:
      return JsonResponse({'status': False, 'msg': 'Fetched not Successfully'}, status=status.HTTP_200_OK)
      
      
def check_valid_tutor(tutorId):
  with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM `tutor` where id =%s", [tutorId])
    row = dictfetchAll(cursor)
    if(len(row)>0):
      return True
    else:
      return False