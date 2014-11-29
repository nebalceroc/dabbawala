from django.conf.urls import patterns, url
from rest_api import views

urlpatterns = patterns('',
    url(r'^comm$', views.query, name='query'),
)
