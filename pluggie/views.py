from django.http import HttpResponse , JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import DeviceProfile , UserProfile
import datetime
from django.utils import timezone
import pytz
from django.utils import formats
from django.template import RequestContext
from forms import DeviceProfileForm
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
            return  render(request, 'deviceprofile.html',{"date":str(now)})
    elif request.POST.get('canceladddevice'):
        return render(request, 'deviceprofile.html',{'devices': DeviceProfile.objects.filter(owner=request.user),"date":str(now)})
    else:
        form = DeviceProfileForm(initial={'owner':request.user})
        form.fields['owner'].widget.attrs['readonly'] = 'True'
    return render(request, 'deviceprofile_add.html', {'form': form,"date":str(now)})


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

def Device(request):
    now = datetime.datetime.now()
    now = formats.date_format(now,"SHORT_DATETIME_FORMAT")
    if request.POST.get('deletedevice'):
         #print request.POST.getlist('items')
         #print  DeviceProfile.objects.filter(id__in=request.POST.getlist('items'))
         DeviceProfile.objects.filter(id__in=request.POST.getlist('items')).delete()
    elif request.POST.get('editdevice'):
            #data = DeviceProfile.objects.filter(id__in=request.POST.getlist('items'))
            #data.update(usage=345)
            data = DeviceProfile.objects.get(pk=request.POST.get('items'))
            #print data
            form = DeviceProfileForm(initial={'owner':request.user})
            dv = {'owner':data.owner,'device_name':data.device_name,'usage':data.usage,'openTime':data.openTime,'closeTime':data.closeTime}
            form = DeviceProfileForm(dv)
            form.fields['owner'].widget.attrs['readonly'] = 'True'
            form.fields['owner'].widget.attrs['disabled'] = 'True'
            return render(request, 'deviceprofile_edit.html', {'form': form,"date":str(now)})
    elif request.POST.get('updatedevice'):
        print "Yoooooooooo----------!!!!!"
        print dv
    return render(request, 'deviceprofile.html',{'devices': DeviceProfile.objects.filter(owner=request.user),"date":str(now)})
        #return render(request, 'deviceprofile_edit.html', {'form': form,"date":str(now)})

def ChooseGraph(request):
    now = datetime.datetime.now()
    now = formats.date_format(now,"SHORT_DATETIME_FORMAT")
    return render(request,'choosegraph.html',{"date":str(now)})

def MonthGraph(request):
    plot = figure()
    plot.circle([1,2], [3,4],[7,8])

    script, div = components(plot)

    return render(request, "simple_chart.html", {"the_script": script, "the_div": div})
