from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Images
 
class CustomUserAdmin(UserAdmin):
    
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('authority','mail',)}),)
    list_display = ['username', 'mail', 'authority']

 
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Images)