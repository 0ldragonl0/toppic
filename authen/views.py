from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from forms import UserForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
import datetime
from django.utils import formats
from pluggie.models import DeviceProfile , UserProfile


# Create your views here.
def signin(request):
    if request.POST.get('login') and 'username' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        print "password: %s"%password
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['user_username'] = user.username
                print "username:%s"%user.username
                #return render(request,'index.html',{'msg': "Do something"})
                return redirect('home')
            else:
                msg="Disabled account"
        else:
            msg="Invalid login"
        return render(request,'signin.html',{'msg': msg})
    elif request.POST.get('register'):
        form = UserForm()
        return render(request, 'adduser.html', {'form': form})
    elif request.POST.get('save'):
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            new_user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request,new_user)
            print new_user.username
            user_pro = UserProfile.objects.create(user = new_user)
            user_pro.save()
            # redirect, or however you want to get to the main view
            msg ="Registered."
            return  render(request, 'signin.html',{'msg': msg})
    elif request.POST.get('cancel'):
        msg = "Please sign-in."
        return  render(request, 'signin.html',{'msg': msg})
    return render(request,'signin.html',{'msg': "Please sign-in"})


def signout(request):
    if request.method == 'POST':
        print "signout"
        if 'user_username' in request.session:
            del request.session['user_username']
            print "del uname"
        logout(request)
    return render(request,'signin.html',{'msg': "Please sign-in"})


#@login_required(login_url='url_signin')
def home(request):
    now = datetime.datetime.now()
    now = formats.date_format(now,"SHORT_DATETIME_FORMAT")
    print "_index user:%s"%request.user.username
    if 'user_username' in request.session:
        uname=request.session['user_username']
    else:
        uname="Anonymous"
    return render(request,'home.html',{"date":str(now)})


from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello World!")

# def lexusadduser(request):
#     if request.POST.get('save'):
#         form = UserForm(request.POST)
#         if form.is_valid():
#             new_user = User.objects.create_user(**form.cleaned_data)
#             new_user.backend = 'django.contrib.auth.backends.ModelBackend'
#             login(request,new_user)
#             # redirect, or however you want to get to the main view
#             msg ="Registered."
#             return  render(request, 'signin.html',{'msg': msg})
#     elif request.POST.get('cancel'):
#         msg = "Please sign-in."
#         return  render(request, 'signin.html')
#     else:
#         form = UserForm()
#     return render(request, 'adduser.html', {'form': form})
