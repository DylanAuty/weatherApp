from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context

from django.conf import settings
from datetime import date, datetime, timedelta
from weatherApp.utils import utils
import requests
import json

# Model imports
from weatherApp.models import location, forecast, conditions

def index(request):
    """
    The weather landing page.
    Retrieves and serves last known request for London at start.
    On page load, an AJAX request will check for updates from the server.
    If an update is available, it will retrieve it and AJAX will fill it in.
    This way, the page appears to load as fast as possible for the user.
    Later comes pretty cacheing.
    """

    # Retrieve most recent entry for London from DB, stick into context and return it.
    # If one doesn't exist, then fire the querying method.
    
    searchString = "London"     # PLACEHOLDER
    # Autocomplete search and reference string retrieval
    searchResults = utils.getAutocompleteResults(searchString)

    locationString = "/q/zmw:00000.1.03772"

    try:
        # Every one of these should succeed. If any fails, it means a fresh forecast needs fetching.
        fcToday = forecast.objects.filter(location__api_ref_string = locationString, date = date.today()).latest('retrieved')
        fcNext1 = forecast.objects.filter(location__api_ref_string = locationString, date = date.today()+timedelta(days=1)).latest('retrieved')
        fcNext2 = forecast.objects.filter(location__api_ref_string = locationString, date = date.today()+timedelta(days=2)).latest('retrieved')
        fcNext3 = forecast.objects.filter(location__api_ref_string = locationString, date = date.today()+timedelta(days=3)).latest('retrieved')
    except forecast.DoesNotExist:
        
        # If there is no forecast in the database then we need to retrieve and store it.
        # The retrieval method will save and return the object, ideally it will save asynchronously.
        pass

    context = {
            "currTime": datetime.now(),
            "retrievalTime": fcToday.retrieved,
            "fcToday": fcToday,
            "fcNext1": fcNext1,
            "fcNext2": fcNext2,
            "fcNext3": fcNext3,
            }
    return render(request, 'weatherApp/index.html', context)

def getExampleForecastJSON(request):
    """
    Retrieves an example forecast for London from local.
    Used for debugging, to avoid exceeding API limits.
    """
    
    return render(request, 'weatherApp/forecastEx.json')

def about(request):
    """
    Returns the hard-coded About page.
    Done using a view instead of hard coding the URL in case this page will need to be made
    dynamic later on (e.g. with version numbers, team contacts etc.)
    """

    return render(request, 'weatherApp/about.html')
