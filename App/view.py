"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT.graph import gr
from DISClib.DataStructures import mapentry as me
from prettytable import PrettyTable
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

cont = None

airportsFile = "airports_full.csv"
routesFile = "routes_full.csv"
citiesFile = "worldcities.csv"

def printMenu():
    print("Bienvenido")
    print("1- Inicializar analizador")
    print("2- Cargar datos al analizador")

def optionTwo(cont):
    # controller.loadAirports(cont, airportsFile)
    controller.loadFiles(cont, airportsFile, routesFile, citiesFile)
    airportsND = controller.vertexAmmount(cont['graphConnections'])
    airportsD = controller.vertexAmmount(cont['digraphConnections'])
    routesND = controller.edgesAmmount(cont['graphConnections'])
    routesD = controller.edgesAmmount(cont['digraphConnections'])

    cities = mp.get(cont['cities'], "Counter")
    cities = me.getValue(cities)

    dAirportIATA = lt.getElement(gr.vertices(cont['digraphConnections']), 1)
    nDAirportIATA = lt.getElement(gr.vertices(cont['graphConnections']), 1)
    dAirportInfo = mp.get(cont['airports'], dAirportIATA)
    dAirportInfo = me.getValue(dAirportInfo)
    nDAirportInfo = mp.get(cont['airports'], nDAirportIATA)
    nDAirportInfo = me.getValue(nDAirportInfo)
    lastCity = lt.getElement((lt.getElement(mp.valueSet(cont['cities']), mp.size(cont['cities'])-1)), 1)

    total = PrettyTable()
    total.field_names = ["Grafo dirigido", "", "Grafo no-dirigido", " ", "Ciudades", "   "]
    total.add_row(["Total de aeropuertos", str(airportsD), "Total de aeropuertos", str(airportsND), "Total de ciudades", cities])
    total.add_row(["Total de rutas", str(routesD), "Total de rutas", str(routesND), " ", " "])
    total.max_width = 25
    print(total)

    airports = PrettyTable() 
    airports.field_names = ["Grafo", "Nombre", "Ciudad", "País", "Latitud", "Longitud"]
    airports.add_row(["No-dirigido", str(nDAirportInfo["Name"]), str(nDAirportInfo["City"]), str(nDAirportInfo["Country"]), str(nDAirportInfo["Latitude"]), str(nDAirportInfo["Longitude"])])
    airports.add_row(["Dirigido", str(dAirportInfo["Name"]), str(dAirportInfo["City"]), str(dAirportInfo["Country"]), str(dAirportInfo["Latitude"]), str(dAirportInfo["Longitude"])])
    airports.max_width = 10

    print("Primeros aeropuertos cargados:")
    print(airports)

    city = PrettyTable()
    city.field_names = ["Nombre de ciudad", "País", "Latitud", "Longitud", "Población", "ID"]
    city.add_row([str(lastCity["city_ascii"]), str(lastCity["country"]), str(lastCity["lat"]), str(lastCity["lng"]), str(lastCity["population"]), str(lastCity["id"])])
    city.max_width = 25
    print("Última ciudad cargada")
    print(city)

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')
    if int(inputs[0]) == 1:
        print("Inicializando...")
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos al analizador...")
        optionTwo(cont)

    else:
        sys.exit(0)
sys.exit(0)
