from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
 
class CustomUserAdmin(UserAdmin):
    
    fieldsets = UserAdmin.fieldsets
    list_display = ['username']

 
admin.site.register(CustomUser, CustomUserAdmin)
