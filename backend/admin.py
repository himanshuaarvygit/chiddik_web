from django.contrib.admin.options import ModelAdmin
from backend.models import CustomUser, Pages
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserModel)

# @admin.register(Pages)
# class PagesAdmin(admin.ModelAdmin):
#     class Media:
#         js = ('js/tiny.js')

