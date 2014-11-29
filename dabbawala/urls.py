from django.conf.urls import patterns, include, url

from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'delivery.views.index', name='index'),
    url(r'^delivery/', include('delivery.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^payment/', include('payment.urls')),
    url(r'^report/', include('report.urls')),
    url(r'^rest_api/', include('rest_api.urls'))
    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
