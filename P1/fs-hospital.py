import csv
import json
import requests

category = "4bf58dd8d48988d196941735" #hospital
token = "yourtoken"

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


with open('cities-usa.tsv','rb') as tsvin:
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
