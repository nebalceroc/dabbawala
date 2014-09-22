from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'delivery.views.index', name='index'),
    url(r'^delivery/', include('delivery.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^payment/', include('payment.urls')),
    url(r'^report/', include('report.urls')),
    
)
