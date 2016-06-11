from django.contrib import admin
from .models import UserProfile, DeviceProfile,DeviceUsage


# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user','user_timezone')
admin.site.register(UserProfile, UserProfileAdmin)

class DeviceProfileAdmin(admin.ModelAdmin):
    list_display = ('owner','device_name','device_id','status_timer','status_manual','total_usage','openTime','closeTime')
admin.site.register(DeviceProfile, DeviceProfileAdmin)

class DeviceUsageAdmin(admin.ModelAdmin):
    list_display = ('device_id','usage','time','date')
admin.site.register(DeviceUsage, DeviceUsageAdmin)
