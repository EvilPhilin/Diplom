import osmnx as ox
from Route import Route
from RouteCreator import RouteCreator
from BusStops import BusStopList
from TrafficMatrix import TrafficMatrix
from DistanceMatrix import DistanceMatrix
from NeighborsMatrix import NeighborsMatrix

pathToStops = "C:/Users/kurdj/Desktop/Diplom/pythonProject/Data/stopsOnlyMap.osm"
pathToMap = "C:/Users/kurdj/Desktop/Diplom/pythonProject/Data/BaseKalOsm.osm"
passengersThreshold = 50

ox.config(log_console=True, use_cache=True)

graph = ox.graph_from_xml(pathToMap, simplify=False)

bsl = BusStopList()
bsl.getStopsFromOSM(pathToStops)
stopsIDs = [int(i.id) for i in bsl.stops]
stopsDict = bsl.createDictionary()

tm = TrafficMatrix(bsl.stops)
tm.fillWithRng() # 1901

dm = DistanceMatrix(bsl.stops)
dm.readFromFile()

nm = NeighborsMatrix(bsl.stops)
nm.calculateNeighbors(graph, stopsIDs)

# Из-за того что матрица трафика содержит слишком большое количесвто пассажиров, в результате мы бы получили очень большое
# количесвто маршрутов. Ограничимся 50-ю для демонстрации
for i in range(1, 51):
    originStop = tm.findMaxLeavingPassengers()["stop"]

    rc = RouteCreator()
    rc.findAllPossibleRoutes(stopsDict, tm, dm, nm, [originStop.id], 0., 0.)
    rc.findBestRoute()
    rc.bestRoute.assignFrequency(stopsDict, tm)
    rc.bestRoute.writeToOSM(graph, i)
    tm.removeTrafficFromCreatedRoute(stopsDict, rc.bestRoute.stopsList)
    print(i)
