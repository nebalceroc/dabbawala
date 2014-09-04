from django.conf.urls import patterns, url
from payment import views

urlpatterns = patterns('',
    url(r'^(?P<request_id>[\d]*)/?', views.menu_charge, name='menu_charge'),

)