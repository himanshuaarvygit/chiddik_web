# Generated by Django 3.2.7 on 2021-09-28 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_alter_subject_cls_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='class',
            old_name='name',
            new_name='cname',
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='name',
            new_name='sname',
        ),
    ]
