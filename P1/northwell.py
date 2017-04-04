from urllib2 import urlopen
from lxml import html

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
            print name + "\t" + speciality + "\t" + rs

printDoctorsByPageTSV(1,100)
