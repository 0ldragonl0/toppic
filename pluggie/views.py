# -- coding: utf-8 --
from django.http import HttpResponse , JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import DeviceProfile , UserProfile,DeviceUsage
import datetime
from django.utils import timezone
import pytz
from django.utils import formats
from django.template import RequestContext
from forms import DeviceProfileForm , EditProfileForm,EditDeviceForm
from django.db.models import Sum,Count
#import for graph
from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import Range1d,HoverTool
from bokeh.charts import Bar , color, marker


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
    data = DeviceProfile.objects.get(device_id=id)

    if request.POST.get('updatedevice'):
        #request.POST.owner = request.user
        form = EditDeviceForm(request.POST)
        if form.is_valid():
            DeviceProfile.objects.filter(device_id=id).update(**form.cleaned_data)
            return redirect('/deviceprofile/')
    elif request.POST.get('cancelupdatedevice'):
            return redirect('/deviceprofile/')
    else:
        dv = {'device_name':data.device_name,'openTime':data.openTime,'closeTime':data.closeTime}
        form = EditDeviceForm(dv)
    return render(request, 'deviceprofile_edit.html', {'form': form,"date":str(now)})

def deletedevice(request,id):
    now = datetime.datetime.now()
    now = formats.date_format(now,"SHORT_DATETIME_FORMAT")

    DeviceProfile.objects.filter(device_id=id).delete()
    DeviceUsage.objects.filter(device_id=id).delete()
    return redirect('/deviceprofile/',{"date":str(now)})
#request.session['user_username']
def devicedetail(request):
    #print(request.user)
    #print(DeviceProfile.objects.filter(owner=request.user).count())
    #dv = {i.device_id: {'usage':i.usage,'time': i.date_time}for i in DeviceUsage.objects.filter(device_id=DeviceProfile.objects.filter(owner=request.user))}
    device =  DeviceProfile.objects.filter(owner=request.user)
    print device
    for du in device:
        dv = {i.device_id: {'usage':i.usage,'time': i.date_time}for i in DeviceUsage.objects.all()}
        return JsonResponse(dv,safe=False)
    return redirect('/')

def UserProfilePage(request):
    now = datetime.datetime.now()
    now = formats.date_format(now,"SHORT_DATETIME_FORMAT")
    return render(request, 'userprofile.html',{'users':User.objects.filter(username =request.user),'profiles':UserProfile.objects.filter(user = request.user),"date":str(now)})

def edit_profile(request,id):
    now =  timezone.make_aware(datetime.datetime.now(),timezone.get_default_timezone())
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
            user.email = request.POST['email']
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
    #dv = {i.devices_id: DeviceUsage.objects.filter(devices_id=i.id)}for i in DeviceProfile.objects.filter(owner=request.user)
    user_now = User.objects.get(username=request.user)
    device =  DeviceProfile.objects.filter(owner=user_now)
    #print device
    for d in device:
        du = DeviceUsage.objects.filter(device_id=d.device_id).aggregate(Sum('usage'))
        dt = DeviceUsage.objects.filter(device_id=d.device_id).aggregate(Sum('time'))
        #print du['usage__sum']
        total_u = du['usage__sum']
        total_t = dt['time__sum']
        #print total_u
        #print total_t
        if total_u is None:
            total_u = 0.0
        if total_t is None:
            total_t = 0.0

        total = float(total_u) * (float(total_t)/3600)
        #print total

        if total is None:
            DeviceProfile.objects.filter(device_id=d.device_id).update(total_usage=0.0)
        else:
            DeviceProfile.objects.filter(device_id=d.device_id).update(total_usage=total)
    return render(request, 'deviceprofile.html',{'devices': DeviceProfile.objects.filter(owner=request.user),"date":str(now)})
        #return render(request, 'deviceprofile_edit.html', {'form': form,"date":str(now)})


def ChooseGraph(request):
    now = datetime.datetime.now()
    now = formats.date_format(now,"SHORT_DATETIME_FORMAT")
    return render(request,'choosegraph.html',{"date":str(now)})

def RealtimeGraph(request):
    now = datetime.datetime.now()
    now = formats.date_format(now,"SHORT_DATETIME_FORMAT")

    x = [1, 2, 3, 4, 5,6,7,8,9,10,11,12,13,14,15
    ,16,17,18,19,20,21,22,23,24,25,26,27,28,29
    ,30,31]
    y = [1, 2, 3, 5, 3,8, 5, 3,8, 5, 3,8,8,1,
    2, 3, 5, 3,8, 5, 3,8, 5, 1, 2, 3, 5,
    3,8, 5, 3,8, 5, 3,8,8,3,8,8]

    plot = figure(plot_width=400, plot_height=400)

    # add both a line and circles on the same plot
    plot.line(x, y, line_width=2)

    script, div = components(plot, CDN)

    return render(request, "simple_chart2.html", {"the_script": script, "the_div": div,'devices': DeviceProfile.objects.filter(owner=request.user),"date":str(now)})



def MonthGraph(request):

    now = datetime.datetime.now()
    now = formats.date_format(now,"SHORT_DATETIME_FORMAT")

    #data = DeviceUsage.objects.values('date').annotate(sumusage=Sum('usage'))# Group by date
    y = [0,0,0,0,0,0,0,0,0,0
        ,0,0,0,0,0,0,0,0,0,0
        ,0,0,0,0,0,0,0,0,0,0,0,0]

    if request.POST.get('deviceid') is not None:
        id = request.POST.get('deviceid')
        if request.POST.get('month') is not None:
            month = request.POST.get('month')
            do = DeviceProfile.objects.get(device_id=id)
            data = DeviceUsage.objects.filter(device_id=do,date__month=month).values('date').annotate(sumusage=Sum('usage'))
            #print data # data[0].get('date').strftime("%d") get only date from year-month-date
            for d in data:
                y[int(d.get('date').strftime("%d"))] = d.get('sumusage')
            head = "usage of device name: "+ do.device_name +" at "+request.POST.get('month')+"th Month"
    else:
        print "Don't select data"
        head=""

    plot = Bar(y,title=head, xlabel='date', ylabel='Unit', width=800, height=400)
    plot.toolbar_location = None
    plot.outline_line_color = None

    script, div = components(plot, CDN)

    return render(request, "monthgraph.html", {"the_script": script, "the_div": div,'devices': DeviceProfile.objects.filter(owner=request.user),"date":str(now)})

def updateusage(request,id,num):
    #use = DeviceProfile.objects.get(pk=id).usage + int(num.encode('ascii'))
    now =  timezone.make_aware(datetime.datetime.now(),timezone.get_default_timezone())
    print now
    usage_num = float(num)

    data = DeviceProfile.objects.get(device_id=id)
    use = DeviceUsage.objects.create(device_id=data,usage=usage_num,time =3,date=now)
    use.save()

    # if data.openTime >= now <= data.closeTime:
    #     print 'update 1'
    #     DeviceProfile.objects.filter(device_id=id).update(status=1)
    # else:
    #     print 'update 0'
    #     DeviceProfile.objects.filter(device_id=id).update(status=0)

    num = int(data.status_manual)
    if num == 0:
        msg = 'Off'
    elif num ==1:
        msg = 'On'
    return HttpResponse(msg)

def setonoff(request,id,num):
    now =  timezone.make_aware(datetime.datetime.now(),timezone.get_default_timezone())
    #print now
    data = DeviceProfile.objects.filter(device_id=id)
    num = int(num)
    if num == 0:
        msg = 'Off'
        data.update(status_manual=0)
    elif num == 1:
        msg = 'On'
        data.update(status_manual=1)


    # data = DeviceProfile.objects.get(device_id=id)
    # now =  timezone.make_aware(datetime.datetime.now(),timezone.get_default_timezone())
    #
    # if data.openTime >= now <= data.closeTime:
    #     msg = '1'
    #     DeviceProfile.objects.get(device_id=id).update(status=1)
    # else:
    #     msg = '0'
    #     DeviceProfile.objects.get(device_id=id).update(status=0)
    return HttpResponse(msg)
