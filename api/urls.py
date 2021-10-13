
from django.contrib import admin
from django.urls import path
from  api import views, tutor, student, service

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('tutor_details/', tutor.tutor_details),
    path('tutor_validate/', tutor.tutor_validate),
    path('tutor_register/', tutor.tutor_register),
    path('tutor_edit_details/', tutor.tutor_edit_details),

    path('student_details/', student.student_details),
    path('student_validate/', student.student_validate),
    path('student_register/', student.student_register),
    path('student_edit_details/', student.student_edit_details),

    path('add_tutor_service/', service.add_tutor_service),
    path('add_service_slots/', service.add_service_slots),
    path('get_tutor_services/', service.get_tutor_services),
    path('get_tutor_service/', service.get_tutor_service),
    path('get_service_schedule/', service.get_service_schedule),
    path('add_tutor_slot/', service.add_tutor_slot),
    path('check_slot/', service.check_slot),
    path('edit_tutor_slot/', service.edit_tutor_slot),
    path('disable_tutor_slot/', service.disable_tutor_slot),
    path('remove_schedule/', service.remove_schedule),

    path('get_all_classes/', views.get_all_classes),
    path('get_all_subject/', views.get_all_subject),
    path('terms_and_condition/', views.terms_and_condition),
    path('get_all_day/', views.get_all_day),
    path('get_banner/', views.get_banner),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)