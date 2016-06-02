# -- coding: utf-8 --
from django.contrib.auth.models import User
from django.forms import ModelForm,forms
from django import forms

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),label='ชื่อผู้ใช้ ')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),label='รหัสผ่าน ')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),label='ชื่อจริง ')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),label='นามสกุล ')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}),label='อีเมล์ ')

    class Meta:
        model = User
        fields = ['username', 'password', 'email','first_name','last_name']
        help_texts = {
            'username': str('Required. 30 characters or fewer. Usernames may contain alphanumeric, _, @, +, . and - characters.<br><br>'),
            'password': str('<br>'),
            'email': str('<br>'),
            'first_name': str('<br>'),
            'last_name' : str('<br>'),
        }
