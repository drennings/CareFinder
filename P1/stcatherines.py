from __future__ import print_function
import hospitalstats
import csv

def mapNameToLocation(name, locations):
    #return hospitalstats.mostSimilar(hospitalstats.ratcliffObershelpSimilarity(name, locations))
    return hospitalstats.mostSimilar(hospitalstats.levenshteinSimilarity(name, locations))

def mapNamesToLocation(path, threshold):
    import pandas as pd
    doctors = pd.read_excel('current_data.xlsx')
    
    locations = (hospitalstats.getLocations('ny', False, 'allHospitalDetails_in_NY-filtered.tsv'))
    keys = [ k for k in locations ]
    with open(path,'rt') as csvin:
        csvin = csv.reader(csvin)
        i = 6053;
        for row in csvin:
            name = row[0]
            speciality = row[1]
            hospital = str(row[2]).split(",")
            url = row[4]
            doctorsLocation = row[3]
            for workingplace in hospital:
                (mapped, ratio) = mapNameToLocation(workingplace, keys)
                (lat, lon) = locations[mapped]
                if ratio > threshold:
                    doctors.loc[i,'Name'] = name
                    doctors.loc[i,'Spec'] = speciality
                    doctors.loc[i,'Hosp'] = workingplace
                    doctors.loc[i,'lat'] = lat
                    doctors.loc[i,'lon'] = lon
                    i = i + 1;
                    #print( str(i) + str(name) + str(speciality) + str(hospital) + str(lat) + str(lon) + str(ratio))
    writer = pd.ExcelWriter('current_data.xlsx', engine='xlsxwriter')
    doctors.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    print(doctors)
    return
    
                
def main():
    #crawl() # done
    mapNamesToLocation('stcatherines.csv', 0.9)

main()
