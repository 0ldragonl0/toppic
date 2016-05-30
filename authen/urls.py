from django.conf.urls import url
from . import views

urlpatterns = [
            url(r'^$', views.signin, name='signin'),
            url(r'^signout/$', views.signout, name='signout'),
            url(r'^index/$', views.index, name='index'),
            url(r'^home/$', views.home, name='home'),
            #url(r'^adduser/$', views.lexusadduser, name='adduser'),
]
