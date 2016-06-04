from django.contrib import admin
from .models import UserProfile, DeviceProfile,DeviceUsage


# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user','user_timezone')
admin.site.register(UserProfile, UserProfileAdmin)

class DeviceProfileAdmin(admin.ModelAdmin):
    list_display = ('id','owner','device_name','total_usage','openTime','closeTime')
admin.site.register(DeviceProfile, DeviceProfileAdmin)

class DeviceUsageAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_id','usage','date_time')
admin.site.register(DeviceUsage, DeviceUsageAdmin)
