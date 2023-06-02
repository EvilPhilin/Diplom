from StopInfo import OriginStopNeighbors


class NeighborsMatrix:
    def __init__(self, stopsList):
        numberOfStops = len(stopsList)

        self.originStopsList = [OriginStopNeighbors(stopsList[i].id, stopsList[i].name) for i in range(numberOfStops)]
        self.numberOfStops = numberOfStops

    def calculateNeighbors(self, graph, stopsIDs):
        for i in range(self.numberOfStops):
            originID = self.originStopsList[i].id

            stopsList = []
            visitedList = []
            generalList = list(graph.neighbors(int(originID)))

            visitedList.append(originID)

            while len(generalList) > 0:
                node = generalList.pop(0)

                if node in visitedList:
                    continue
                visitedList.append(node)

                if node in stopsIDs:
                    stopsList.append(node)

                else:
                    newNeighbors = list(graph.neighbors(node))
                    for n in newNeighbors:
                        generalList.append(n)

            self.originStopsList[i].neighbors = stopsList

    def print(self):
        for i in range(self.numberOfStops):
            print(
                self.originStopsList[i].id,
                self.originStopsList[i].name,
                end=' '
            )

            print(len(self.originStopsList[i].neighbors))
            for j in self.originStopsList[i].neighbors:
                print(j, end=' ')

            print()
