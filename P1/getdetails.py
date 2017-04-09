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

# Counter
i = 0;

# Get user key if provided, else ask for it
try:
    key = sys.argv[1]
except IndexError:
    print "INDEXERROR: Please provide your API key"

# Return the jsonresult given by Google Places for the placeID
def getHospitalDetails(placeID):
    url = 'https://maps.googleapis.com/maps/api/place/details/' + output + '?placeid=' + str(placeID) + '&key=' + key	
    print url
    r = requests.get(url)
    jsonresult = r.json()   # dict object
    if(jsonresult['status'] != 'OK'):
        print 'ERROR: ' +  jsonresult['status'] + ' / ' + jsonresult['error_message'] + ' @ ' + url
    return jsonresult;

# Write data headers
def writeHeaders(pathToDestination,headers):
    with open(pathToDestination,'a') as tsvout:
        tsvout = csv.writer(tsvout, delimiter='\t')
        tsvout.writerow(headers)                                                # TODO set header values

# From all details return a list of needed details (should comply with headers)
def getNeededDetails(allDetails):
    allDetails = allDetails['result']
    result = []

    # Fill in available data per header
    for header in headers:
        if header in allDetails:
            result.append(allDetails[header])
        else:
            result.append('')
    
    # Get lat and long from geometry (deeper into the JSON object)
    latitudeIndex = headers.index('latitude')
    result[latitudeIndex] = allDetails['geometry']['location']['lat']
    result[latitudeIndex+1] = allDetails['geometry']['location']['lng']
    
    return result;
    
# Return a list of jsonresults given the paramaters to Google Places
def writeHospitalDetails(pathToSource,pathToDestination):           # TODO fix good entry in wb
    with open(pathToSource, 'r') as tsvin, open(pathToDestination,'a') as tsvout:
		tsvin = csv.reader(tsvin, delimiter='\t')
		tsvout = csv.writer(tsvout, delimiter='\t')
        
		for entry in tsvin:
			global i 
			i = i + 1
			print i     # show at which entry we are
			placeID = entry[0]
			#print(placeID)
			hospitalDetails = getHospitalDetails(placeID);
			#print(hospitalDetails)
			neededDetails = getNeededDetails(hospitalDetails);
			#print(neededDetails)
			tsvout.writerow(neededDetails)

# MAIN code
headers = ['place_id', 'name', 'formatted_address', 'latitude', 'longitude', 'formatted_phone_number', 'international_phone_number', 'website', 'opening_hours', 'permanently_closed', 'price_level', 'rating', 'url', 'utc_offset', 'vicinity'] 
pathToDestination = 'details.tsv'
pathToSource = 'header.tsv'
writeHeaders(pathToDestination, headers)
writeHospitalDetails(pathToSource,pathToDestination)

#hospitalDetails = getHospitalDetails('ChIJ0z3FGguzu4cRnV4Ce0PzzfQ')
#print hospitalDetails
#neededDetails = getNeededDetails(hospitalDetails)
#print neededDetails

#writeHospitalDetails('hospitalIDs.tsv', 'hospitalDetails.tsv')





