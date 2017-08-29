from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.greeting, name='greeting'),
    url(r'^registration$', views.registration, name='registration'),
    url(r'^login$', views.login, name='login'),
    url(r'^validate$', views.validate, name='validate'),
]