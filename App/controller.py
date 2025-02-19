﻿"""
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

def loadFiles(analyzer, airportsFile, routesFile, citiesFile):
    """
    Carga los datos de los archivos CSV en el modelo.
    """
    airportsFile = cf.data_dir + airportsFile
    routesFile = cf.data_dir + routesFile
    citiesFile = cf.data_dir + citiesFile
    cityCount = 0

    airportsInputFile = csv.DictReader(open(airportsFile, encoding="utf-8"),
                                delimiter=",")
    routesInputFile = csv.DictReader(open(routesFile, encoding="utf-8"),
                                delimiter=",")
    citiesInputFile = csv.DictReader(open(citiesFile, encoding="utf-8"),
                                delimiter=",")

    for airport in airportsInputFile:
        model.addAirport(analyzer, airport)
    for route in routesInputFile:
        model.addRoute(analyzer, route)
    for city in citiesInputFile:
        cityCount += 1
        model.addCity(analyzer, city, cityCount)

    return analyzer

# Funciones de ordenamiento



# Funciones de consulta sobre el catálogo
def vertexAmmount(graph):
    return model.vertexAmmount(graph)

def edgesAmmount(graph):
    return model.edgesAmmount(graph)

def aerialInterconnection(cont):
    return model.aerialInterconnection(cont)

def homonymCities(cont, city):
    return model.homonymCities(cont, city)

def shortestRoute(cont, originCityInfo, destinationCityInfo):
    return model.shortestRoute(cont, originCityInfo, destinationCityInfo)

def total_clusters(cont, air_1, air_2):
    return model.total_clusters(cont,air_1,air_2)

def min_tree(cont,origen,millas):
    return model.min_tree(cont,origen,millas)

def diferenciakm(cont,lista):

    return model.diferenciakm(cont,lista)    

def affectedairports(cont,airport):

    return model.affectedairports(cont,airport)    
       
