from django.conf.urls import url
from django.views.generic import TemplateView

from register import views

urlpatterns = [
    url(r'^$', views.register, name='register'),
    url(r'^forgotten/$', views.forgotten, name='forgotten'),
    url(r'^thanks/$', TemplateView.as_view(template_name='register/thanks.html'), name='thanks'),
]
