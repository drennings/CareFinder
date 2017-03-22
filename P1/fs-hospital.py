import csv
import json
import requests
import numpy as np

category = "4bf58dd8d48988d196941735" #hospital
token = "C34D1ZTW32QMDZCR4D1ZP3CK5Q53JLUEPTQOMC1JSSZ5V5Y5"

# convert("20-55N")
# convert("32-11-50.000W")
def convert(tude):
    multiplier = 1 if tude[-1] in ['N', 'E'] else -1
    return multiplier * sum(float(x) / 60 ** n for n, x in enumerate(tude[:-1].split('-')))


def getHospitals(identifier, lat, lon):
    url = 'https://api.foursquare.com/v2/venues/search?categoryId='+category+'&ll='+str(lat)+','+str(lon)+'&oauth_token='+token+'&v=20170316'
    print url
    r = requests.get(url)
    return r.json()

# 'cities-usa.tsv'
def collectHospitalsFromCityFile(path):
    with open(path,'rb') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
            city = row[0]
            lat = convert(row[1])
            lon = convert(row[2])
            print city + ": " + str(lat) + ", " +str(lon)
            response = getHospitals(city, lat, lon)
            code = response['meta']['code']
            if code == 200:
                filename = city+'.json'
            else:
                filename = 'error-'+city+'.json'

            with open('collection/'+filename, 'w') as outfile:
                json.dump(response, outfile)

# 'cities-usa.tsv'
#def findLargestRectangleFromCityFile(path):
with open("cities-usa.tsv",'rb') as tsvin:
    tsvin = csv.reader(tsvin, delimiter='\t')
    minLat = 1000
    minLon = 1000
    maxLat = -1000
    maxLon = -1000
    for row in tsvin:
        city = row[0]
        lat = convert(row[1])
        lon = convert(row[2])
        if (lat > 17.0 and lat < 90.0 and lon > -190.0 and lon < -55.13): # rough boundary around the us incl. alaska and hawaii
            print "\""+city+"\"" + ": { center: {lat: "+str(lat)+", lng: "+str(lon)+"} },"
            minLat = min(minLat, lat)
            minLon = min(minLon, lon)
            maxLat = max(maxLat, lat)
            maxLon = max(maxLon, lon)
    print "south: " + str(minLat) + ","
    print "north: " + str(maxLat) + ","
    print "west: " + str(minLon) + ","
    print "east: " + str(maxLon)
    # north: 50,
    # south:  17,
    # west: -170.0,
    # east: -55.1333333333
