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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos

def loadRoutes(analyzer, routesFile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Crea un vértice por cada aeropuerto dentro del archivo.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    routesFile = cf.data_dir + routesFile
    inputFile = csv.DictReader(open(routesFile, encoding="utf-8"),
                                delimiter=",")
    lastFlight = None

    for route in inputFile:
        if lastFlight is not None:
            sameDeparture = lastFlight['Departure'] == route['Departure']
            sameDestination = lastFlight['Destination'] == route['Destination']
            if sameDeparture and not sameDestination:
                model.addStopConnection(analyzer, lastFlight, route)
        lastFlight = route
    model.addRouteConnections(analyzer)
    return analyzer

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
