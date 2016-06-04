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
    owner = models.CharField(max_length=30)
    device_name = models.CharField(max_length=30)
    total_usage = models.FloatField(max_length=20,default='0')
    openTime = models.TimeField('time to open device')
    #openTime = models.DateTimeField('time to open device',auto_now_add=True) <- timestamp
    closeTime = models.TimeField('time to close device')
    def __str__(self):
        return self.device_name

class DeviceUsage(models.Model):
    device_id = models.BigIntegerField(max_length=10)
    usage = models.FloatField(max_length=20)
    date_time = models.DateTimeField()
    def __str__(self):
        return str(self.device_id)
