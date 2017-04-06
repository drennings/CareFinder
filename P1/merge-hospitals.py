import json
import os
import sys
import codecs
import csv

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

noURLcounter = 0
noContactcounter = 0
hospitalcounter = 0
citycounter = 0

files = {}
wrongfiles = []
goodfiles = []
root = ''

def storeHospital(hospitalobject):
    with open('duplicateHospitals.csv', 'ab') as csvfile:
        fieldnames = ['referralId', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,dialect='excel')
        writer.writerow({'referralId': hospitalobject['referralId'], 'name': hospitalobject['name']})

    with open('duplicateHospitals.csv','r') as in_file, open('singleHospitals.csv','w') as out_file:
        seen = set() # set for fast O(1) amortized lookup
        for line in in_file:
            if line in seen: continue # skip duplicate

            seen.add(line)
            out_file.write(line)

    return


# Traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk("./collectionT/"):
    continue

# Drop error files, keep good files
for filename in files:
    if filename.startswith('error') or not filename.endswith('.json'):
        wrongfiles.append(filename)
    else:
        goodfiles.append(filename)

for filename in goodfiles:
    filename = './collectionT/' + filename
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
	    else:
	        #print contact

		url = '/'
	    if 'url' not in venue:
			noURLcounter += 1
	    else:
	        url = venue['url']

	    hospitalObject = {'referralId': referralId, 'name': name}
	    storeHospital(hospitalObject)
	    #sys.stdout.write("{0} - {1} - ({2}, {3}) - {4}".format(referralId, name, latitude, longitude, url))

print("Amount of cities: {0}".format(len(files)))
print("Amount of cities inspected: {0}".format(citycounter))
print("Amount of cities NOT inspected: {0}".format(len(wrongfiles)-citycounter))

print("Amount of (potential duplicate) hospitals found: {0}".format(hospitalcounter))
print("Amount of (potential duplicate) hospitals that do not have a URL: {0}".format(noURLcounter))
print("Amount of (potential duplicate) hospitals with NO contact details: {0}".format(noContactcounter))
