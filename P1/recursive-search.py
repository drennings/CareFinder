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
entityType = 'hospital'

# Get user key if provided, else ask for it
try:
    key = sys.argv[1]
except IndexError:
    print "INDEXERROR: Please provide your API key"

# Return a list of jsonresults given the paramaters to Google Places
def getHospitalsWithinRange(latitude, longitude, radius, nextpagetoken):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/' + output + '?location=' + str(latitude) + ',' + str(longitude) + '&radius=' + str(radius) +'&type=' + entityType + '&key=' + key + '&pagetoken=' + str(nextpagetoken)
    #print((50000/radius-1)*'\t' + url)	
    print url
    r = requests.get(url)
    jsonresult = r.json()   # dict object
    
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
		radius = radius/2
		print(radius)
		#brng = [22.5,67.5,112.5,157.5]
		brng = [45.0,135.0,225.0,315.0]
		#brng = [45,90,135,180]
		#brng = [90,180,270,360]
		localhospitals = []
		for br in brng:
			print(br)
			(lat,lon) = reversehaversine(latitude,longitude,radius,br)
			res = getAllHospitalsWithinRange(lat,lon,radius)
			localhospitals.extend(res)
		print("added " + str(len(res)) + " of " + str(len(localhospitals)) + " current total hospitals ") 
		return localhospitals
	else:
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

# Get all hospitals within a square with center (latitude, longitude)
# Through an exhaustive recursive call
def getMyHospitals(latitude, longitude, radius):
    hosps = []
    if(radius <= 50000):
        print('found radius <= 50000!')
        res = getAllHospitalsWithinRange(latitude,longitude,radius)
        print(type(res))
        hosps.extend(res)
        return hosps;
    else:	
        print('found radius > 50000!')
        radius = radius/2
        print(radius)
        brng = [45.0,135.0,225.0,315.0]
        for br in brng:
            print(br)
            (lat,lon) = reversehaversine(latitude,longitude,radius,br)
            res = getAllHospitalsWithinRange(lat,lon,radius)
            hosps.extend(res)
	return hosps;

def writeUniqueIDsToFile(data, pathToFile):
    with open(pathToFile,'wb') as tsvout:
		tsvout = csv.writer(tsvout, delimiter='\t')
		print("Original set size (with duplicates) = " + str(len(data)) )
		idList = [];
 		for hospital in data:
			idList.append(hospital.get('place_id'))
		idSet = set(idList);
		print("New set size (without duplicates = " + str(len(idSet)) )
		for id in idSet:
			tsvout.writerow([id]) #write complete ID in first column
			

# example call
latitude = 38.0000
longitude = -97.0000
radius = 50000

# example call - 0 hospitals
latitude = 38.0000
longitude = -97.0000
radius = 10000

# example call - 10 hospitals
latitude = 38.0000
longitude = -97.0000
radius = 30000

# example call - 2 hospitals
latitude = 38.0000
longitude = -97.0000
radius = 24000

# call for NY
latitude = 40.730610
longitude = -73.935242
radius = 200000

# MAIN function calls
hosp = [];
hosp.extend(getMyHospitals(latitude, longitude, radius));
#hosp.extend(getAllHospitalsWithinRange(latitude, longitude, radius));
print('Found ' + str(len(hosp)) + " hospitals")
writeUniqueIDsToFile(hosp, 'hospitalIDs.tsv')


#t = type(hosp)
#print t




#reversehaversine(1,1,1,1)
#res = getHospitalsWithinRange(latitude, longitude, radius, '');
#result = fetchHospitalResult(res)
#print(result)
#print(len(result))
#myhospitals = getAllHospitalsWithinRange(latitude, longitude, radius)
#print(myhospitals)

#if(res['status'] == 'REQUEST_DENIED'):
#    print "REQUESTERROR: Please check you request"
