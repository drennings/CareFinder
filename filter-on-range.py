import csv
import sys
from math import sin, cos, sqrt, atan2, radians
from decimal import *

# Parameter to be set in advance
latColumn = 5;
longColumn = 6;

# Parameters to acquire from user input per call
pathToSource = ''		# Relative path to source file with all available hospitals
pathToDestination = ''	# Relative path to destination file with hospitals within range (overwritten!)
range = 0;				# Range in kilometers
originLat = 0.0;		# User position expressed in latitude
originLong = 0.0;		# User position expressed in longitude

# Get needed user input if possible
try:
	pathToSource = sys.argv[1]
	pathToDestination = sys.argv[2]
	range = Decimal(sys.argv[3])
	originLat = radians(Decimal(sys.argv[4]))
	originLong = radians(Decimal(sys.argv[5]))
except IndexError:
    print "INPUTERROR: Please provide the needed input and make a call in the form: \n filter-on-range.py <pathToSource> <pathToDestination> <range> <originLat> <originLong>"
	
# Writes all entries in pathToSource that have a lat lon withing range from origin to pathToDestination 
def filterOnRange(range, originLat, originLong):
    with open(pathToSource, 'r') as tsvin, open(pathToDestination,'wb') as tsvout:
		tsvin = csv.reader(tsvin, delimiter='\t')
		tsvout = csv.writer(tsvout, delimiter='\t')
        
		for entry in tsvin:
			entryLat = radians(float(entry[latColumn]))
			entryLong = radians(float(entry[longColumn]))
			
			distance = calculateDistance(range, originLat, originLong, entryLat, entryLong)
			
			if distance <= range:
				# print entry
				tsvout.writerow(entry)

# Returns whether distance between origin and destination <= range
def calculateDistance(range, originLat, originLong, destinationLat, destinationLong):
# PLEASE NOTE: Code strongly based upon http://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
	R = 6371.0 # #Radius of the Earth from Wikipedia
	
	dlon = destinationLong - originLong
	dlat = destinationLat - originLat

	a = sin(dlat / 2)**2 + cos(originLat) * cos(destinationLat) * sin(dlon / 2)**2		# apply the haversine formula
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c

	return distance

# Code to EXECUTE
filterOnRange(range, originLat, originLong)

# DEPRECATED Test TODO
#def testFilterOnRange
#pathToSource = "northwell-located.tsv"					# Source file with all available hospitals
#pathToDestination = "northwell-located-filtered.tsv"	# Destination file with hospitals within range (overwritten!)
#range
#originLat
#originLong
#filterOnRange(5000,2,3)

# Test a regular case
def testCalculateDistance():
	lat1 = radians(52.2296756)
	lon1 = radians(21.0122287)
	lat2 = radians(52.406374)
	lon2 = radians(16.9251681)
	testresult = calculateDistance(5,lat1,lon1,lat2,lon2)
	print testresult == 278.54558935106695
	return testresult == 278.54558935106695