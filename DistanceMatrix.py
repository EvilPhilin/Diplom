from StopInfo import OriginStop
import osmnx as ox
import csv


class DistanceMatrix:
    def __init__(self, stopsList):
        numberOfStops = len(stopsList)

        self.originStopsList = [OriginStop(stopsList[i].id, stopsList[i].name, numberOfStops) for i in range(numberOfStops)]
        self.numberOfStops = numberOfStops

    def calculateDistances(self, graph):
        for i in range(self.numberOfStops):
            origin = [int(self.originStopsList[i].id)] * self.numberOfStops
            dest = []
            for j in range(self.numberOfStops):
                dest.append(int(self.originStopsList[j].id))

            routes = ox.shortest_path(graph, origin, dest)

            for j in range(self.numberOfStops):
                self.originStopsList[i].destinationStopsList[j] = self.calculateRouteLen(graph, routes[j])

    def calculateRouteLen(self, graph, route):
        totalLen = 0
        for i in range(len(route) - 1):
            totalLen += graph.get_edge_data(route[i], route[i + 1])[0]['length']

        return totalLen

    def writeToFile(self):
        with open("C:/Users/kurdj/Desktop/Diplom/pythonProject/Data/distances.txt", "w", encoding='UTF8') as f:
            writer = csv.writer(f)

            for i in range(self.numberOfStops):
                row = [self.originStopsList[i].id, self.originStopsList[i].name]
                for j in self.originStopsList[i].destinationStopsList:
                    row.append(j)

                writer.writerow(row)

    def readFromFile(self):
        with open("C:/Users/kurdj/Desktop/Diplom/pythonProject/Data/distances.txt", "r", encoding='UTF8') as f:
            reader = csv.reader(f)

            i = 0
            for row in reader:
                if len(row) != 0:
                    self.originStopsList[i].id = row[0]
                    self.originStopsList[i].name = row[1]
                    for j in range(self.numberOfStops):
                        self.originStopsList[i].destinationStopsList[j] = row[j + 2]
                    i += 1

    def print(self):
        for i in range(self.numberOfStops):
            print(
                self.originStopsList[i].id,
                self.originStopsList[i].name,
                self.originStopsList[i].leavingPassangersCnt,
                end=' '
            )

            for j in range(self.numberOfStops):
                print(self.originStopsList[i].destinationStopsList[j], end=' ')

            print()