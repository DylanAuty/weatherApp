from django.conf import settings
from datetime import date, datetime, timedelta

# Model imports
from weatherApp.models import location, forecast, conditions

import requests
import json

def getAutocompleteResults(searchString):
    """
    Access the Wunderground API's autocomplete feature, which returns a
    JSON of possible locations matches.
    
    Arguments:
    searchString -- The string to lookup. This will be input by the user (and sanitised).

    Returns:
    locResults --   A dict containing multiple possible results - their names and refStrings.
    """

    requestURL = "http://autocomplete.wunderground.com/aq?query=" + searchString
    
    APIResponseRaw = requests.get(requestURL)
    return APIResponseRaw.json()['RESULTS']


def getCurrentWeather(locationString="/q/zmw:00000.1.03772"):
    """
    Fetches the current weather.
    If no locationString is provided, it uses the default (London, UK).
    """

    requestURL = "http://api.wunderground.com/api/" + settings.WUNDERGROUND_API_KEY + "/geolookup/forecast" + locationString + ".json"
    #requestURL = "http://127.0.0.1:8000/getExampleForecastJSON"

    APIResponseRaw = requests.get(requestURL)       # Keep raw data in case any other response info is needed.
    APIResponseDict = APIResponseRaw.json()
    ForecastDict = APIResponseDict['forecast']
    textForecastDict = ForecastDict['txt_forecast']['forecastday']
    simpleForecastDict = ForecastDict['simpleforecast']['forecastday']

    # See if the location is stored. If not, store it.
    try:
        currLoc = location.objects.get(api_ref_string=locationString)
    except location.DoesNotExist:
        currLoc = location()
        currLoc.api_ref_string = locationString          ## PLACEHOLDER
        currLoc.location_type = APIResponseDict['location']['type']
        currLoc.country = APIResponseDict['location']['country']
        currLoc.country_iso3166 = APIResponseDict['location']['country_iso3166']
        currLoc.country_name = APIResponseDict['location']['country_name']
        currLoc.state = APIResponseDict['location']['state']
        currLoc.city = APIResponseDict['location']['city']
        currLoc.tz_short = APIResponseDict['location']['tz_short']
        currLoc.tz_long = APIResponseDict['location']['tz_long']
        currLoc.lat = APIResponseDict['location']['lat']
        currLoc.lon = APIResponseDict['location']['lon']
        currLoc.save()

    # Loop over the txt_forecasts, extracting relevant data.
    # There are 8 periods. For txt_forecast, 2 per day. For simpleforecast, 1 per day, starting at 1.

    # Instantiate 4 forecasts. Loop over forecastDays, adding to correct forecast depending on their period.
    forecastArr = [forecast() for i in range(4)]
    forecastDate = date.today()     # Assumption is that forecasts begin today.
    oneDayDelta = timedelta(days=1) # To increment the date stored for the forecast. Instantiated once here to save time.
	
    for i in range(8):
	fc_index = (i / 2)  # fc_index maps i -> period - 1 of simpleforecast.

        # For day/night specific fields from txt_forecast
        if(i % 2 == 0):
            forecastArr[fc_index].date = forecastDate
            forecastArr[fc_index].retrieved = datetime.now()
            forecastDate += oneDayDelta

            forecastArr[fc_index].icon_tf_day = textForecastDict[i]['icon']
            forecastArr[fc_index].icon_tf_day_url = textForecastDict[i]['icon_url']
            forecastArr[fc_index].fcttext_metric_day = textForecastDict[i]['fcttext_metric']
            forecastArr[fc_index].pop_tf_day = textForecastDict[i]['pop']

        else:
            forecastArr[fc_index].icon_tf_night = textForecastDict[i]['icon']
            forecastArr[fc_index].icon_tf_night_url = textForecastDict[i]['icon_url']
            forecastArr[fc_index].fcttext_metric_night = textForecastDict[i]['fcttext_metric']

            forecastArr[fc_index].pop_tf_night = textForecastDict[i]['pop']

    for fc_index in range(4):
        # Assign location
        forecastArr[fc_index].location = currLoc

        # All other fields, from simpleforecast.
        forecastArr[fc_index].icon_sf = simpleForecastDict[fc_index]['icon']
        forecastArr[fc_index].icon_sf_url = simpleForecastDict[fc_index]['icon_url']
        forecastArr[fc_index].pop = simpleForecastDict[fc_index]['pop']
        forecastArr[fc_index].high = simpleForecastDict[fc_index]['high']['celsius']
        forecastArr[fc_index].low = simpleForecastDict[fc_index]['low']['celsius']
        forecastArr[fc_index].conditions = simpleForecastDict[fc_index]['conditions']
        forecastArr[fc_index].max_windspeed = simpleForecastDict[fc_index]['maxwind']['kph']
        forecastArr[fc_index].max_winddir = simpleForecastDict[fc_index]['maxwind']['dir']
        forecastArr[fc_index].ave_windspeed = simpleForecastDict[fc_index]['avewind']['kph']
        forecastArr[fc_index].ave_winddir = simpleForecastDict[fc_index]['avewind']['dir']
        forecastArr[fc_index].ave_humidity = simpleForecastDict[fc_index]['avehumidity']
        forecastArr[fc_index].max_humidity = simpleForecastDict[fc_index]['maxhumidity']
        forecastArr[fc_index].min_humidity = simpleForecastDict[fc_index]['minhumidity']

        forecastArr[fc_index].save()

    return 
