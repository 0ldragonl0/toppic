from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max

# Create your models here.
def number():
        no = UserProfile.objects.aggregate(Max('ID'))
        if no['ID__max'] == None:
            return 1
        else:
            return no['ID__max'] + 1



class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_timezone = models.CharField(max_length=20,help_text="Please use the following format: UTC.")
    def __str__(self):
        return str(self.user)

class DeviceProfile(models.Model):
    owner = models.ForeignKey(User)
    device_id = models.CharField(max_length=20,primary_key=True, unique=True)
    device_name = models.CharField(max_length=30)
    status_timer = models.CharField(max_length=5,default='0')
    status_manual = models.CharField(max_length=5,default='0')
    total_usage = models.FloatField(max_length=20,default='0')
    openTime = models.DateTimeField('time to open device')
    #openTime = models.DateTimeField('time to open device',auto_now_add=True) <- timestamp
    closeTime = models.DateTimeField('time to close device')
    def __str__(self):
        return self.device_id

class DeviceUsage(models.Model):
    device_id = models.ForeignKey(DeviceProfile)
    usage = models.FloatField(max_length=20)
    time = models.IntegerField(max_length=5)
    date = models.DateTimeField(auto_now=False)
    def __str__(self):
         return str(self.device_id)
