from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^getCurrentWeather/$', views.getCurrentWeather, name="getCurrentWeather"),
]






