from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^play/(?P<id>[^/]+)/$', views.play, name='play'),
    url(r'^score/$', views.score, name='score'),
]