from django.conf.urls import url
from . import views

urlpatterns = [
		url(r'^$home/$', views.home, name='home'),
        url(r'^$set_timezone/$', views.set_timezone, name='set_timezone'),
	]
