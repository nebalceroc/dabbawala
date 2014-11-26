from django.conf.urls import patterns, url
from delivery import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^forbidden/$', views.register, name='forbidden'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^op/$', views.op_panel, name='op_panel'),
    url(r'^dom/$', views.dom_panel, name='dom_panel'),
)
