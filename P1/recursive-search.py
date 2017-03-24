import csv
import json
import sys
import requests
import unicodedata
import time
import math

# Chosen Google Places API Values for all calls
key = ''
output = 'json'
type = 'hospital'

# Get user key if provided, else ask for it
try:
    key = sys.argv[1]
except IndexError:
    print "INDEXERROR: Please provide your API key"

# Return a list of jsonresults given the paramaters to Google Places
def getHospitalsWithinRange(latitude, longitude, radius, nextpagetoken):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/' + output + '?location=' + str(latitude) + ',' + str(longitude) + '&radius=' + str(radius) +'&type=' + type + '&key=' + key + '&pagetoken=' + str(nextpagetoken)
    print((50000/radius-1)*'\t' + url)
    r = requests.get(url)
    jsonresult = r.json()

    if("next_page_token" in jsonresult):        # When a query has more than 20 results
        nextpagetoken = jsonresult['next_page_token']
        #print((50000/radius-1)*'\t' + url+str(nextpagetoken))
        time.sleep(2)                           # Wait for nextpage to be ready
        r2 = requests.get(url+str(nextpagetoken))
        jsonresult2 = r2.json()
        
        if("next_page_token" in jsonresult2):   # When a query has more than 40 
            nextpagetoken = jsonresult2['next_page_token']
            #print((50000/radius-1)*'\t' + url+str(nextpagetoken))
            time.sleep(2)                       # Wait for nextpage to be ready
            r3 = requests.get(url+str(nextpagetoken))    
            jsonresult3 = r3.json()
            return [jsonresult, jsonresult2, jsonresult3]   # Return the result of 3 pages 
        else:
            return [jsonresult,jsonresult2]             # Return the result of 2 pages 
    else:
        return [jsonresult]                                 # Return the result of 1 page

# Return a clean list of (at most 60) hospitals given a list of jsonresults from Google Places        
def fetchHospitalResult(jsonresultlist):
    hospitalList = []
    for jsonresult in jsonresultlist:
        hospitalList.extend(jsonresult['results'])           
    return hospitalList

# Get all hospitals within a square with center (latitude, longitude)
# Through an exhaustive recursive call
# Length of the box is sqrt(d^2/2) due to ABC formula
def getAllHospitalsWithinRange(latitude, longitude, radius):
    jsonresultlist = getHospitalsWithinRange(latitude, longitude, radius, '')
    hospitals = fetchHospitalResult(jsonresultlist)
    print("(" + str(latitude) + "," + str(longitude) + ")")
    
    if len(hospitals) == 60:
        print('found 60 or more hospitals!')
        halfradius = radius/2
        print(halfradius)
        #brng = [22.5,67.5,112.5,157.5]
        brng = [45.0,135.0,225.0,315.0]
        #brng = [45,90,135,180]
        #brng = [90,180,270,360]
        for br in brng:
            print(br)
            (lat,lon) = reversehaversine(latitude,longitude,halfradius,br)
            res = getAllHospitalsWithinRange(lat,lon,halfradius)
            hospitals.extend(res)
        print("added " + str(len(res)) + " of " + str(len(hospitals)) + " current total hospitals ") 
        return hospitals
        
        
    print("returning " + str(len(hospitals)) + " hospitals")        
    return hospitals

# haversine formula reversed
# current function is strongly based on http://stackoverflow.com/questions/7222382/get-lat-long-given-current-point-distance-and-bearing
# bearing (in radians, clockwise from north)
def reversehaversine(lat,lon,d,brng):
    R = 6371.0      #Radius of the Earth from wikipedia
    brng = math.radians(brng)
    d = d/1000

    lat1 = math.radians(float(lat)) #Current lat point converted to radians
    lon1 = math.radians(float(lon)) #Current long point converted to radians

    lat2 = math.asin( math.sin(lat1)*math.cos(d/R) + math.cos(lat1)*math.sin(d/R)*math.cos(brng))
    
    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1), math.cos(d/R)-math.sin(lat1)*math.sin(lat2))
    
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    
    print(lat2)
    print(lon2)   
    
    return (lat2, lon2)
    
 
# example call
latitude = 38.0000
longitude = -97.0000
radius = 50000

hosp = getAllHospitalsWithinRange(latitude, longitude, radius);
print(len(hosp))


#reversehaversine(1,1,1,1)
#res = getHospitalsWithinRange(latitude, longitude, radius, '');
#result = fetchHospitalResult(res)
#print(result)
#print(len(result))
#myhospitals = getAllHospitalsWithinRange(latitude, longitude, radius)
#print(myhospitals)

#if(res['status'] == 'REQUEST_DENIED'):
#    print "REQUESTERROR: Please check you request"
