from django.conf.urls import url,include
from django.contrib import admin
from pluggie import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^userprofile/', views.UserProfilePage, name='UserProfilePage'),
    url(r'^deviceprofile/', views.Device, name='Device'),
    url(r'^set_timezone', views.set_timezone ,name='set_timezone'),
    url(r'^home', views.home ,name='home'),
    url(r'^$', views.output),
    url(r'^adddevice/', views.adddevice,name='adddevice'),
    url(r'^editdevice/(?P<id>[0-9]+)/$', views.editdevice,name='editdevice'),
    url(r'^deletedevice/(?P<id>[0-9]+)/$', views.deletedevice,name='deletedevice'),
    url(r'^devicedetail.json', views.devicedetail, name='devicedatail'),
    url(r'^authen/',include('authen.urls')),
    #url(r'^updatedevice/', views.updatedevice,name='updatedevice'),
    url(r'^graph/', views.ChooseGraph,name='ChooseGraph'),
    url(r'^month_graph/$', views.MonthGraph,name='MonthGraph'),

]
