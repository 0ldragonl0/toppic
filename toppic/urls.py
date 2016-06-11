from django.conf.urls import url,include
from django.contrib import admin
from pluggie import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^userprofile/', views.UserProfilePage, name='UserProfilePage'),
    url(r'^deviceprofile/', views.Device, name='Device'),
    url(r'^home', views.home ,name='home'),
    url(r'^$', views.output),
    url(r'^adddevice/', views.adddevice,name='adddevice'),
    url(r'^editdevice/(?P<id>[0-9]+)/$', views.editdevice,name='editdevice'),
    url(r'^deletedevice/(?P<id>[0-9]+)/$', views.deletedevice,name='deletedevice'),
    url(r'^devicedetail.json', views.devicedetail, name='devicedatail'),
    url(r'^authen/',include('authen.urls')),
    url(r'^graph/', views.ChooseGraph,name='ChooseGraph'),
    url(r'^month_graph/$', views.MonthGraph,name='MonthGraph'),
    url(r'^realtime_graph/$', views.RealtimeGraph,name='RealtimeGraph'),
    url(r'^editprofile/(?P<id>[0-9]+)/$', views.edit_profile,name='edit_profile'),
    #url(r'^updateusage/$', views.updateusage,name='updateusage'),
    url(r'^updateusage/(?P<id>[0-9]+)/(?P<num>\d+\.\d{2})/$', views.updateusage,name='updateusage'),
    url(r'^setonoff/(?P<id>[0-9]+)/(?P<num>[0-9]+)/$', views.setonoff,name='setonoff'),
    url(r'^realtimeData.tsv/$',views.realtimeData,name='realtimeData'),
]
