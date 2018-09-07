import urllib.request, csv
from urllib.parse import urlencode
from xml.dom.minidom import parse, parseString
from math import sqrt, cos, radians

class aircraftData:
    pass

class jobs:
    pass

def domParse(link):
    #Parse requested data from the FSE API
    dom = parse(urllib.request.urlopen(link))
    return dom

def getValue(node, index):
    #Fetch data from nodes in a less tedious way
    value = node.childNodes[index].childNodes[0].nodeValue
    return value

def airportDat(icao):
    #Get data about the required airport
    with open('icaodata.csv') as csvfile:
        index = csv.reader(csvfile, delimiter=',')
        for row in index:
            if row[0] == icao:
                lat = float(row[1])
                long = float(row[2])
    return lat, long

def airportDist(icaoDep, icaoDest):
    #Get the distance between two aiports
    icaoDep = airportDat(icaoDep)
    icaoDest = airportDat(icaoDest)
    distLong = cos(radians(icaoDep[0]+icaoDest[0])/2)*60
    dist = sqrt(((icaoDest[0]-icaoDep[0])*60)**2+((icaoDest[1]-icaoDep[1])*distLong)**2)
    return dist

def jobCollect(icao):
    pass

MakeModel = str(input("Input MakeModel: "))

aircraft = domParse("http://server.fseconomy.net/data?userkey=564BRJV514&format=xml&query=aircraft&search=configs")
aircraftTypes = aircraft.getElementsByTagName('MakeModel')

for a in aircraftTypes:
	if a.childNodes[0].nodeValue == MakeModel:
		aircraftType = a.parentNode

for a in aircraftType.childNodes:
    if a.nodeValue != '\n':
        exec("aircraftData." + a.nodeName + " = \'" + a.childNodes[0].nodeValue +"\'")

airports = domParse('http://server.fseconomy.net/data?userkey=564BRJV514&format=xml&query=aircraft&search=makemodel&' + urlencode({'makemodel' : MakeModel}))
airportNames = airports.getElementsByTagName('Location')

icao = set()

for a in airportNames:
    if (float(a.parentNode.childNodes[21].childNodes[0].nodeValue) != 0 or float(a.parentNode.childNodes[23].childNodes[0].nodeValue)) != 0 and a.parentNode.childNodes[31].childNodes[0].nodeValue == 'Not rented.' and int(a.parentNode.childNodes[41].childNodes[0].nodeValue.partition(':')[0]) < 95 and a.childNodes[0].nodeValue != 'In Flight':
        icao.add(a.childNodes[0].nodeValue)

icao = sorted(icao)

for i in icao:
    pass
