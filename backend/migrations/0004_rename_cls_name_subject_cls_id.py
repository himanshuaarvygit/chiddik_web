# Generated by Django 3.2.7 on 2021-09-27 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_subject'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='cls_name',
            new_name='cls_id',
        ),
    ]