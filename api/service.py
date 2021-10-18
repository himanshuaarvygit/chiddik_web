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
from api.tutor import check_valid_tutor

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
        
        if not check_valid_tutor(t_id):
          return JsonResponse({'status': False, 'msg': 'Tutor Not Valid.', 'error': 'INVALID_TUTOR'}, status=status.HTTP_200_OK)
        
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
              cursor.execute("INSERT INTO `subject_request`(t_id,c_id,name,is_cid_active) VALUES (%s,%s,%s,%s)",[t_id,c_id,s_other,int(is_cid_active)])
              sr_id = cursor.lastrowid
 
              if(type_personal == 'yes' and type_group == 'yes'):
                result = cursor.execute("INSERT INTO `services`(t_id,c_id,s_id,type_personal,type_group,personal_price,group_price,c_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",[t_id,c_id,sr_id,type_personal,type_group,personal_price,group_price,'active'])
                if (result>0):
                  id = cursor.lastrowid
                  cursor.execute("SELECT * FROM `services` WHERE id = %s", [id])
                  row = dictfetchAll(cursor)[0]
                  return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':row}, status=status.HTTP_200_OK)
                else:
                  return JsonResponse({'status': False, 'msg': 'Error Occurred! Please try again!','error': 'ERROR'}, status=status.HTTP_200_OK)    
              elif(type_personal == 'yes'):
                result = cursor.execute("INSERT INTO `services`(t_id,c_id,s_id,type_personal,type_group,personal_price,group_price,c_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",[t_id,c_id,sr_id,type_personal,type_group,personal_price,group_price,'active'])
                if (result>0):
                  id = cursor.lastrowid
                  cursor.execute("SELECT * FROM `services` WHERE id = %s", [id])
                  row = dictfetchAll(cursor)[0]
                  return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':row}, status=status.HTTP_200_OK)
                else:
                  return JsonResponse({'status': False, 'msg': 'Error Occurred! Please try again!','error': 'ERROR'}, status=status.HTTP_200_OK)          
              elif(type_group == 'yes'):
                result = cursor.execute("INSERT INTO `services`(t_id,c_id,s_id,type_personal,type_group,personal_price,group_price,c_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",[t_id,c_id,sr_id,type_personal,type_group,personal_price,group_price,'active'])
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
            cursor.execute("INSERT INTO `slots`(t_id,service_id,schedule_id,start_time,duration,class_type, day_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",[t_id,service_id,schedule_id,slot["start_time"],slot["duration"],slot["class_type"],daySchedule["day_id"]]) 
        return JsonResponse({'status': True, 'msg': 'Slot Booking  Successfully'}, status=status.HTTP_200_OK)  
      else:
        return JsonResponse({'status': False, 'msg': 'Servces not valid', 'error':'INVALID_SERVICES'}, status=status.HTTP_200_OK)
    else:
      return JsonResponse({'status': False, 'msg': 'Tutor not valid', 'error':'INVALID_TUTOR'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_tutor_services(request):
  with connection.cursor() as cursor:
    id = request.GET['id']
    count = cursor.execute("SELECT `services`.*, `class`.`name` AS `class`, `subject`.`name` AS `subject` FROM `services` INNER JOIN `class` ON `services`.`c_id` = `class`.`id` INNER JOIN `subject` ON `services`.`s_id` = `subject`.`id` WHERE `services`.`t_id`=%s AND `services`.`status`='active'",[id])
    if(count>0):
      row = dictfetchAll(cursor)
      return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data': row}, status=status.HTTP_200_OK)
    else:
      return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':[]}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_tutor_service(request):
  with connection.cursor() as cursor:
    try:
      id = request.GET['id']
      serviceId = request.GET['service_id']
      
      count = cursor.execute("SELECT `services`.*, `class`.`name` AS `class`, `subject`.`name` AS `subject` FROM `services` INNER JOIN `class` ON `services`.`c_id` = `class`.`id` INNER JOIN `subject` ON `services`.`s_id` = `subject`.`id` WHERE `services`.`t_id`=%s AND `services`.`id`=%s AND `services`.`status`='active'",[id,serviceId])

      row = dictfetchAll(cursor)
      if(len(row)>=1):
        data = row[0]
        return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data': data}, status=status.HTTP_200_OK)
      else:
        return JsonResponse({'status': False, 'msg': 'Fetched Successfully','data':[]}, status=status.HTTP_200_OK)
    except Exception as e:
      return JsonResponse({'status': False, 'msg': 'Error fetching data', 'error':f'{e}'}, status=status.HTTP_200_OK)
    finally:
      cursor.close()

@api_view(['POST'])
def update_service(request):
  with connection.cursor() as cursor:
    try:
      tutorId = request.POST['t_id']
      serviceId = request.POST['service_id']
      type_personal = request.POST['type_personal']
      type_group = request.POST['type_group']
      personal_price = request.POST['personal_price']
      group_price = request.POST['group_price']

      if not check_valid_tutor(tutorId):
        return JsonResponse({'status': False, 'msg': 'Tutor Not Valid.', 'error': 'INVALID_TUTOR'}, status=status.HTTP_200_OK)

      if not check_valid_service(tutorId, serviceId):
        return JsonResponse({'status': False, 'msg': 'Service Not Valid.', 'error': 'INVALID_SERVICE'}, status=status.HTTP_200_OK)
      
      sql = "UPDATE `services` SET `type_personal`=%s,`type_group`=%s,`personal_price`=%s,`group_price`=%s,`updated`=%s WHERE `id`=%s and `t_id`=%s"
      sqlData = [type_personal, type_group, personal_price, group_price, serviceId, tutorId]

      updateService = cursor.execute(sql, sqlData)

      if updateService>0:
        return JsonResponse({'status':True, 'msg': 'Updated Successfully'}, status = status.HTTP_200_OK)
      else:
        return JsonResponse({'status': False, 'msg': 'Error'}, status=status.HTTP_200_OK)

    except Exception as e:
      return JsonResponse({'status': False, 'msg': 'Error'}, status=status.HTTP_200_OK)
    finally:
      cursor.close()

@api_view(['GET'])
def get_service_schedule(request):
  with connection.cursor() as cursor:
    try:
      id = request.GET['id']
      serviceId = request.GET['service_id']
      
      cursor.execute("SELECT `schedule`.*, `day`.`day` as `day_name` FROM `schedule` LEFT JOIN `day` ON `schedule`.`day_id`=`day`.`id` WHERE `schedule`.`service_id`=%s AND `schedule`.`status`='active'",[serviceId])
      schedule = dictfetchAll(cursor)
      if len(schedule)>0:
        result = []
        for day in schedule:
          res = day
          # print(day['id'])
          cursor.execute("SELECT * FROM `slots` WHERE `t_id`=%s and `service_id`=%s and `schedule_id`=%s and `status`='active'",[id,serviceId,day['id']])
          slots = dictfetchAll(cursor)
          # print(slots)
          res['slots']=slots
          result.append(res)
        return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data': result}, status=status.HTTP_200_OK)
      else:
        return JsonResponse({'status': True, 'msg': 'Fetched Successfully','data':[]}, status=status.HTTP_200_OK)
    except Exception as e:
      return JsonResponse({'status': False, 'msg': 'Error fetching data', 'error':f'{e}'}, status=status.HTTP_200_OK)
    finally:
      cursor.close()

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
    
    if not check_valid_tutor(t_id):
        return JsonResponse({'status': False, 'msg': 'Tutor Not Valid.', 'error': 'INVALID_TUTOR'}, status=status.HTTP_200_OK)
    
    if not check_valid_service(t_id, service_id):
      return JsonResponse({'status': False, 'msg': 'Service Not Valid.', 'error': 'INVALID_SERVICE'}, status=status.HTTP_200_OK)
    
    if not check_slot(t_id, day_id, start_time, end_time):
      return JsonResponse({'status': False, 'msg': 'Slot clashing with other slots'})

    count = cursor.execute("INSERT INTO `slots`(t_id,service_id,schedule_id,start_time,duration,class_type, day_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",[t_id,service_id,schedule_id,start_time,duration,class_type,day_id]) 
    if(count>0):
      id = cursor.lastrowid
      # cursor.execute("SELECT * FROM `slots` WHERE id = %s", [id])
      # row = dictfetchAll(cursor)
      return JsonResponse({'status': True, 'msg': 'Fetched Successfully', 'slot_id': cursor.lastrowid}, status=status.HTTP_200_OK)
    else:
      return JsonResponse({'status': False, 'msg': 'Slot not added.','data':[]}, status=status.HTTP_200_OK)
      
@api_view(['POST'])
def remove_tutor_slot(request):
  with connection.cursor() as cursor:
    try:
      tutorId = request.POST['t_id']
      slotId = request.POST['slot_id']

      if not check_valid_tutor(tutorId):
        return JsonResponse({'status': False, 'msg': 'Tutor Not Valid.', 'error': 'INVALID_TUTOR'}, status=status.HTTP_200_OK)
      
      result = cursor.execute("UPDATE `slots` SET status = 'inactive' WHERE `id`=%s AND `t_id`=%s", [slotId, tutorId])
      if(result > 0):
        return JsonResponse({'status': True, 'msg': 'Slot removed'}, status=status.HTTP_200_OK) 
      else:
        return JsonResponse({'status': False, 'msg':'Slot not removed',}, status=status.HTTP_200_OK)
    except Exception as e:
      print(e)
      return JsonResponse({'status': False, 'msg': 'Slot not removed here', 'error': f'{e}'}, status=status.HTTP_200_OK) 
    finally:
      cursor.close()
      
@api_view(['POST'])
def edit_tutor_slot(request):
  with connection.cursor() as cursor:
    try:
      t_id = request.POST['t_id']
      service_id =request.POST['service_id']
      slot_id =request.POST['slot_id']
      start_time =request.POST['start_time']
      end_time =request.POST['end_time']
      duration =request.POST['duration']
      dayId = request.POST['day_id']
      class_type =request.POST['class_type']

      if not check_valid_tutor(t_id):
        return JsonResponse({'status': False, 'msg': 'Tutor Not Valid.', 'error': 'INVALID_TUTOR'}, status=status.HTTP_200_OK)
      
      if not check_valid_service(t_id, service_id):
        return JsonResponse({'status': False, 'msg': 'Service Not Valid.', 'error': 'INVALID_SERVICE'}, status=status.HTTP_200_OK)

      if slot_id and start_time and duration and class_type:
        if check_slot(t_id, dayId, start_time, end_time, slot_id):
          sqlQuery = "UPDATE slots SET start_time=%s,duration=%s,class_type=%s WHERE id=%s"
          data = (start_time, duration, class_type, slot_id)
          result = cursor.execute(sqlQuery, data)
          if (result>0):
            return JsonResponse({'status': True, 'msg': 'Updated Successfully'}, status=status.HTTP_200_OK)  
        else:
          return JsonResponse({'status': False, 'msg': 'Slot clashing with other slots'}, status=status.HTTP_200_OK)
         
      else:
        return JsonResponse({'status': False, 'msg': 'Slot not update'}, status=status.HTTP_200_OK)
      
    except Exception as e:
      print(e)
      return JsonResponse({'status': False, 'msg': 'Slot not update here'}, status=status.HTTP_200_OK)
    finally:
      cursor.close() 

@api_view(['POST'])
def add_schedule(request):
  with connection.cursor() as cursor:
    try:
      tutorId = request.POST['t_id']
      serviceId = request.POST['service_id']
      dayId = request.POST['day_id']

      if not check_valid_tutor(tutorId):
        return JsonResponse({'status': False, 'msg': 'Tutor Not Valid.', 'error': 'INVALID_TUTOR'}, status=status.HTTP_200_OK)
      
      if check_schedule(serviceId, dayId):
        return JsonResponse({'status': False, 'msg': 'Schedule Already Available.', 'error': 'SCHEDULE_ALREADY_AVAILABLE'}, status=status.HTTP_200_OK)
      
      addSchedule = cursor.execute("INSERT INTO `schedule`(day_id,service_id) VALUES (%s,%s)",[dayId, serviceId])
      if addSchedule>0:
        return JsonResponse({'status': True, 'msg':'Schedule added successfully', 'schedule_id': cursor.lastrowid}, status=status.HTTP_200_OK)
      else:
        return JsonResponse({'status': False, 'msg':'Error added schedule'}, status=status.HTTP_200_OK)

    except Exception as e:
      return JsonResponse({'status': False, 'msg':'Error added schedule', 'error': f'{e}'}, status=status.HTTP_200_OK)
    finally:
      cursor.close()

@api_view(['POST'])
def remove_schedule(request):
  with connection.cursor() as cursor:
    try:
      tutorId = request.POST['t_id']
      scheduleId = request.POST['schedule_id']

      if not check_valid_tutor(tutorId):
        return JsonResponse({'status': False, 'msg': 'Tutor Not Valid.', 'error': 'INVALID_TUTOR'}, status=status.HTTP_200_OK)
      
      removeSchedule = cursor.execute("UPDATE `schedule` SET `status`='inactive' WHERE `id`=%s",[scheduleId])
      if removeSchedule>0:
        removeSlots = cursor.execute("UPDATE `slots` SET `status`='inactive' WHERE `t_id`=%s AND `schedule_id`=%s",[tutorId, scheduleId])
        if removeSlots>0:
          return JsonResponse({'status': True, 'msg':'Schedule removed successfully'}, status=status.HTTP_200_OK)
        else:
          return JsonResponse({'status': False, 'msg':'Error removing schedule'}, status=status.HTTP_200_OK)
      else:
        return JsonResponse({'status': False, 'msg':'Error removing schedule'}, status=status.HTTP_200_OK)

    except Exception as e:
      return JsonResponse({'status': False, 'msg':'Error removing schedule', 'error': f'{e}'}, status=status.HTTP_200_OK)
    finally:
      cursor.close()

def check_valid_service(tutorId, serviceId):
  with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM `services` where id = %s AND t_id = %s AND status='active'", [serviceId, tutorId])
    row = dictfetchAll(cursor)
    if(len(row)>0):
      return True
    else:
      return False

def check_schedule(serviceId, dayId):
  with connection.cursor() as cursor:
    sql = ""
    sqlData = []

    sql = "SELECT * FROM `schedule` WHERE service_id = %s and day_id = %s and status='active'"
    sqlData = [serviceId, dayId]

    count = cursor.execute(sql, sqlData)
    if (count>0):
      return True
    else:
      return False

def check_slot(tutorId, dayId, newStartTime, newEndTime, slotId=0):
  with connection.cursor() as cursor:
    now = datetime.now()
    start = datetime.strptime(newStartTime, '%H:%M:%S')
    end = datetime.strptime(newEndTime, '%H:%M:%S')

    sql = ""
    sqlData = []
    if slotId==0:
      sql = "SELECT * FROM `slots` WHERE t_id = %s and day_id = %s and status='active'"
      sqlData = [tutorId, dayId]
    else:
      sql = "SELECT * FROM `slots` WHERE t_id = %s and day_id = %s and id!=%s and status='active'"
      sqlData = [tutorId, dayId, slotId]

    count = cursor.execute(sql, sqlData)
    if (count>0):
      slots = dictfetchAll(cursor)
      for slot in slots:
        time = slot['start_time']
        slotStart = datetime(now.year, now.month, now.day, time.hour, time.minute, time.second)
        slotDuration = int(slot['duration'])
        slotEnd = slotStart + timedelta(minutes=slotDuration)

        if(start.time()>slotStart.time()):
          if(start.time()<slotEnd.time()):
            return False
        else:
          if(end.time()>slotStart.time()):
            return False
      
      return True
    else:
      return True

    