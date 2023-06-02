class StopData:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class OriginStop(StopData):
    def __init__(self, id, name, numberOfStops):
        self.id = id
        self.name = name
        self.destinationStopsList = [0 for i in range(numberOfStops)]
        self.leavingPassangersCnt = 0


class OriginStopNeighbors(StopData):
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.neighbors = []
