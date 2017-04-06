from urllib2 import urlopen
from lxml import html
import sys
from threading import Thread
import time
import hospitalstats
import csv

def page(i): return 'https://www.northwell.edu/find-care/find-a-doctor?zip=New%20York&page=' + str(i)

def subpage(relative): return 'https://www.northwell.edu' + relative

# Main Pages with pagination
# Extracts names and path for detail page
def getNameAndSubpage(start, end):
    subpages = []
    names = []
    for i in range(start,end):
        data = str(urlopen(page(i)).read())
        tree = html.fromstring(data)
        subpages = subpages + tree.xpath('//h3[@class="result__title"]/a/@href')
        names = names + tree.xpath('//h3[@class="result__title"]/a/text()')
    return zip(names,subpages)


# Subpage scan
# Extracts speciality and residencies
def getSpecialityAndResidencies(relativePath):
    data = str(urlopen(subpage(relativePath)).read())
    tree = html.fromstring(data)
    speciality = map(lambda s: s.strip(), tree.xpath('.//*[@id="main"]/div/div[1]/div/div[2]/div[1]/div/p[1]/text()'))[0]
    # one doctor might have multiple residencies
    residencies = []
    i = 1
    residency = lambda i: tree.xpath('//*[@id="section-credentials"]/ul[3]/li['+str(i)+']/text()')
    r = residency(1)
    while r:
        residencies = residencies + r
        i += 1
        r = residency(i)
    return (speciality, residencies)


def printDoctorsByPageTSV(start, end):
    for i in range(start, end):
        for (name, relativePath) in getNameAndSubpage(i,i+1):
            (speciality, residencies) = getSpecialityAndResidencies(relativePath)
            rs = ', '.join(residencies)
            print name + '\t' + speciality + '\t' + rs + '\t' + relativePath
            sys.stdout.flush()


def crawl():
    # Sequential
    # printDoctorsByPageTSV(1,100)
    # printDoctorsByPageTSV(100,200)
    # printDoctorsByPageTSV(200,300)
    # printDoctorsByPageTSV(300,400)
    # printDoctorsByPageTSV(400,500)
    # printDoctorsByPageTSV(500,600)
    # printDoctorsByPageTSV(600,660)

    # Concurrent
    Thread(target = printDoctorsByPageTSV, args = (1,100)).start()
    Thread(target = printDoctorsByPageTSV, args = (100,200)).start()
    Thread(target = printDoctorsByPageTSV, args = (200,300)).start()
    Thread(target = printDoctorsByPageTSV, args = (300,400)).start()
    Thread(target = printDoctorsByPageTSV, args = (400,500)).start()
    Thread(target = printDoctorsByPageTSV, args = (500,600)).start()
    Thread(target = printDoctorsByPageTSV, args = (600,660)).start()

def mapNameToLocation(name):
    locations = (hospitalstats.getLocations('ny', False))
    #loadTfidf(locations) # doesnt work
    keys = [ k for k in locations ]
    return hospitalstats.mostSimilar(hospitalstats.ratcliffObershelpSimilarity(name, keys))
    #print hospitalstats.mostSimilar(hospitalstats.levenshteinSimilarity(name.lower(), keys))

def mapNamesToLocation(path):
    with open(path,'rb') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
            hospital = row[2]
            mapping = mapNameToLocation(hospital)
            if mapping[1] > 0.80:
                print hospital + ': ' + str(mapping)

def main():
    #crawl() # done
    mapNamesToLocation('northwell.tsv')

main()
