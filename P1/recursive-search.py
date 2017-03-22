import csv
import json
import sys
import requests
import unicodedata
import time

key = ''
url = ''
output = 'json'
type = 'hospital'
latitude = 38.0000
longitude = -97.0000
radius = 50000

# Get user key if provided, else ask for it
try:
    key = sys.argv[1]
except IndexError:
    print "INDEXERROR: Please provide your API key"

# Get all hospital data up to 60 results
def getHospitalsWithinRange(latitude, longitude, radius, nextpagetoken):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/' + output + '?location=' + str(latitude) + ',' + str(longitude) + '&radius=' + str(radius) +'&type=' + type + '&key=' + key + '&pagetoken=' + str(nextpagetoken)
    print url
    r = requests.get(url)
    jsonresult = r.json()

    if("next_page_token" in jsonresult):
        nextpagetoken = jsonresult['next_page_token']
        time.sleep(2)
        jsonOtherresult = getHospitalsWithinRange(latitude, longitude, radius, nextpagetoken)
        return [jsonresult,jsonOtherresult]
    else:
        return jsonresult
    
# Do the recursive job
res = getHospitalsWithinRange(latitude, longitude, radius, '')

#if(res['status'] == 'REQUEST_DENIED'):
#    print "REQUESTERROR: Please check you request"

print(res)