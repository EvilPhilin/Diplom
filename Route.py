import xml.etree.ElementTree as et
import osmnx as ox

class Route:
    def __init__(self, stopsList, traffic, length, numOfBusses=1):
        self.stopsList = stopsList
        self.traffic = traffic
        self.length = length
        # Время в минутах. Считается, что он стоит на каждой остановке одну минуту
        self.lapseTime = length / 600. + len(stopsList)
        self.numOfBusses = numOfBusses

    def assignFrequency(self, stopsDict, trafficMatrix):
        desiredPassengersPerBus = 50
        desiredTimeWaiting = 5

        maxPassengersPerBus = 0
        currPassengersPerBus = 0
        for i in range(len(self.stopsList)):
            posOfI = stopsDict[str(self.stopsList[i])]

            # Вошедшие пассажиры
            for j in range(i + 1, len(self.stopsList)):
                posOfJ = stopsDict[str(self.stopsList[j])]
                currPassengersPerBus += trafficMatrix.originStopsList[posOfI].destinationStopsList[posOfJ]

            # Вышедшие пассажиры
            for j in range(i):
                posOfJ = stopsDict[str(self.stopsList[j])]
                currPassengersPerBus -= trafficMatrix.originStopsList[posOfJ].destinationStopsList[posOfI]

            maxPassengersPerBus = max(maxPassengersPerBus, currPassengersPerBus)

        score = min(desiredTimeWaiting / self.lapseTime / self.numOfBusses, 1) * \
                (1 - abs(maxPassengersPerBus / self.numOfBusses - desiredPassengersPerBus) / desiredPassengersPerBus)

        newBusNumber = self.numOfBusses
        while True:
            newBusNumber += 1
            newScore = min(desiredTimeWaiting / self.lapseTime / newBusNumber, 1) * \
                       (1 - abs(maxPassengersPerBus / newBusNumber - desiredPassengersPerBus) / desiredPassengersPerBus)

            delta = newScore - score

            if delta > 0:
                self.numOfBusses = newBusNumber
                score = newScore
            else:
                break

    def writeToOSM(self, graph, idOSM):
        fullListOfNodes = []

        # Ноды
        for i in range(len(self.stopsList) - 1):
            pathToNextStop = ox.shortest_path(graph, int(self.stopsList[i]), int(self.stopsList[i+1]))
            for j in range(len(pathToNextStop) - 1):
                fullListOfNodes.append(pathToNextStop[j])

        fullListOfNodes.append(self.stopsList[-1])

        # Дороги
        fullListOfRoads = []
        for i in range(len(fullListOfNodes) - 1):
            road = graph.get_edge_data(fullListOfNodes[i], fullListOfNodes[i + 1])[0]["osmid"]
            if road not in fullListOfRoads:
                fullListOfRoads.append(road)

        relation = et.Element("relation")
        relation.set("id", str(idOSM))
        relation.set("version", "1")

        tag = et.SubElement(relation, "tag")
        tag.set("k", "type")
        tag.set("v", "route")
        tag = et.SubElement(relation, "tag")
        tag.set("k", "route")
        tag.set("v", "bus")
        tag = et.SubElement(relation, "tag")
        tag.set("k", "numOfBusses")
        tag.set("v", str(self.numOfBusses))
        tag = et.SubElement(relation, "tag")
        tag.set("k", "length")
        tag.set("v", str(self.length))
        tag = et.SubElement(relation, "tag")
        tag.set("k", "traffic")
        tag.set("v", str(self.traffic))

        for i in fullListOfNodes:
            member = et.SubElement(relation, "member")
            member.set("type", "node")
            member.set("ref", str(i))
            member.set("role", "inner")

        for i in fullListOfRoads:
            member = et.SubElement(relation, "member")
            member.set("type", "way")
            member.set("ref", str(i))
            member.set("role", "inner")

        with open("output.xml", "a") as f:
            f.write(f"{et.tostring(relation)}\n")
