import json
import os
import sys
import codecs
import tfidf
from difflib import SequenceMatcher
import Levenshtein
import csv

# Initially created by Daan, modified by Marc
# This function returns all the hospitals including lat/lon from the collected hospitals from FourSquare
def getFourSquareLocations(path, doPrint):
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)
    sys.stderr = codecs.getwriter('utf8')(sys.stderr)

    noURLcounter = 0
    noContactcounter = 0
    hospitalcounter = 0
    citycounter = 0

    files = {}
    wrongfiles = []
    goodfiles = []
    defaultUrl = '/'
    root = ''
    # Traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk(path):
        continue

    # Drop error files, keep good files
    for filename in files:
        if filename.startswith('error') or not filename.endswith('.json'):
            wrongfiles.append(filename)
        else:
            goodfiles.append(filename)

    locations = {}
    for filename in goodfiles:
        filename = path + '/' + filename
        with open(filename, 'r') as f:
            data = json.load(f)

        response = data['response']
        citycounter += 1

        for venue in response['venues']:
                hospitalcounter += 1
                referralId = venue['referralId']
                name = venue['name']
                latitude = venue['location']['lat']
                longitude = venue['location']['lng']
                contact = venue['contact']
                if not contact:
                    noContactcounter += 1
                url = defaultUrl
                if 'url' not in venue:
                    noURLcounter += 1
                else:
                    url = venue['url']
                    #print url

                #sys.stdout.write("{0} - {1} - ({2}, {3}) - {4}".format(referralId, name, latitude, longitude, url))
                if doPrint:
                    print (name + "\t" + str(latitude) + "\t" + str(longitude) + "\t" + url)
                locations[name] = (latitude, longitude)

    if doPrint:
        print("Amount of cities: {0}".format(len(files)))
        print("Amount of cities inspected: {0}".format(citycounter))
        print("Amount of cities NOT inspected: {0}".format(len(wrongfiles)-citycounter))
        print("Amount of (potential duplicate) hospitals found: {0}".format(hospitalcounter))
        print("Amount of (potential duplicate) hospitals that do not have a URL: {0}".format(noURLcounter))
        print("Amount of (potential duplicate) hospitals with NO contact details: {0}".format(noContactcounter))
    
    return locations

def getGooglePlacesLocations(path):
    f = codecs.open(path, 'rU','utf-8')
    tsvin = csv.reader(f, delimiter='\t')
    locations = {};
            
    for entry in tsvin:
        name = entry[1]
        latitude = entry[3]
        longitude = entry[4]
        locations[name] = (latitude, longitude)
        
    return locations

def getLocations(foursquarePath, doPrint, googlePath):
    locationsFourSquare = getFourSquareLocations(foursquarePath, doPrint);
    locationsGooglePlaces = getGooglePlacesLocations(googlePath);
    locations = locationsFourSquare.copy();
    #locations.update(locationsGooglePlaces);
    return locations
    
# Doesnt seem to work
def loadTfidf(locations):
    table = tfidf.tfidf()
    for l in locations:
        print l.split(" ")
        table.addDocument(l, ' '.split(l))
    print '\nPREDICT:'
    for f in table.similarities(['Fillmore']):
        if f[1] > 0:
            print f

def ratcliffObershelp(a, b):
    return SequenceMatcher(None, a, b).ratio()

def ratcliffObershelpSimilarity(word, keys):
    return map(lambda k: (k, ratcliffObershelp(word, k)), keys)

def levenshtein(a, b):
    return Levenshtein.ratio(unicode(a),unicode(b))

def levenshteinSimilarity(word, keys):
    return map(lambda k: (k, levenshtein(word, k)), keys)

def mostSimilar(similarities):
    return max(similarities, key=lambda x:x[1])


def main():
    # Example
    locations = (getLocations('ny', False, 'allHospitalDetails_in_NY-filtered.tsv'))
    #loadTfidf(locations) # doesnt work
    keys = [ k.lower() for k in locations ]
    print keys;
    toFind = 'Staten Island University Hospital'
    print mostSimilar(ratcliffObershelpSimilarity(toFind.lower(), keys))
    print mostSimilar(levenshteinSimilarity(toFind.lower(), keys))

main()
