# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class BackendAdminhod(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    admin = models.OneToOneField('BackendCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'backend_adminhod'


class BackendCustomuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    user_type = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'backend_customuser'


class BackendCustomuserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(BackendCustomuser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'backend_customuser_groups'
        unique_together = (('customuser', 'group'),)


class BackendCustomuserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(BackendCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'backend_customuser_user_permissions'
        unique_together = (('customuser', 'permission'),)


class BackendStaff(models.Model):
    address = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    admin = models.OneToOneField(BackendCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'backend_staff'


class BackendUser(models.Model):
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    admin = models.OneToOneField(BackendCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'backend_user'


class Chat(models.Model):
    t_id = models.TextField()
    s_id = models.TextField()
    sender = models.CharField(max_length=7)
    date = models.TextField()
    time = models.TextField()
    message = models.TextField()
    message_type = models.TextField()
    status = models.CharField(max_length=7)

    class Meta:
        managed = False
        db_table = 'chat'


class Class(models.Model):
    name = models.TextField()
    status = models.TextField()
    created_at = models.DateField(blank=True, null=True)
    updated_at = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'class'


class ClassRequest(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    status = models.TextField()
    t_id = models.TextField()

    class Meta:
        managed = False
        db_table = 'class_request'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(BackendCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Pages(models.Model):
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


class Schedule(models.Model):
    id = models.IntegerField(primary_key=True)
    s_id = models.TextField()
    day_id = models.TextField()
    date_time = models.TextField()
    status = models.TextField()

    class Meta:
        managed = False
        db_table = 'schedule'


class Services(models.Model):
    c_id = models.TextField()
    s_id = models.TextField()
    type_personal = models.TextField()
    type_group = models.TextField()
    personal_price = models.TextField()
    group_price = models.TextField()
    t_id = models.TextField()
    status = models.TextField()
    created = models.DateField()
    updated = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'services'


class Slots(models.Model):
    id = models.IntegerField(primary_key=True)
    s_id = models.TextField()
    s_c_id = models.TextField()
    start_time = models.TextField()
    duration = models.TextField()
    class_type = models.CharField(max_length=8)
    status = models.TextField()

    class Meta:
        managed = False
        db_table = 'slots'


class Subject(models.Model):
    c_id = models.TextField()
    name = models.TextField()
    status = models.TextField()
    created_at = models.DateField(blank=True, null=True)
    updated_at = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subject'


class SubjectRequest(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    status = models.TextField()
    t_id = models.TextField()
    c_id = models.TextField()

    class Meta:
        managed = False
        db_table = 'subject_request'


class Tutor(models.Model):
    name = models.TextField()
    email = models.TextField()
    phone = models.TextField()
    id_prove = models.TextField()
    education_cer = models.TextField()
    location = models.TextField()
    long_tb = models.TextField()
    lat_tb = models.TextField()
    pic = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=8)
    video_link = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    wallet = models.TextField()

    class Meta:
        managed = False
        db_table = 'tutor'
