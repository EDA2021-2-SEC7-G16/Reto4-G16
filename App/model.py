"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import math
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import orderedmap as om
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import mapentry as me
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    analyzer = {'airports': None,
                'IATACodes': None,
                'digraphConnections': None,
                'graphConnections': None, 
                'cities': None,
                'latitudeIndex': None}

    analyzer['airports'] = mp.newMap(numelements=15000,
                                     maptype='PROBING',
                                     comparefunction=compareIATACode)

    analyzer['IATACodes'] = mp.newMap(numelements=14000,
                                      maptype='PROBING')

    analyzer['digraphConnections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=100000,
                                              comparefunction=compareIATACode)

    analyzer['graphConnections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=100000,
                                              comparefunction=compareIATACode)

    analyzer['cities'] = mp.newMap(maptype='CHAINING',
                                   loadfactor=4)

    analyzer['latitudeIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareCoordinates)

    return analyzer


# Funciones para agregar informacion al catalogo

def addRoute(analyzer, route):
    origin = route['Departure']
    destination = route['Destination']
    distance = float(route['distance_km'])
    distance = abs(distance)
    addStop(analyzer['digraphConnections'], origin)
    addStop(analyzer['digraphConnections'], destination)
    addConnection(analyzer['digraphConnections'], origin, destination, distance)
    if gr.getEdge(analyzer['digraphConnections'], destination, origin) != None:
        addStop(analyzer['graphConnections'], origin)
        addStop(analyzer['graphConnections'], destination)
        addConnection(analyzer['graphConnections'], origin, destination, distance)
    return analyzer

def addAirport(analyzer, airport):
    if not mp.contains(analyzer['airports'], airport['IATA']):
        mp.put(analyzer['airports'], airport['IATA'], airport)
        addStop(analyzer['digraphConnections'], airport['IATA'])

    mp.put(analyzer['IATACodes'], airport['IATA'], airport)
    updateLatitude(analyzer['latitudeIndex'], airport)

def updateLatitude(latMap, record):
    latitude = round(float(record["Latitude"]), 2)
    if om.isEmpty(latMap) == True or om.contains(latMap, latitude) == False:
        longitude = round(float(record["Longitude"]), 2)
        newLonMap = om.newMap(omaptype='RBT', comparefunction=compareCoordinates)
        tempList = lt.newList("ARRAY_LIST")
        lt.addLast(tempList, record)
        om.put(newLonMap, longitude, tempList)
        om.put(latMap, latitude, newLonMap)

    else:
        longitude = round(float(record["Longitude"]), 2)
        existingLonMap = om.get(latMap, latitude)
        existingLonMap = me.getValue(existingLonMap)
        addOrCreateListInMap(existingLonMap, longitude, record)
        om.put(latMap, latitude, existingLonMap)

    return latMap

def addOrCreateListInMap(lonMap, key, element):
    if om.contains(lonMap, key) == False:
        tempList = lt.newList("ARRAY_LIST")
        lt.addLast(tempList, element)
        om.put(lonMap, key, tempList)

    else:
        couple = om.get(lonMap, key)
        existingList = me.getValue(couple)
        lt.addLast(existingList, element)
        om.put(lonMap, key, existingList)

def addStop(graph, airportID):
    if not gr.containsVertex(graph, airportID):
        gr.insertVertex(graph, airportID)

def addCity(analyzer, city, counter):
    mp.put(analyzer['cities'], "Counter", counter)
    if not mp.contains(analyzer['cities'], city['city']):
        cityList = lt.newList('ARRAY_LIST')
        lt.addLast(cityList, city)
        mp.put(analyzer['cities'], city['city'], cityList)
    else:
        couple = mp.get(analyzer['cities'], city['city'])
        existingList = me.getValue(couple)
        lt.addLast(existingList, city)
        mp.put(analyzer['cities'], city['city'], existingList)
    return analyzer

def addConnection(graph, origin, destination, distance):
    edge = gr.getEdge(graph, origin, destination)
    if edge is None:
        gr.addEdge(graph, origin, destination, distance)

# Funciones ayuda para carga de datos

def formatVertex(route):
    """
    Se formatea el nombre del vértice con el ID de la estación
    seguido de la ruta.
    """
    name = route['Destination'] + '-'
    name = name + route['Airline']
    return name

def cleanServiceDistance(lastFlight, route):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if route['distance_km'] == '':
        route['distance_km'] = 0
    if lastFlight['distance_km'] == '':
        lastFlight['distance_km'] = 0

# Funciones para creacion de datos

# Funciones de consulta

def vertexAmmount(graph):
    return gr.numVertices(graph)

def edgesAmmount(graph):
    return gr.numEdges(graph)

def aerialInterconnection(cont):
    dVertexList = gr.vertices(cont["digraphConnections"])
    minDPQ = mpq.newMinPQ(compareDegree)

    for vertice in lt.iterator(dVertexList):
        inDegree = gr.indegree(cont["digraphConnections"], vertice)
        outDegree = gr.outdegree(cont["digraphConnections"], vertice)
        totalDegree = inDegree + outDegree

        if totalDegree > 0:
            info = [vertice, totalDegree, inDegree, outDegree]
            mpq.insert(minDPQ, info)

    nDVertexList = gr.vertices(cont['graphConnections'])
    minNDPQ = mpq.newMinPQ(compareDegree)
    for vertice in lt.iterator(nDVertexList):
        degree = gr.degree(cont['graphConnections'], vertice)
        info = [vertice, degree]
        if degree != 0:
            mpq.insert(minNDPQ, info)
    return (minDPQ, minNDPQ)

def shortestRoute(cont, originCityInfo, destinationCityInfo):
    origin = closestAirport(cont, originCityInfo)
    destination = closestAirport(cont, destinationCityInfo)
    (originTerDis, originIATA) = origin
    (destinationTerDis, destinationIATA) = destination
    path = minimumCostPath(cont, originIATA, destinationIATA)
    return (origin, destination, path)

def closestAirport(cont, cityInfo):
    kilometers = 10
    isFound = False
    areaAirportList = lt.newList("ARRAY_LIST")

    while isFound == False and kilometers < 10000:
        (maxLat, minLat, maxLon, minLon) = maxCoordinates(cityInfo, kilometers)
        areaAirportList = airportsByGeography(cont, minLon, maxLon, minLat, maxLat)

        if lt.isEmpty(areaAirportList) == False:
            seHaEncontrado = True
        else:
            kilometers += 10

    # Calcula distancia por cada uno, y elige el menor
    if lt.isEmpty(areaAirportList) == False:
        minLength = None
        minIATA = ""
        for airport in lt.iterator(areaAirportList):
            length = airportDistance(airport, cityInfo)
            if minLength == None:
                minLength = length
                minIATA = airport["IATA"]
            elif length < minLength:
                minLength = length
                minIATA = airport["IATA"]
    return (minLength, minIATA)

def airportsByGeography(cont, lonMin, lonMax, latMin, latMax):
    latMap = cont["latitudeIndex"]
    mapsInRangeList = om.values(latMap, latMin, latMax)
    latLonRangeList = lt.newList("ARRAYLIST")

    for lonMap in lt.iterator(mapsInRangeList):
        recordList = om.values(lonMap, lonMin, lonMax)
        for records in lt.iterator(recordList):
            for record in lt.iterator(records):
                lt.addLast(latLonRangeList, record)

    return(latLonRangeList)

def airportDistance(airport, city):
    # Adaptado de https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    # R = Radio aproximado de la tierra en kilómetros
    R = 6373.0
    lat1 = math.radians(float(city["lat"]))
    lon1 = math.radians(float(city["lng"]))
    lat2 = math.radians(float(airport["Latitude"]))
    lon2 = math.radians(float(airport["Longitude"]))
    distanceLon = lon2 - lon1
    distanceLat = lat2 - lat1
    a = math.sin(distanceLat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(distanceLon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def minimumCostPath(analyzer, initialStation,destStation):
    paths= djk.Dijkstra(analyzer['digrafo conecciones'], initialStation)
    path = djk.pathTo(paths, destStation)
    return path

def maxCoordinates(city, kilometers):
    # Adaptado de https://stackoverflow.com/questions/7477003/calculating-new-longitude-latitude-from-old-n-meters
    # R = Radio aproximado de la tierra en kilómetros
    R = 6378.137
    metersRange = kilometers * 1000
    latitude = float(city["lat"])
    longitude = float(city["lng"])
    m = (1 / ((2 * math.pi / 360) * R)) / 1000
    maxLat = latitude + (metersRange * m)
    minLat = latitude  -  (metersRange * m)
    maxLon = longitude + (metersRange * m) / math.cos(latitude * (math.pi / 180))
    minLon = longitude - (metersRange * m) / math.cos(latitude * (math.pi / 180))
    return (maxLat, minLat, maxLon, minLon)

def minimumCostPath(cont, originIATA, destinationIATA):
    paths = djk.Dijkstra(cont['digraphConnections'], originIATA)
    path = djk.pathTo(paths, destinationIATA)
    return path

def homonymCities(cont, city):
    couple = mp.get(cont['cities'], city)

    if couple != None:
        citiesList = me.getValue(couple)

    return citiesList

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

# Funciones de comparación

def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def compareInterconnections(inter1, inter2):
    return inter1['Interconnections'] > inter2['Interconnections']

def compareCoordinates(lat1, lat2):
    if (lat1 == lat2):
        return 0
    elif (lat1 > lat2):
        return 1
    else:
        return -1 

def compareDegree(vertice1, vertice2):
    fDegree = vertice1[1]
    sDegree = vertice2[1]
    return  (fDegree < sDegree)

def compareRoutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1

def compareIATACode(IATA, IATAkey):
    IATAcode = IATAkey['key']
    if (IATA == IATAcode):
        return 0
    elif (IATA > IATAcode):
        return 1
    else:
        return -1
