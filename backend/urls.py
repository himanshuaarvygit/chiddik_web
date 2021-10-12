
from django.contrib import admin
from django.urls import path
from backend import views

urlpatterns = [
    
    # url(r'^backend/', views.index, name='index'),
    # url(r'^web/category', views.add_category, name='category'),

    path('', views.showlogin, name='showlogin'),
    path('login1', views.login1, name='login1'),
    path('logout_admin', views.logout_admin, name='logout_admin'),
    
    path('dashboard', views.dashboard, name='dashboard'),
    path('terms_condition_tutor/<int:id>/', views.terms_condition_tutor, name='terms_condition_tutor'),
    path('privacy_policy_tutor/<int:id>/', views.privacy_policy_tutor, name='privacy_policy_tutor'),
    path('terms_condition_stud/<int:id>/', views.terms_condition_stud, name='terms_condition_stud'),
    path('privacy_policy_stud/<int:id>/', views.privacy_policy_stud, name='privacy_policy_stud'),
    path('about_us/<int:id>/', views.about_us, name='about_us'),
    
    path('add_class', views.add_class, name='add_class'),
    path('list_class', views.list_class, name='list_class'),
    path('edit_class/<int:id>/', views.edit_class, name='edit_class'),
    path('delete_class/<int:id>/', views.delete_class, name='delete_class'),

    path('add_subject', views.add_subject, name='add_subject'),
    path('list_subject', views.list_subject, name='list_subject'),
    path('edit_subject/<int:id>/', views.edit_subject, name='edit_subject'),
    path('delete_subject/<int:id>/', views.delete_subject, name='delete_subject'),

]