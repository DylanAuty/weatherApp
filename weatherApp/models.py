from __future__ import unicode_literals

from django.db import models

class location(models.Model):
    """
    Represents a location as returned by Wunderground's geolookup feature.
    Some fields have been omitted as they are undocumented by Wunderground or unnecessary
    for this application.

    Fields:
    * location_type:    Either CITY or INTCITY, maybe more but Wunderground documentation is missing.
    * country:          Country code (e.g. UK, FR etc.)
    * country_iso3116:  As above, compliant with ISO 3116
    * country_name:     Name of country, written in full (United States of America, United Kingdom etc.)
    * state:            Code for state in the US, e.g. AZ, TX, CA. Unclear what happens abroad with this.
    * city:             Name of the city.
    * tz_short:         Code of the timezone in the location, e.g. EST, GMT, UTC
    * tz_long:          Country/city timezone e.g. "Australia/Sydney"
    * lat:              Latitude, in decimal degrees format.
    * lon:              Longitude, in decimal degrees format.
    """
    
    api_ref_string = models.CharField(max_length=200)
    location_type = models.CharField(max_length=200)
    country = models.CharField(max_length=20)
    country_iso3166 = models.CharField(max_length=20)
    country_name = models.CharField(max_length = 200)
    state = models.CharField(max_length = 20)
    city = models.CharField(max_length = 200)
    tz_short = models.CharField(max_length = 20)
    tz_long = models.CharField(max_length = 64)
    lat = models.CharField(max_length = 200)
    lon = models.CharField(max_length = 200)

class forecast(models.Model):
    """
    Represents a weather forecast.
    Data collated from txt_forecast and simpleforecast objects returned by Wunderground API.
    A forecast instance represents the weather forecast for a day. It includes day/night text forecasts and chances of rain, and 
    a more detailed forecast for the whole of the day.

    Fields:
    * location:             Foreign key to location table. Every forecast has a location.
                            If location gets deleted then all forecasts for that location will go too.
    * date:                 The date the forecast refers to. A Date object. Inferred from retrieval date, possibly checked against an epoch from simpleforecast.
    * last_updated:         The timestamp the forecast was updated, as reported by Wunderground.
    * retrieved:            The timestamp the forecast was retrieved from the server at.
    * icon_tf_day:          From txt_forecast, for the day. Icon returned from txt_forecast and simpleforecast will differ.
                            A keyword describing the weather icon to be used (cloudy, sunny etc.)
    * icon_tf_night:        From txt_forecast, for the night.
    * icon_sf:              From simpleforecast. A keyword describing the weather icon to be used (cloudy, sunny etc.)
    * icon_tf_day_url:      From txt_forecast, for the day icon. The API returns a URL for an icon resource. This may not be used but will be stored anyway.
    * icon_tf_day_url:      From txt_forecast, for the night icon.
    * icon_sf_url:          From simpleforecast.
    * fcttext_metric_day:   Contains a text forecast for the day, with metric units. API returns an Imperial one too, which won't be used.
    * fcttext_metric_night: Contains a text forecast for the night, with metric units. API returns an Imperial one too, which won't be used.
                            See https://www.wunderground.com/weather/api/d/docs?d=resources/phrase-glossary for details.
    * pop:                  Probability of precipitation (%) for the whole day. Derived from simpleforecast.
    * pop_tf_day:           Probability of precipitation (%) for the daytime. Derived from txt_forecast. Storing 3 different pops as they sometimes don't
                            match up, so will present them as given.
    * pop_tf_night:         Probability of precipitation (%) for the night.
    * high:                 Temp. high (C) for the whole day. From simpleforecast.
    * low:                  Temp. low (C) for the whole day. From simpleforecast.
    * conditions:           Text description of the weather conditions for the entire day. Derived from simpleforecast.
    * max_windspeed:        Maximum windspeed in Km/h
    * max_winddir:          Direction of maximum winds that period.
    * ave_windspeed:        Average windspeed in Km/h
    * ave_winddir:          Average wind direction (North, ESE etc.). 20 chars as one listed val. is 'variable'.
    * ave_humidity:         Percentage average humidity.
    * max_humidity:         Percentage maximum humidity. Seems to malfunction (showed 0 when ave was 74 in one example)
    * min_humidity:         Percentage minimum humidity, same issue as with max_humidity.
    """
    
    # Metadata (time/location)
    location = models.ForeignKey('location', on_delete=models.CASCADE)
    date = models.DateField()
    retrieved = models.DateTimeField()

    # Icons
    icon_tf_day = models.CharField(max_length=20)           # From txt_forecast. Current max length used is 14.
    icon_tf_night = models.CharField(max_length=20)         # From txt_forecast. Current max length used is 14.
    icon_sf = models.CharField(max_length=20)               # From simpleforecast
    icon_tf_day_url = models.URLField(max_length=200)       # From txt_forecast.
    icon_tf_night_url = models.URLField(max_length=200)     # From txt_forecast.
    icon_sf_url = models.URLField(max_length=200)           # From simpleforecast
    
    # Text forecasts
    fcttext_metric_day = models.CharField(max_length=200)   # Name fcttext_metric chosen for consistency with API responses.
    fcttext_metric_night = models.CharField(max_length=200)

    # Raw weather data
    pop = models.IntegerField(blank=True, null=True)             # Probability of Precipitation. A percentage. This taken from simpleforecast, referring to the whole day.
    pop_tf_day = models.IntegerField(blank=True, null=True)      # As above, but taken from txt_forecast and referring to the day. Stored as sometimes the three pop fields don't correspond, so will be shown as given.
    pop_tf_night = models.IntegerField(blank=True, null=True)    # As above, but for night.
    high = models.IntegerField(blank=True, null=True)            # Temp. high in Celcius
    low = models.IntegerField(blank=True, null=True)             # Temp. low in Celcius.
    conditions = models.CharField(max_length=200)         # Condition description.
    max_windspeed = models.IntegerField(blank=True, null=True)   # In Km/h
    max_winddir = models.CharField(max_length=20)  # Compass direction (NNE, ESE etc.)
    ave_windspeed = models.IntegerField(blank=True, null=True)
    ave_winddir = models.CharField(max_length=20)
    ave_humidity = models.IntegerField(blank=True, null=True)    # Percentage
    max_humidity = models.IntegerField(blank=True, null=True)    # Percentage, weirdly returns 0 sometimes.
    min_humidity = models.IntegerField(blank=True, null=True)    # Also 0 sometimes for no reason.
    
class conditions(models.Model):
    """
    Represents current conditions somewhere. Some fields overlap with forecast, but
    the API delivers a separate conditions object that contains other things as well.

    Fields:
	* display_location:	
	* observation_timestamp: Used in conjunction with location timezone.
	* observation_tz:           This may not be needed
        * weather:                  A text description of the current weather ("Mostly cloudy", "Chance of rain" etc.)
        * temperature:              Temperature, in degrees Celsius.
        * humidity:                 Percentage relative humidity.
        * wind_dir:                 A compass direction, or "Variable".
        * windspeed:                 Nominal windspeed, metric.
        * windspeed_gust:            Gusting windspeed, metric. For some reason this can sometimes be 0, it is unclear what this is indicating (documentation missing from Wunderground)
        * pressure:              Atmospheric pressure, millibars.
        * dewpoint:                 The dewpoint, in degrees Celsius.
        * feelslike:                The feels like temperature, taking into account wind chill, humidity etc.
        * visibility:               The visibility in km.
        * uv:                       The UV index
        * precip_1hr:               The precipitation in the next hour, mm. Can be "--".
        * precip_today:             The precipitation in the next day, mm. Can be "--".
        * icon:                     The name of the icon to use for these conditions.
        * icon_url:                 The URL of the icon to use.
        * forecast_url:             URL of the Wunderground page for this forecast.
    """

    display_location = models.ForeignKey('location', on_delete=models.CASCADE)
    observation_timestamp = models.DateTimeField()
    observation_tz = models.CharField(max_length=20)
    weather = models.CharField(max_length=100)
    temperature = models.IntegerField(blank=True, null=True)
    humidity = models.IntegerField(blank=True, null=True)
    wind_dir = models.CharField(max_length=20)
    windspeed = models.IntegerField(blank=True, null=True)
    windspeed_gust = models.IntegerField(blank=True, null=True)
    pressure = models.IntegerField(blank=True, null=True)
    dewpoint = models.IntegerField(blank=True, null=True)
    feelslike = models.IntegerField(blank=True, null=True)
    visibility = models.IntegerField(blank=True, null=True)
    uv = models.IntegerField(blank=True, null=True)
    precip_1hr = models.IntegerField(blank=True, null=True)
    precip_today = models.IntegerField(blank=True, null=True)
    icon = models.CharField(max_length=20)
    icon_url = models.URLField(max_length=200)
    forecast_url = models.URLField(max_length=200)



