import random
from StopInfo import OriginStop


class TrafficMatrix:
    def __init__(self, stopsList):
        numberOfStops = len(stopsList)

        self.originStopsList = [OriginStop(stopsList[i].id, stopsList[i].name, numberOfStops) for i in range(numberOfStops)]
        self.numberOfStops = numberOfStops

    def fillWithRng(self, seed=144):
        random.seed(seed)

        for i in range(self.numberOfStops):
            passCnt = 0
            for j in range(self.numberOfStops):
                if i != j:
                    rngInt = random.randint(0, 5)
                    passCnt += rngInt
                    self.originStopsList[i].destinationStopsList[j] = rngInt

            self.originStopsList[i].leavingPassangersCnt = passCnt

    def findMaxLeavingPassengers(self):
        maxPass = 0
        for i in range(len(self.originStopsList)):
            if maxPass < self.originStopsList[i].leavingPassangersCnt:
                maxPass = self.originStopsList[i].leavingPassangersCnt
                indexOfStop = i

        return {"stop": self.originStopsList[indexOfStop], "count": maxPass}

    def removeTrafficFromCreatedRoute(self, stopsDict, route):
        for i in range(len(route)):
            originPos = stopsDict[str(route[i])]
            for j in range(i+1, len(route)):
                destinationPos = stopsDict[str(route[j])]
                self.originStopsList[originPos].destinationStopsList[destinationPos] = 0
                self.originStopsList[destinationPos].destinationStopsList[originPos] = 0

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
