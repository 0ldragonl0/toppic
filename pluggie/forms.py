# -- coding: utf-8 --

from .models import DeviceProfile , UserProfile
from django.forms import ModelForm,forms
from django import forms
import datetime
from django.contrib.auth.models import User

class DeviceProfileForm(forms.ModelForm):
    owner = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),label='เจ้าของ ')
    device_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),label='ชื่ออุปกรณ์ ')
    openTime = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control'}),initial=datetime.datetime.now,label='เวลาเปิดอุปกรณ์ ')
    closeTime = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control'}),initial=(datetime.datetime.now),label='เวลาปิดอุปกรณ์ ')

    class Meta:
        model = DeviceProfile
        fields = ('owner','device_name','openTime','closeTime')

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),label='ชื่อจริง ')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),label='นามสกุล ')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}),label='อีเมล์ ')

    class Meta:
        model = User
        fields = ['first_name', 'last_name','email']
