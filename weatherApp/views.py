from django.shortcuts import render
from django.http import HttpResponse

from django.conf import settings
import requests
import json

def index(request):
    # Retrieve most recent entry for London from DB, stick into context and return it.
    # If one doesn't exist, then fire the querying method.
    
    context = {

            }
    return render(request, 'weatherApp/index.html', context)

def getCurrentWeather(request):
    # Dummy placeholder text
    locationString = "/q/zmw:00000.1.03772"
    #requestURL = "http://api.wunderground.com/api/" + settings.WUNDERGROUND_API_KEY + "/forecast" + locationString + ".json"
    requestURL = "file:///home/da-sol-vb/Documents/HealthUnlocked/forecastEx.json"

    API_response = requests.get(requestURL)
    #print(type(API_response.json()))
    #API_response_JSON = json.loads(API_response)
    #print(API_response_JSON.dumps)

    return HttpResponse(API_response)


def getExampleForecastJSON(request):
    """
    Retrieves an example forecast for London from local.
    Used for debugging, to avoid exceeding API limits.
    """
    return render(request, 'weatherApp/forecastEx.json')
