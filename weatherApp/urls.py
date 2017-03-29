from django.conf.urls import url

from . import views
from weatherApp.utils import utils

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^about/$', views.about, name="about"),
 #   url(r'^getCurrentWeather/$', views.getCurrentWeather, name="getCurrentWeather"),
    url(r'^getExampleForecastJSON/$', views.getExampleForecastJSON, name="getExampleForecastJSON"),
    url(r'^getExampleLocationJSON/$', views.getExampleForecastJSON, name="getExampleForecastJSON"),
    url(r'^getAutocompleteResults/$', utils.getAutocompleteResults, name="getAutocompleteResults"),
    ]






