import csv

def convert(tude):
    multiplier = 1 if tude[-1] in ['N', 'E'] else -1
    return multiplier * sum(float(x) / 60 ** n for n, x in enumerate(tude[:-1].split('-')))

#print "20-55N:", convert("20-55N")
#print "32-11W:", convert("32-11-50.000W")

with open('cities-usa.tsv','rb') as tsvin:
    tsvin = csv.reader(tsvin, delimiter='\t')
    for row in tsvin:
        city = row[0]
        lat = convert(row[1])
        lon = convert(row[2])
        print city + ": " + str(lat) + ", " +str(lon)
