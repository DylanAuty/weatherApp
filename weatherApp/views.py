from django.shortcuts import render
from django.http import HttpResponse

import requests
import json

def index(request):

    context = {

            }
    return render(request, 'weatherApp/index.html', context)

def getCurrentWeather(request):
    API_response = requests.get('http://api.wunderground.com/api/b405479b9102f47f/forecast/q/CA/San_Francisco.json')
    return HttpResponse(API_response)



