from django.conf.urls import url

from cloudsearch import views

urlpatterns = [
    url(r'^$', views.search, name='search'),
]
