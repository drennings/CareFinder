from __future__ import print_function
import hospitalstats
import csv

def mapNameToLocation(name, locations):
    #return hospitalstats.mostSimilar(hospitalstats.ratcliffObershelpSimilarity(name, locations))
    return hospitalstats.mostSimilar(hospitalstats.levenshteinSimilarity(name, locations))

def mapNamesToLocation(path, threshold):
    print('test')
    tsvout = open('stcatherines.tsv', 'w')
    #tsvout.write('name' + '\t' + 'speciality' + '\t' + 'hospital' + '\t' + 'mapped' + '\t' + 'ratio' + '\t' + 'lat' + '\t' + 'lon' + '\t' + 'url'+ '\t' + 'doctorsLocations' +'\n')
    locations = (hospitalstats.getLocations('ny', False))
    keys = [ k for k in locations ]
    with open(path,'rt') as csvin:
        csvin = csv.reader(csvin)
        for row in csvin:
            try:
                name = row[0]
                speciality = row[1]
                hospital = row[2]
                url = row[4]
                doctorsLocation = row[3]
                (mapped, ratio) = mapNameToLocation(hospital, keys)
                (lat, lon) = locations[mapped]
                if ratio > threshold:
                    #print hospital + ': ' + str(mapped) + ', ' + str(ratio)
                    tsvout.write(name + '\t' + speciality + '\t' + hospital + '\t' + mapped + '\t' + str(ratio) + '\t' + str(lat) + '\t' + str(lon) + '\t' + url+ '\t' + doctorsLocation +'\n')
                    #print(name + '\t' + speciality + '\t' + hospital + '\t' + mapped + '\t' + str(ratio) + '\t' + str(lat) + '\t' + str(lon)+ + '\t' + str(url)+ '\t' + str(doctorsLocation), file=tsvout)
            except:
                raise

def main():
    #crawl() # done
    mapNamesToLocation('stcatherines.csv', -0.10)

main()
