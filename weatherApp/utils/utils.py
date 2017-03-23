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

