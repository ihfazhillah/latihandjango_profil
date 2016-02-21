from django.conf.urls import url
from . import views


urlpatterns = ( url(r'^$', views.index, name='index'),
               url(r'^(?P<pk>\d+)/$', views.detail, name='detail'),
               url(r'^create/$', views.create, name='create'),
               url(r'^(?P<pk>\d+)/edit$', views.edit, name='edit'),
               url(r'^login/$', views.login, name='login'),
               url(r'^logout/$', views.logout, name='logout'),
               )