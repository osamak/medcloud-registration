from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin


urlpatterns = [
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup/', include('register.urls', namespace='register'), ),
]
