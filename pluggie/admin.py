from django.contrib import admin
from .models import UserProfile
from .models import DeviceProfile


# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user','user_timezone')
admin.site.register(UserProfile, UserProfileAdmin)

class DeviceProfileAdmin(admin.ModelAdmin):
    list_display = ('id','owner','device_name','usage','openTime','closeTime')
admin.site.register(DeviceProfile, DeviceProfileAdmin)
