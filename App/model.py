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


from DISClib.Algorithms.Graphs.dfs import DepthFirstSearch, pathTo
from DISClib.Algorithms.Graphs.prim import PrimMST, weightMST
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.DataStructures import mapentry as me
assert cf
from DISClib.ADT import stack as stk
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
                'digraphConnections': None,
                'graphConnections': None, 
                'cities': None}

    analyzer['airports'] = mp.newMap(numelements=15000,
                                     maptype='PROBING',
                                     comparefunction=compareIATACode)

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

def total_clusters(cont,air_1,air_2):

    all_scc = scc.KosarajuSCC(cont['digraphConnections'])
    Conectados = scc.stronglyConnected(all_scc,air_1,air_2)
    
    return scc.connectedComponents(all_scc), Conectados

def min_tree(cont,origen,millas):


    structure =  PrimMST(cont['graphConnections'])

    peso, lista = weightMST(cont['graphConnections'],structure)

    size_lista = lt.size(lista)

    dfs = DepthFirstSearch(cont['graphConnections'],origen)

    caminos = lt.newList()

    longest_root = ''
    longest_root_size = 0

    for x in lt.iterator(lista):
        if x != origen:
            path = pathTo(dfs,x)

            if path != None:
                lt.addLast(caminos,path)
                if stk.size(path) > longest_root_size:
                    longest_root = path
                    longest_root_size = stk.size(path)

                
            


    return peso,size_lista, caminos, longest_root_size, longest_root

def diferenciakm(cont,lista):

    grafo = cont['graphConnections']    

    tamano = lt.size(lista)
    final = 0

    x = 0
    while x < tamano:
        
        final = final + gr.getEdge(grafo,lt.getElement(lista,x),lt.getElement(lista,x+1))['weight']
        x += 1
         
    return final


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
