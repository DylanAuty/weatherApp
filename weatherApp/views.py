from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from django.views.decorators.cache import cache_page

from django.conf import settings
from datetime import date, datetime, timedelta
from weatherApp.utils import utils
from weatherApp.decorators import cache_page_vary_on_locationString
import requests
import json

# Model imports
from weatherApp.models import location, forecast, conditions

@cache_page_vary_on_locationString
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
    # When using caching - if this point is reached, we can safely naively pull fresh data from the API.
    if request.method == 'POST' and request.POST['locationString']:
        locationString = request.POST['locationString']
        request.session['locationString'] = locationString
    elif 'locationString' in request.session:
        locationString = request.session.get('locationString')
    else:
        locationString = "/q/zmw:00000.1.03772"     # For London, UK.
# The try/except is necessary if caching is disabled, but when enabled with the correct limit then data can be retrieved naively with no overhead.
#    try:
#        # Every one of these should succeed. If any fails, it means a fresh forecast needs fetching.
#        fcToday = forecast.objects.filter(location__api_ref_string = locationString, date = date.today()).latest('retrieved')
#        fcNext1 = forecast.objects.filter(location__api_ref_string = locationString, date = date.today()+timedelta(days=1)).latest('retrieved')
#        fcNext2 = forecast.objects.filter(location__api_ref_string = locationString, date = date.today()+timedelta(days=2)).latest('retrieved')
#        fcNext3 = forecast.objects.filter(location__api_ref_string = locationString, date = date.today()+timedelta(days=3)).latest('retrieved')
#    except forecast.DoesNotExist:
    utils.getCurrentWeather(locationString = locationString)
    fcToday = forecast.objects.filter(location__api_ref_string = locationString, date = date.today()).latest('retrieved')
    fcNext1 = forecast.objects.filter(location__api_ref_string = locationString, date = date.today()+timedelta(days=1)).latest('retrieved')
    fcNext2 = forecast.objects.filter(location__api_ref_string = locationString, date = date.today()+timedelta(days=2)).latest('retrieved')
    fcNext3 = forecast.objects.filter(location__api_ref_string = locationString, date = date.today()+timedelta(days=3)).latest('retrieved')

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

def getExampleLocationJSON(request):
    """
    Retrieves an example location search result json, run on the string "London".
    Used for offline debugging.
    """

    return render(request, 'weatherApp/locationEx.json')

def about(request):
    """
    Returns the hard-coded About page.
    Uses a view instead of hard-coded URL to take advantage of the Django template system.
    """
    return render(request, 'weatherApp/about.html')






