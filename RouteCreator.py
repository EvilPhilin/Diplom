from Route import Route


class RouteCreator:
    def __init__(self):
        self.possibleRoutes = []
        self.bestRoute = []

    def findAllPossibleRoutes(self, stopsDict, trafficMatrix, distanceMatrix, neighborsMatrix, currList, currentLength, currentTraffic):
        lengthLimit = 6000.

        if currentLength > lengthLimit:
            self.possibleRoutes.append(Route(currList, currentTraffic, currentLength))
            return

        lastAddedStop = currList[-1]
        posOfLastAddedStop = int(stopsDict[str(lastAddedStop)])

        for neighbor in neighborsMatrix.originStopsList[posOfLastAddedStop].neighbors:
            if neighbor not in currList:
                posOfNeighbor = int(stopsDict[str(neighbor)])
                additionalLength = float(distanceMatrix.originStopsList[posOfLastAddedStop].destinationStopsList[posOfNeighbor])

                additionalTraffic = 0
                for i in currList:
                    posOfI = stopsDict[str(i)]
                    additionalTraffic += trafficMatrix.originStopsList[posOfI].destinationStopsList[posOfNeighbor]
                    additionalTraffic += trafficMatrix.originStopsList[posOfNeighbor].destinationStopsList[posOfI]

                newList = currList.copy()
                newList.append(neighbor)

                newLength = currentLength + additionalLength
                newTraffic = currentTraffic + additionalTraffic

                self.findAllPossibleRoutes(stopsDict, trafficMatrix, distanceMatrix, neighborsMatrix, newList, newLength, newTraffic)

    def findBestRoute(self):
        maxTraffic = 0
        bestRoutePos = 0

        for i in range(len(self.possibleRoutes)):
            if maxTraffic < self.possibleRoutes[i].traffic:
                maxTraffic = self.possibleRoutes[i].traffic
                bestRoutePos = i

        self.bestRoute = self.possibleRoutes[bestRoutePos]
