# -- coding: utf-8 --

from .models import DeviceProfile , UserProfile
from django.forms import ModelForm,forms
from django import forms
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.forms.widgets import HiddenInput


class DeviceProfileForm(forms.ModelForm):
    owner = forms.ModelChoiceField(queryset=User.objects.all(),widget=forms.HiddenInput(),label='เจ้าของ ')
    device_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}),label='รหัสระจำตัวอุปกรณ์ ')
    device_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),label='ชื่ออุปกรณ์ ')
    openTime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control'}),initial=(timezone.make_aware(datetime.datetime.now(),timezone.get_default_timezone())),label='เวลาเปิดอุปกรณ์ ',required=False)
    closeTime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control'}),initial=(timezone.make_aware(datetime.datetime.now(),timezone.get_default_timezone())),label='เวลาปิดอุปกรณ์ ',required=False)

    class Meta:
        model = DeviceProfile
        fields = ('owner','device_id','device_name','openTime','closeTime')


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),label='ชื่อจริง ')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),label='นามสกุล ')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}),label='อีเมล์ ')

    class Meta:
        model = User
        fields = ['first_name', 'last_name','email']

class EditDeviceForm(forms.ModelForm):
    device_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),label='ชื่ออุปกรณ์ ')
    openTime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control'}),initial=(timezone.make_aware(datetime.datetime.now(),timezone.get_default_timezone())),label='เวลาเปิดอุปกรณ์ ',required=False)
    closeTime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control'}),initial=(timezone.make_aware(datetime.datetime.now(),timezone.get_default_timezone())),label='เวลาปิดอุปกรณ์ ',required=False)
    class Meta:
        model = DeviceProfile
        fields = ('device_name','openTime','closeTime')
