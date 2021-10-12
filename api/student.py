from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse

from rest_framework import status

from django.db import connection
from .utility import dictfetchAll

from rest_framework.decorators import api_view



@api_view(['POST'])
def student_details(request):
      with connection.cursor() as cursor:
        id = request.POST['id']
        # cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        count = cursor.execute("SELECT * FROM `student` WHERE id = %s", [id])
        # row = cursor.fetchone()
        # log.debug(dictfetchall(cursor))
        if (count>0):
            row = dictfetchAll(cursor)[0] 
            return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':row}, status=status.HTTP_200_OK)   
        else:
            return JsonResponse({'status': True, 'msg': 'Fetched not Successfully','data':None}, status=status.HTTP_200_OK)

@api_view(['POST'])
def student_validate(request):
      with connection.cursor() as cursor:
         phone = request.POST['phone']
         count = cursor.execute("SELECT * FROM `student` WHERE phone = %s", [phone])
         if (count>0):
            row = dictfetchAll(cursor)[0] 
            return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':row,'valid':1}, status=status.HTTP_200_OK)   
         else:
            return JsonResponse({'status': True, 'msg': 'Fetched not Successfully','valid':0}, status=status.HTTP_200_OK)

@api_view(['POST'])
def student_register(request):
      with connection.cursor() as cursor:
        phone = request.POST['phone']
        name = request.POST['name']
        email = request.POST['email']
        # location = request.POST['location']
        # long_tb = request.POST['long_tb']
        # lat_tb = request.POST['lat_tb']

        count = cursor.execute("SELECT * FROM `student` WHERE phone = %s", [phone])
        if(count>0):
          row = dictfetchAll(cursor)[0]
          return JsonResponse({'status': True, 'msg': 'Student already exists'}, status=status.HTTP_200_OK)   
        else:
          result = cursor.execute ("INSERT INTO `student`(phone, name, email) VALUES (%s,%s,%s)",[phone,name,email])
          # row = cursor.fetchone()
          # log.debug(dictfetchall(cursor))
          if (result>0):
            cursor.execute("SELECT * FROM `student` WHERE phone = %s", [phone])
            row = dictfetchAll(cursor)[0]
            return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':row}, status=status.HTTP_200_OK)   
          else:
            return JsonResponse({'status': True, 'msg': 'Student not register'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def student_edit_details(request):
  with connection.cursor() as cursor:
    try:
      id = request.POST['id']
      name = request.POST['name']
      pic = request.FILES.get('pic','')
      
      # print(pic)
      if pic != '':	
        profile_pic = f'media/student/{pic.name}'
        handle_uploaded_file(pic, profile_pic)					
        sqlQuery = "UPDATE student SET name=%s, pic=%s  WHERE id=%s"
        # print(name)
        data = (name, profile_pic, id)
        result = cursor.execute(sqlQuery, data)
        if (result>0):
          cursor.execute("SELECT * FROM `student` where id =%s", [id])
          row = dictfetchAll (cursor)[0]
          return JsonResponse({'status': True, 'msg': 'Updated Successfully','data':row}, status=status.HTTP_200_OK)   
      elif name and id :
        sqlQuery = "UPDATE student SET name=%s  WHERE id=%s"
        data = (name, id)
        result = cursor.execute(sqlQuery, data)
        if (result>0):
          cursor.execute("SELECT * FROM `student` where id =%s", [id])
          row = dictfetchAll (cursor)[0]
          return JsonResponse({'status': True, 'msg': 'Updated Successfully','data':row}, status=status.HTTP_200_OK)   
      else:
        return JsonResponse({'status': False, 'msg': 'Student not update'}, status=status.HTTP_200_OK)
    except Exception as e:
      print(e)
      return JsonResponse({'status': False, 'msg': 'Student not update here'}, status=status.HTTP_200_OK)
    finally:
      cursor.close() 

def handle_uploaded_file(file, path):
    destination = open(path, 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()