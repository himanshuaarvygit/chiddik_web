
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import AutoField, DateTimeField
from django.dispatch import receiver
from django.db.models.signals import post_save
from tinymce.models import HTMLField


# Create your models here.

class CustomUser(AbstractUser):
    user_type_data = ((1,"admin"),(2,"staff"),(3,"user"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=100)

class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

class User(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            Staff.objects.create(admin=instance)
        if instance.user_type==3:
            User.objects.create(admin=instance)
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.staff.save()
    if instance.user_type==3:
        instance.user.save()

class Pages(models.Model):
    id = models.IntegerField(primary_key=True)
    terms_condition_tutor = models.TextField()
    privacy_policy_tutor = models.TextField()
    terms_condition_stud = models.TextField()
    privacy_policy_stud = models.TextField()
    about_us = models.TextField()
    status = models.TextField()
    created_at = models.DateField()
    updated_at = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pages'

class Class(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    status = models.TextField()
    created_at = models.DateField()
    updated_at = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'class'

class Subject(models.Model):
    id = models.IntegerField(primary_key=True)
    c_id = models.TextField()
    name = models.TextField()
    status = models.TextField()
    created_at = models.DateField()
    updated_at = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subject'



