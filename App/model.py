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
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    analyzer = {'airports': None,
                'digraphConnections': None}

    analyzer['airports'] = mp.newMap(numelements=15000,
                                     maptype='PROBING',
                                     comparefunction=compareIATACode)

    analyzer['digraphConnections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=100000,
                                              comparefunction=compareIATACode)
    return analyzer


# Funciones para agregar informacion al catalogo

def addStopConnection(analyzer, lastFlight, route):
    """
    Adiciona los aeropuertos al grafo como vértices y arcos entre las
    estaciones adyacentes.
    """
    
    origin = formatVertex(lastFlight)
    destination = formatVertex(route)
    cleanServiceDistance(lastFlight, route)
    distance = float(route['distance_km']) - float(lastFlight['distance_km'])
    distance = abs(distance)
    addStop(analyzer, origin)
    addStop(analyzer, destination)
    addConnection(analyzer, origin, destination, distance)
    addRouteStop(analyzer, route)
    addRouteStop(analyzer, lastFlight)
    return analyzer
    

def addStop(analyzer, airportID):
    """
    Adiciona un aeropuerto como un vértice del grafo.
    """
    if not gr.containsVertex(analyzer['airports'], airportID):
        gr.insertVertex(analyzer['airports'], airportID)
    return analyzer


def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos aeropuertos.
    """
    edge = gr.getEdge(analyzer['airports'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['airports'], origin, destination, distance)
    return analyzer

def addRouteStop(analyzer, route):
    """
    Agrega a un aeropuerto una ruta que 
    es servida en esa estación.
    """
    entry = mp.get(analyzer['digraphConnections'], route['Destination'])
    if entry is None:
        routesList = lt.newList(cmpfunction=compareRoutes)
        lt.addLast(routesList, route['Airline'])
        mp.put(analyzer['digraphConnections'], route['Destination'], routesList)
    else:
        routesList = entry['value']
        info = route['Airline']
        if not lt.isPresent(routesList, info):
            lt.addLast(routesList, info)
    return analyzer

def addRouteConnections(analyzer):
    """
    Por cada vértice (cada estacion) se recorre la lista
    de rutas servidas en dicho aeropuerto y se crean
    arcos entre ellos para representar el cambio de ruta
    que se puede realizar en una estación.
    """
    stopsList = mp.keySet(analyzer['airports'])
    for key in lt.iterator(stopsList):
        routesList = mp.get(analyzer['airports'], key)['value']
        prevRoute = None
        for route in lt.iterator(routesList):
            route = key + '-' + route
            if prevRoute is not None:
                addConnection(analyzer, prevRoute, route, 0)
                addConnection(analyzer, route, prevRoute, 0)
            prevRoute = route

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
