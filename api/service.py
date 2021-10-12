from django.http import request
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
import json
from api.models import Slots
import os
from datetime import datetime, timedelta

from rest_framework import status

from django.db import connection
from .utility import dictfetchAll

from rest_framework.decorators import api_view


@api_view(['POST'])
def add_tutor_service(request):
      with connection.cursor() as cursor:
        t_id = request.POST['t_id']
        c_id = request.POST['c_id']
        s_id = request.POST['s_id']
        type_personal = request.POST['type_personal']
        type_group = request.POST['type_group']
        personal_price = request.POST['personal_price']
        group_price = request.POST['group_price']
        
        count = cursor.execute("SELECT * FROM `tutor` WHERE id = %s", [t_id])
        if(count>0):
          if(c_id == '0'):
            c_other = request.POST.get('c_other', '')
            s_other = request.POST.get('s_other', '')

            if(c_other==''):
              return JsonResponse({'status': False, 'msg': 'Other class name not given','data':None}, status=status.HTTP_200_OK)
            if(s_other==''):
              return JsonResponse({'status': False, 'msg': 'Other subject name not given','data':None}, status=status.HTTP_200_OK)

            cursor.execute("INSERT INTO `class_request`(t_id, name) VALUES (%s,%s)",[t_id,c_other])
            cr_id = cursor.lastrowid
            cursor.execute("INSERT INTO `subject_request`(t_id,c_id,name) VALUES (%s,%s,%s)",[t_id,cr_id,s_other])
            sr_id = cursor.lastrowid

            if(type_personal == 'yes' and type_group == 'yes'):
              result = cursor.execute("INSERT INTO `services`(t_id,c_id,s_id,type_personal,type_group,personal_price,group_price) VALUES (%s,%s,%s,%s,%s,%s,%s)",[t_id,cr_id,sr_id,type_personal,type_group,personal_price,group_price])
              if (result>0):
                id = cursor.lastrowid
                cursor.execute("SELECT * FROM `services` WHERE id = %s", [id])
                row = dictfetchAll(cursor)[0]
                return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':row}, status=status.HTTP_200_OK)
              else:
                return JsonResponse({'status': False, 'msg': 'Error Occurred! Please try again!','error': 'ERROR'}, status=status.HTTP_200_OK)    
            elif(type_personal == 'yes'):
              cursor.execute("INSERT INTO `services`(t_id,c_id,s_id,type_personal,type_group,personal_price,group_price) VALUES (%s,%s,%s,%s,%s,%s,%s)",[t_id,cr_id,sr_id,type_personal,type_group,personal_price,group_price])
              id = cursor.lastrowid
              cursor.execute("SELECT * FROM `services` WHERE id = %s", [id])
              row = dictfetchAll(cursor)[0]
              return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':row}, status=status.HTTP_200_OK)
            elif(type_group == 'yes'):
              cursor.execute("INSERT INTO `services`(t_id,c_id,s_id,type_personal,type_group,personal_price,group_price) VALUES (%s,%s,%s,%s,%s,%s,%s)",[t_id,cr_id,sr_id,type_personal,type_group,personal_price,group_price])
              id = cursor.lastrowid
              cursor.execute("SELECT * FROM `services` WHERE id = %s", [id])
              row = dictfetchAll(cursor)[0]
              return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':row}, status=status.HTTP_200_OK)
              
          else:
            if(s_id == '0'):
              is_cid_active = 1
              s_other = request.POST.get('s_other','')
              # print(f"s_other : {s_other}")
              if(s_other==''):
                return JsonResponse({'status': True, 'msg': 'Other subject name not given','data':None}, status=status.HTTP_200_OK)
              count = cursor.execute("INSERT INTO `subject_request`(t_id,c_id,name,is_cid_active) VALUES (%s,%s,%s,%s)",[t_id,c_id,s_other,int(is_cid_active)])
              sr_id = cursor.lastrowid

              
              if(type_personal == 'yes' and type_group == 'yes'):
                result = cursor.execute("INSERT INTO `services`(t_id,c_id,s_id,type_personal,type_group,personal_price,group_price) VALUES (%s,%s,%s,%s,%s,%s,%s)",[t_id,c_id,sr_id,type_personal,type_group,personal_price,group_price])
                if (result>0):
                  id = cursor.lastrowid
                  cursor.execute("SELECT * FROM `services` WHERE id = %s", [id])
                  row = dictfetchAll(cursor)[0]
                  return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':row}, status=status.HTTP_200_OK)
                else:
                  return JsonResponse({'status': False, 'msg': 'Error Occurred! Please try again!','error': 'ERROR'}, status=status.HTTP_200_OK)    
              elif(type_personal == 'yes'):
                cursor.execute("INSERT INTO `services`(t_id,c_id,s_id,type_personal,type_group,personal_price,group_price) VALUES (%s,%s,%s,%s,%s,%s,%s)",[t_id,c_id,sr_id,type_personal,type_group,personal_price,group_price])
                id = cursor.lastrowid
                cursor.execute("SELECT * FROM `services` WHERE id = %s", [id])
                row = dictfetchAll(cursor)[0]
                return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':row}, status=status.HTTP_200_OK)
              elif(type_group == 'yes'):
                result = cursor.execute("INSERT INTO `services`(t_id,c_id,s_id,type_personal,type_group,personal_price,group_price) VALUES (%s,%s,%s,%s,%s,%s,%s)",[t_id,c_id,sr_id,type_personal,type_group,personal_price,group_price])
                if (result>0):
                  id = cursor.lastrowid
                  cursor.execute("SELECT * FROM `services` WHERE id = %s", [id])
                  row = dictfetchAll(cursor)[0]
                  return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':row}, status=status.HTTP_200_OK)
                else:
                  return JsonResponse({'status': False, 'msg': 'Error Occurred! Please try again!','error': 'ERROR'}, status=status.HTTP_200_OK)          
            
            else:
              # count = cursor.execute("SELECT * FROM `class` WHERE id = %s", [c_id])
              if(type_personal == 'yes' and type_group == 'yes'):
                result = cursor.execute("INSERT INTO `services`(t_id,c_id,s_id,type_personal,type_group,personal_price,group_price,status,c_status,s_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[t_id,c_id,s_id,type_personal,type_group,personal_price,group_price,'active','active','active'])
                if (result>0):
                  id = cursor.lastrowid
                  cursor.execute("SELECT * FROM `services` WHERE id = %s", [id])
                  row = dictfetchAll(cursor)[0]
                  return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':row}, status=status.HTTP_200_OK)
                else:
                  return JsonResponse({'status': False, 'msg': 'Error Occurred! Please try again!','error': 'ERROR'}, status=status.HTTP_200_OK)    
              elif(type_personal == 'yes'):
                cursor.execute("INSERT INTO `services`(t_id,c_id,s_id,type_personal,type_group,personal_price,group_price,status,c_status,s_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[t_id,c_id,s_id,type_personal,type_group,personal_price,group_price,'active','active','active'])
                id = cursor.lastrowid
                cursor.execute("SELECT * FROM `services` WHERE id = %s", [id])
                row = dictfetchAll(cursor)[0]
                return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':row}, status=status.HTTP_200_OK)
              elif(type_group == 'yes'):
                cursor.execute("INSERT INTO `services`(t_id,c_id,s_id,type_personal,type_group,personal_price,group_price,status,c_status,s_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[t_id,c_id,s_id,type_personal,type_group,personal_price,group_price,'active','active','active'])
                id = cursor.lastrowid
                cursor.execute("SELECT * FROM `services` WHERE id = %s", [id])
                row = dictfetchAll(cursor)[0]
                return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':row}, status=status.HTTP_200_OK)
        else:
          return JsonResponse({'status': False, 'msg': 'Tutor not valid', 'error':'INVALID_TUTOR'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_service_slots(request):
  with connection.cursor() as cursor:
    t_id =request.POST['t_id']
    service_id =request.POST['service_id']
    schedule =request.POST['schedule']

    data = json.loads(schedule)
    print(type(data))
    print(data)

    count = cursor.execute("SELECT * FROM `tutor` WHERE id = %s", [t_id])
    if(count>0):
      result = cursor.execute("SELECT * FROM `services` WHERE id = %s and t_id = %s", [service_id,t_id])
      if(result>0):
        # print("data")
        for daySchedule in data:
          # print (daySchedule["day_id"])
          cursor.execute("INSERT INTO `schedule`(day_id,service_id) VALUES (%s,%s)",[daySchedule["day_id"],service_id])
          schedule_id = cursor.lastrowid

          for slot in daySchedule['slots']:
            # print(slot["href"])
            cursor.execute("INSERT INTO `slots`(t_id,service_id,schedule_id,start_time,duration,class_type) VALUES (%s,%s,%s,%s,%s,%s)",[t_id,service_id,schedule_id,slot["start_time"],slot["duration"],slot["class_type"]]) 
        return JsonResponse({'status': True, 'msg': 'Slot Booking  Successfully'}, status=status.HTTP_200_OK)  
      else:
        return JsonResponse({'status': False, 'msg': 'Servces not valid', 'error':'INVALID_SERVICES'}, status=status.HTTP_200_OK)
    else:
      return JsonResponse({'status': False, 'msg': 'Tutor not valid', 'error':'INVALID_TUTOR'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_tutor_service(request):
  with connection.cursor() as cursor:
    id = request.GET['id']
    count = cursor.execute("SELECT `services`.*, `class`.`name` AS `class`, `subject`.`name` AS `subject` FROM `services` INNER JOIN `class` ON `services`.`c_id` = `class`.`id` INNER JOIN `subject` ON `services`.`s_id` = `subject`.`id` WHERE `services`.`t_id`=%s AND `services`.`status`='active'",[id])
    if(count>0):
      row = dictfetchAll(cursor)
      return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data': row}, status=status.HTTP_200_OK)
    else:
      return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':[]}, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_tutor_slot(request):
  with connection.cursor() as cursor:
    t_id = request.POST['t_id']
    service_id =request.POST['service_id']
    schedule_id =request.POST['schedule_id']
    start_time =request.POST['start_time']
    end_time =request.POST['end_time']
    duration =request.POST['duration']
    class_type =request.POST['class_type']
    day_id=request.POST['day_id']
    
    # tutor_id(t_id)
    count = cursor.execute("SELECT * FROM `tutor` WHERE id = %s", [t_id])
    if(count>0):
      if(check_slot(t_id, day_id, start_time, end_time)):
        count = cursor.execute("INSERT INTO `slots`(t_id,service_id,schedule_id,start_time,duration,class_type, day_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",[t_id,service_id,schedule_id,start_time,duration,class_type,day_id]) 
        if(count>0):
          id = cursor.lastrowid
          cursor.execute("SELECT * FROM `slots` WHERE id = %s", [id])
          row = dictfetchAll(cursor)
          return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data': row}, status=status.HTTP_200_OK)
        else:
          return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':[]}, status=status.HTTP_200_OK)
      else:
        return JsonResponse({'status': False, 'msg': 'Slot clashing with other slots'})
    else:
      return JsonResponse({'status': False, 'msg': 'Tutor not valid', 'error':'INVALID_TUTOR'}, status=status.HTTP_200_OK)
      
@api_view(['POST'])
def edit_tutor_slot(request):
  with connection.cursor() as cursor:
    try:
      id = request.POST['id']
      t_id = request.POST['t_id']
      service_id =request.POST['service_id']
      schedule_id =request.POST['schedule_id']
      slot_id =request.POST['slot_id']
      start_time =request.POST['start_time']
      duration =request.POST['duration']
      class_type =request.POST['class_type']


      if  t_id and service_id and schedule_id and slot_id and start_time and duration and class_type and id:
        sqlQuery = "UPDATE slots SET t_id=%s,service_id=%s,schedule_id=%s,id=%s,start_time=%s,duration=%s,class_type=%s WHERE id=%s"
        # print(name)
        data = (t_id,service_id,schedule_id,slot_id,start_time,duration,class_type, id)
        result = cursor.execute(sqlQuery, data)
        if (result>0):
          cursor.execute("SELECT * FROM `slots` where id =%s", [slot_id])
          row = dictfetchAll (cursor)
          return JsonResponse({'status': True, 'msg': 'Updated Successfully','data':row}, status=status.HTTP_200_OK)   
      else:
        return JsonResponse({'status': False, 'msg': 'Slot not update'}, status=status.HTTP_200_OK)
    except Exception as e:
      print(e)
      return JsonResponse({'status': False, 'msg': 'Slot not update here'}, status=status.HTTP_200_OK)
    finally:
      cursor.close() 

def check_slot(tutorId, dayId, newStartTime, newEndTime):
  with connection.cursor() as cursor:
    now = datetime.now()
    start = datetime.strptime(newStartTime, '%H:%M:%S')
    end = datetime.strptime(newEndTime, '%H:%M:%S')


    count = cursor.execute("SELECT * FROM `slots` WHERE t_id = %s and day_id = %s and status='active'", [tutorId, dayId])
    if (count>0):
      slots = dictfetchAll(cursor)
      for slot in slots:
        time = slot['start_time']
        slotStart = datetime(now.year, now.month, now.day, time.hour, time.minute, time.second)
        slotDuration = slot['duration']
        slotEnd = slotStart + datetime.timedelta(minutes=slotDuration)

        if(start.time()>slotStart.time()):
          if(start.time()<slotEnd.time()):
            return False
        else:
          if(end.time()>slotStart.time()):
            return False
      
      return True
    else:
      return True

    


# def my_function(type_personal):
#   if(type_personal == 'yes'):
#     result = "yes"
    
#     print(result)
# my_function()

# def tutor_id_valid(t_id):
#   with connection.cursor() as cursor:
#     t_id = request.POST['t_id']

#     count = cursor.execute("SELECT * FROM `tutor` WHERE id = %s", [t_id])
#     if(count>0):
#       return JsonResponse({'status': True, 'msg': 'Tutor valid'}, status=status.HTTP_200_OK)
#     else:
#       return JsonResponse({'status': False, 'msg': 'Tutor not valid', 'error':'INVALID_TUTOR'}, status=status.HTTP_200_OK)

