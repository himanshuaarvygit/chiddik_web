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
        # cursor.execute('CREATE TEMPORARY TABLE `temp_tutor` AS SELECT * FROM `tutor`;')
        # cursor.execute('ALTER TABLE `temp_tutor` DROP COLUMN `coordinates`;')
        # cursor.execute('SELECT * FROM temp_sale_details; ')

        # `id`, `name`, `email`, `phone`, `id_proof`, `education_cer`, `location`, `pic`, `status`, `video_link`, `bio`, `wallet`
        sql = "SELECT *, ST_X(coordinates) as lat_tb, ST_Y(coordinates) as long_tb FROM `tutor` WHERE id = %s"
        count = cursor.execute(sql, [id])
        # row = cursor.fetchone()
        # log.debug(dictfetchall(cursor))
        if (count>0):
          row = dictfetchAll(cursor)[0]
          row.pop('coordinates') 
          print(row)
          return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':row}, status=status.HTTP_200_OK)   
        else:
          return JsonResponse({'status': True, 'msg': 'Fetched not Successfully','data':None}, status=status.HTTP_200_OK)

@api_view(['POST'])
def tutor_validate(request):
      with connection.cursor() as cursor:
         phone = request.POST['phone']
         count = cursor.execute("SELECT *, ST_X(coordinates) as lat_tb, ST_Y(coordinates) as long_tb FROM `tutor` WHERE phone = %s", [phone])
         if (count>0):
            row = dictfetchAll(cursor)[0] 
            row.pop('coordinates')
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
          # row = dictfetchAll(cursor)[0] 
          return JsonResponse({'status': True, 'msg': 'User already exists'}, status=status.HTTP_200_OK)   
        else:
          edu_cert_name = f'media/tutor_certificate/edu_cert/{education_cer.name}'
          handle_uploaded_file(education_cer, edu_cert_name)
          
          id_proof_name = f'media/tutor_certificate/id_proof/{id_proof.name}'
          handle_uploaded_file(id_proof, id_proof_name) 
          lat = float(lat_tb)
          lon = float(long_tb)
          result = cursor.execute ("INSERT INTO `tutor`(name, email, phone, location, education_cer, id_proof, coordinates) VALUES (%s,%s,%s,%s,%s,%s, ST_GeomFromText('POINT(%s %s)'))",[name,email,phone,location,edu_cert_name,id_proof_name,lat,lon])
          if (result>0):
            cursor.execute("SELECT *, ST_X(coordinates) as lat_tb, ST_Y(coordinates) as long_tb FROM `tutor` WHERE phone = %s", [phone])
            row = dictfetchAll (cursor)[0]
            row.pop('coordinates')
            return JsonResponse({'status': True, 'msg': 'Registered Successfully','data':row}, status=status.HTTP_200_OK)   
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

        sqlQuery = "UPDATE tutor SET name=%s,location=%s,pic=%s,bio=%s,video_link=%s,coordinates=ST_GeomFromText('POINT(%s %s)') WHERE id=%s"
        # print(name)
        data = (name, location, profile_pic,bio,video_link,lat_tb, long_tb, id)
        result = cursor.execute(sqlQuery, data)
        if (result>0):
          cursor.execute("SELECT *, ST_X(coordinates) as lat_tb, ST_Y(coordinates) as long_tb FROM `tutor` where id =%s", [id])
          row = dictfetchAll (cursor)[0]
          row.pop('coordinates')
          return JsonResponse({'status': True, 'msg': 'Updated Successfully','data':row}, status=status.HTTP_200_OK)   
      elif name and location and long_tb and lat_tb and bio and video_link and  id:
        sqlQuery = "UPDATE tutor SET name=%s,location=%s,bio=%s,video_link=%s,coordinates=ST_GeomFromText('POINT(%s %s)') WHERE id=%s"
        data = (name, location, bio,video_link,lat_tb, long_tb, id)
        result = cursor.execute(sqlQuery, data)
        if (result>0):
          cursor.execute("SELECT *, ST_X(coordinates) as lat_tb, ST_Y(coordinates) as long_tb FROM `tutor` where id =%s", [id])
          row = dictfetchAll (cursor)[0]
          row.pop('coordinates')
          return JsonResponse({'status': True, 'msg': 'Updated Successfully','data':row}, status=status.HTTP_200_OK)   
      else:
        return JsonResponse({'status': False, 'msg': 'Tutor not update'}, status=status.HTTP_200_OK)
    except Exception as e:
      print(e)
      return JsonResponse({'status': False, 'msg': 'Tutor not update here'}, status=status.HTTP_200_OK)
    finally:
      cursor.close() 


@api_view(['POST'])
def search_tutor(request):
  with connection.cursor() as cursor:
    name = request.POST.get('name', '')
    lat = request.POST.get('lat','')
    lon = request.POST.get('lon','')
    c_id = request.POST.get('c_id','')
    s_id = request.POST.get('s_id','')
    class_type = request.POST.get('class_type','')
    min_price = request.POST.get('min_price','')
    max_price = request.POST.get('max_price','')
    page = request.POST.get('page','0')

    tutorResult = []
    pageCount = int(page)*20
    
    sql = ""
    nameQuery = ""
    classSubjectQuery = ""
    classTypeQuery = ""
    

    if name=='' and lat =='' and lon =='' and class_type=='' and c_id=='' and s_id=='' and min_price =='' and max_price =='':
      sql = f"SELECT DISTINCT(`id`) FROM `tutor` WHERE `status`='active' ORDER BY `id` DESC LIMIT {pageCount}, 20"
    else:
      if name!='':
        nameQuery = f"AND `tutor`.`name` LIKE '%{name}%'"
      
      if class_type=='group':
        if min_price !='' and max_price !='':
          classTypeQuery = f"AND (`services`.`type_group` = 'yes' AND `services`.`group_price` >= {min_price} AND `services`.`group_price` <= {max_price})"
        else:
          classTypeQuery = f"AND (`services`.`type_group` = 'yes')"
      elif class_type=='personal':
        if min_price !='' and max_price !='':
          classTypeQuery = f"AND (`services`.`type_personal` = 'yes' AND `services`.`personal_price` >= {min_price} AND `services`.`personal_price` <= {max_price})"
        else:
          classTypeQuery = f"AND (`services`.`type_personal` = 'yes')"
      else:
        if min_price !='' and max_price !='':
          classTypeQuery = f"AND (`services`.`group_price` >= {min_price} AND `services`.`group_price` <= {max_price})"

      if c_id !='':
        if s_id !='':
          classSubjectQuery = f"AND services`.`c_id` = {c_id} AND `services`.`s_id` = {s_id}"
        else:
          classSubjectQuery = f"AND services`.`c_id` = {c_id}"
      
      
      
      if lat !='' and lon !='':
        #all query with lat lon
        sql = f"""
          SELECT 
              DISTINCT(tutor.id),
              (6371 * ACOS(COS(RADIANS({lat})) * COS(RADIANS(Y(coordinates))) 
              * COS(RADIANS(X(coordinates)) - RADIANS({lon})) + SIN(RADIANS({lat}))
              * SIN(RADIANS(Y(coordinates))))) AS distance
          FROM `tutor`
          LEFT JOIN `services` ON `tutor`.`id` = `services`.`t_id`
          WHERE MBRContains (
              LineString (
                  Point (
                      {lon} + 15 / (111.320 * COS(RADIANS({lat}))),
                      {lat} + 15 / 111.133
                  ),
                  Point (
                      {lon} - 15 / (111.320 * COS(RADIANS({lat}))),
                      {lat} - 15 / 111.133
                  )
              ),
              coordinates
              )
              AND `services`.`status` = 'active'
              {nameQuery}
              {classSubjectQuery}
              {classTypeQuery}
          HAVING distance < 15
          ORDER By distance
          LIMIT {pageCount}, 20
        """
      else:
        #all queries without lat lon
        sql = f"""
          SELECT 
              DISTINCT(tutor.id)
          FROM `tutor`
          LEFT JOIN `services` ON `tutor`.`id` = `services`.`t_id`
          WHERE 
              `services`.`status` = 'active'
              {nameQuery}
              {classSubjectQuery}
              {classTypeQuery}
          ORDER BY `id` DESC
          LIMIT {pageCount}, 20
        """

    print(sql)
    cursor.execute(sql)
    result = dictfetchAll(cursor)
    for t in result:
      id = t['id']
      cursor.execute("SELECT *, ST_X(coordinates) as lat_tb, ST_Y(coordinates) as long_tb FROM `tutor` WHERE `id`=%s", [id])
      tRes = dictfetchAll(cursor)
      if len(tRes) != 0:
        data = tRes[0]
        data.pop('coordinates')
        tutorResult.append(data)

    return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':tutorResult}, status=status.HTTP_200_OK)
      
      
def check_valid_tutor(tutorId):
  with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM `tutor` where id =%s", [tutorId])
    row = dictfetchAll(cursor)
    if(len(row)>0):
      return True
    else:
      return False