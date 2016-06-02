from django.http import HttpResponse , JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import DeviceProfile , UserProfile
import datetime
from django.utils import timezone
import pytz
from django.utils import formats
from django.template import RequestContext
from forms import DeviceProfileForm , EditProfileForm
#import for graph
from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components

def home(request):
    now = datetime.datetime.now()
    now = formats.date_format(now,"SHORT_DATETIME_FORMAT")
    #html = "<html><body>It is now %s.</body></html>" % now
    #return HttpResponse(request.session['django_timezone'])
    return render(request, 'home.html',{"date":str(now)})

def output(request):
   x = request.GET.get('user', '')
   return HttpResponse(x)

def adddevice(request):
    now = datetime.datetime.now()
    now = formats.date_format(now,"SHORT_DATETIME_FORMAT")
    if request.POST.get('adddevice'):
        form = DeviceProfileForm(request.POST)
        if form.is_valid():
            new_deviceprofile = DeviceProfile.objects.create(**form.cleaned_data)
            new_deviceprofile.save()
            return redirect('/deviceprofile/')
    elif request.POST.get('canceladddevice'):
        return redirect('/deviceprofile/')
    else:
        form = DeviceProfileForm(initial={'owner':request.user})
        form.fields['owner'].widget.attrs['readonly'] = 'True'
    return render(request, 'deviceprofile_add.html', {'form': form,"date":str(now)})

def editdevice(request,id):
    now = datetime.datetime.now()
    now = formats.date_format(now,"SHORT_DATETIME_FORMAT")
    data = DeviceProfile.objects.get(pk=id)
    if request.POST.get('updatedevice'):
        #request.POST.owner = request.user
        form = DeviceProfileForm(request.POST)
        if form.is_valid():
            DeviceProfile.objects.filter(pk=id).update(**form.cleaned_data)
            return redirect('/deviceprofile/')
    elif request.POST.get('cancelupdatedevice'):
            return redirect('/deviceprofile/')
    else:
        form = DeviceProfileForm(initial={'owner':request.user})
        dv = {'owner':data.owner,'device_name':data.device_name,'usage':data.usage,'openTime':data.openTime,'closeTime':data.closeTime}
        form = DeviceProfileForm(dv)
        form.fields['owner'].widget.attrs['readonly'] = 'True'
    return render(request, 'deviceprofile_edit.html', {'form': form,"date":str(now)})
<<<<<<< HEAD

def deletedevice(request,id):
    now = datetime.datetime.now()
    now = formats.date_format(now,"SHORT_DATETIME_FORMAT")
    DeviceProfile.objects.filter(id=id).delete()
=======

def deletedevice(request,id):
    now = datetime.datetime.now()
    now = formats.date_format(now,"SHORT_DATETIME_FORMAT")

    DeviceProfile.objects.filter(id__in=id).delete()
>>>>>>> origin/master
    return redirect('/deviceprofile/',{"date":str(now)})
#request.session['user_username']
def devicedetail(request):
    #print(request.user)
    #print(DeviceProfile.objects.filter(owner=request.user).count())
    dv = {i.device_name: {'usage':i.usage,'open time': i.openTime,'close time': i.closeTime,} for i in DeviceProfile.objects.filter(owner=request.user)}
    return JsonResponse(dv,safe=False)

def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')
    else:
        return render(request, 'template.html', {'timezones': pytz.common_timezones})

def UserProfilePage(request):
    now = datetime.datetime.now()
    now = formats.date_format(now,"SHORT_DATETIME_FORMAT")
    return render(request, 'userprofile.html',{'users':User.objects.filter(username =request.user),'profiles':UserProfile.objects.filter(user = request.user),"date":str(now)})

def edit_profile(request,id):
    now = datetime.datetime.now()
    now = formats.date_format(now,"SHORT_DATETIME_FORMAT")
    data = User.objects.get(pk=id)
    if request.POST.get('updateuser'):
        user = request.user
        time = request.POST['timezone']
        form = EditProfileForm(request.POST)
        time_user = UserProfile.objects.filter(pk=id).update(user_timezone=time)
        request.session['django_timezone'] = request.POST['timezone']
        if form.is_valid():
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()

            return redirect('/userprofile/')
    elif request.POST.get('canceledituser'):
            return redirect('/userprofile/')
    else:
        form = EditProfileForm()
        dv = {'first_name':data.first_name,'last_name':data.last_name,'email':data.email}
        form = EditProfileForm(dv)
    return render(request, 'userprofile_edit.html', {'form':form,'timezones':pytz.common_timezones,"date":str(now)})

def Device(request):
    now = datetime.datetime.now()
    now = formats.date_format(now,"SHORT_DATETIME_FORMAT")
    return render(request, 'deviceprofile.html',{'devices': DeviceProfile.objects.filter(owner=request.user),"date":str(now)})
        #return render(request, 'deviceprofile_edit.html', {'form': form,"date":str(now)})

def ChooseGraph(request):
    now = datetime.datetime.now()
    now = formats.date_format(now,"SHORT_DATETIME_FORMAT")
    return render(request,'choosegraph.html',{"date":str(now)})

def MonthGraph(request):
    return render(request, "simple_chart.html")

def usage_data(request):
    myfile1={
    "usage": [
        {
            "id" : 1,
            "device_id": 0,
            "usage" : 93.24,
            "datetime": 24-Apr-07
        },
        {
            "id" : 1,
            "device_id": 0,
            "usage" : 95.35,
            "datetime": 25-Apr-07
        },
        ]
    }
