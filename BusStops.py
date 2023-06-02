import xml.etree.ElementTree as et
from StopInfo import StopData


class BusStopList:
    def __init__(self):
        self.stops = []

    def getStopsFromOSM(self, pathToFile):
        tree = et.parse(pathToFile)
        root = tree.getroot()

        for child in root:
            stopID = child.attrib.get('id')
            for tag in child:
                if tag.attrib['k'] == 'name':
                    stopName = tag.attrib['v']

            self.stops.append(StopData(stopID, stopName))

    def createDictionary(self):
        dict = {}
        for i in range(len(self.stops)):
            dict[self.stops[i].id] = i

        return dict
