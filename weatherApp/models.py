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

    location_type = models.CharField(max_length=200)
    country = models.CharField(max_length=20)
    country_iso3116 = models.CharField(max_length=20)
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

    Fields:
    * location:         Foreign key to location table. Every forecast has a location.
                        If location gets deleted then all forecasts for that location will go too.
    * period:           A number from 0 to ??? (WU docs incomplete, probably 7 or 13?).
                        Refers to a half of a particular day of the week.
    * date:             The date the forecast refers to. A DateTime object.
                        Used in conjunction with ampm and period.
    * ampm:             Whether the forecast refers to the morning (AM) or evening (PM).
    * icon_tf:          From txt_forecast, icon returned from txt_forecast and simpleforecast will differ.
                        A keyword describing the weather icon to be used (cloudy, sunny etc.)
    * icon_sf:          From simpleforecast. A keyword describing the weather icon to be used (cloudy, sunny etc.)
    * icon_tf_url:      From txt_forecast. Sometimes the icons differ between the two.
                        The API returns a URL for an icon resource.
                        This may not be used but will be stored anyway.
    * icon_sf_url:      From simpleforecast.
                        The API returns a URL for an icon resource.
                        This may not be used but will be stored anyway.
    * title:            Describes time period forecast refers to. A day of the week, plus optionally the word "night", if pulled from txt_forecast, else None.
    * fcttext_metric:   Contains a text forecast, with metric units. API returns an Imperial one too, which won't be used.

                        See https://www.wunderground.com/weather/api/d/docs?d=resources/phrase-glossary for details.
    * max_windspeed:    Maximum windspeed in Km/h
    * max_winddir:      Direction of maximum winds that period.
    * ave_windspeed:    Average windspeed in Km/h
    * ave_winddir:      Average wind direction (North, ESE etc.). 20 chars as one listed val. is 'variable'.
    * ave_humidity:     Percentage average humidity.
    * max_humidity:     Percentage maximum humidity. Seems to malfunction (showed 0 when ave was 74 in one example)
    * min_humidity:     Percentage minimum humidity, same issue as with max_humidity.
    """
    
    # Metadata (time/location)
    location = models.ForeignKey('location', on_delete=models.CASCADE)
    period = models.IntegerField()
    date = models.DateTimeField()
    ampm = models.CharField(max_length=10)       # 10 chars as a precaution
    # Icons
    icon_tf = models.CharField(max_length=20)   # From txt_forecast. Current max length used is 14.
    icon_sf = models.CharField(max_length=20)   # From simpleforecast
    icon_tf_url = models.URLField(max_length=200)   # From txt_forecast.
    icon_sf_url = models.URLField(max_length=200)   # From simpleforecast
    title = models.CharField(max_length=20) # <day of the week + optionally " night">
    fcttext_metric = models.CharField(max_length=200)   # There is also an imperial field returned called fcttext, which won't be used. Name fcttext_metric chosen for consistency with API responses.
    
    # Raw weather data
    pop = models.IntegerField()             # Probability of Precipitation. A percentage.
    high = models.IntegerField()            # Temp. high in Celcius
    low = models.IntegerField()             # Temp. low in Celcius.
    conditions = models.CharField(max_length=200)         # Condition description.
    max_windspeed = models.IntegerField()   # In Km/h
    max_winddir = models.CharField(max_length=20)  # Compass direction (NNE, ESE etc.)
    ave_windspeed = models.IntegerField()
    ave_winddir = models.CharField(max_length=20)
    ave_humidity = models.IntegerField()    # Percentage
    max_humidity = models.IntegerField()    # Percentage, weirdly returns 0 sometimes.
    min_humidity = models.IntegerField()    # Also 0 sometimes for no reason.
    
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
    temperature = models.IntegerField()
    humidity = models.IntegerField()
    wind_dir = models.CharField(max_length=20)
    windspeed = models.IntegerField()
    windspeed_gust = models.IntegerField()
    pressure = models.IntegerField()
    dewpoint = models.IntegerField()
    feelslike = models.IntegerField()
    visibility = models.IntegerField()
    uv = models.IntegerField()
    precip_1hr = models.IntegerField()
    precip_today = models.IntegerField()
    icon = models.CharField(max_length=20)
    icon_url = models.URLField(max_length=200)
    forecast_url = models.URLField(max_length=200)



