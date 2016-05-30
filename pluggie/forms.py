from .models import DeviceProfile , UserProfile
from django.forms import ModelForm,forms
from django import forms
import datetime

class DeviceProfileForm(forms.ModelForm):
    openTime = forms.TimeField(initial=datetime.datetime.now)
    closeTime = forms.TimeField(initial=(datetime.datetime.now))

    class Meta:
        model = DeviceProfile
        fields = ('owner','device_name','usage','openTime','closeTime')
