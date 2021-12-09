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
from DISClib.ADT import minpq as mpq
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
    print("3- Encontrar puntos de interconexión aérea")
    print("5- Encontrar la ruta más corta entre ciudades")

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

def optionThree(cont):
    (dMinPQ, nDMinPQ) = controller.aerialInterconnection(cont)
    print("==================================")
    print("Grafo dirigido")
    print("==================================")
    print("Cantidad de aeropuertos interconectados: " + (str(mpq.size(dMinPQ))))
    print("Los 5 aeropuertos más interconectados en la red son:")
    printDirected(cont, dMinPQ)
    print("==================================")
    print("Grafo no-dirigido")
    print("==================================")
    print("Cantidad de aeropuertos interconectados: " + (str(mpq.size(nDMinPQ))))
    print("Los 5 aeropuertos más interconectados en la red son:")
    printNotDirected(cont, nDMinPQ)

def printNotDirected(cont, minpq):
    count = 0
    table = PrettyTable()
    table.field_names = ["IATA", "Nombre", "Ciudad", "País", "Conexiones"]
    while count < 5:
        count += 1
        info = mpq.delMin(minpq)
        iata = info[0]
        degree = info[1]
        infoiata = mp.get(cont['airports'], iata)
        infoiata = me.getValue(infoiata)
        table.add_row([iata, str(infoiata["Name"]), str(infoiata["City"]), str(infoiata["Country"]), str(degree)])
    table.max_width = 25
    print(table)

def printDirected(cont, minpq):
    count = 0
    table = PrettyTable()
    table.field_names = ["IATA", "Nombre", "Ciudad", "País", "Total de conexiones", "Salida", "Entrada"]
    while count < 5:
        count += 1
        info = mpq.delMin(minpq)
        iata = info[0]
        degree = info[1]
        outbound = info[3]
        inbound = info[2]
        infoiata = mp.get(cont['airports'], iata)
        infoiata = me.getValue(infoiata)
        table.add_row([iata, str(infoiata["Name"]), str(infoiata["City"]), str(infoiata["Country"]), degree, outbound, inbound])
    table.max_width = 15
    print(table)

def optionFive(cont, originCity, destinationCity):
    originList = controller.homonymCities(cont, originCity)
    destinationList = controller.homonymCities(cont, destinationCity)
    (infoOriginCity, infoDestinationCity) = viewHomonymCities(originList, destinationList)
    (origin, destination, path) = controller.shortestRoute(cont, infoOriginCity, infoDestinationCity)
    (originTerDis, originIATA) = origin
    (destinationTerDis, destinationIATA) = destination
    originT = PrettyTable()
    originT.field_names = ["IATA", "Nombre", "Ciudad", "País"]
    originAe = mp.get(cont["airports"], originIATA)["value"]
    originT.add_row([originAe["IATA"], originAe["Name"], originAe["City"], originAe["Country"]])
    destinationT = PrettyTable()
    destinationT.field_names = ["IATA", "Nombre", "Ciudad", "País"]
    destinationAe = mp.get(cont["airports"], destinationIATA)
    destinationAe = me.getValue(destinationAe)
    destinationT.add_row([destinationAe["IATA"], destinationAe["Name"], destinationAe["City"], destinationAe["Country"]])
    table = PrettyTable()
    table.field_names = ["Origen", "Destino", "Distancia (km)", "Tipo de trayectoria"]
    table.add_row([originCity, originIATA, round(originTerDis, 3), "Terrestre"])  
    totalWeight = originTerDis + destinationTerDis

    print("El aeropuerto de salida cercano a " + originCity + " es: ")
    originT.max_width = 25

    print(originT)
    print("El aeropuerto de llegada cercano a " + destinationCity + " es: ")
    destinationT.max_width = 25

    print(destinationT)
    print("Ruta recomendada: ")

    if path == None:
        print("No se encontró una ruta entre los dos aeropuertos de las ciudades dadas, seguramente no se encuentran en el mismo cluster aéreo.")
    else:
        for route in lt.iterator(path):
            start = route["vertexA"]
            end = route["vertexB"]
            flightWeight = route["weight"]
            table.add_row([start, end, flightWeight, "Aérea"])  
            totalWeight = totalWeight + flightWeight
        table.add_row([destinationCity, destinationIATA, round(destinationTerDis, 3), "Terrestre"])  
        table.add_row([" ", "", round(totalWeight, 3), "Total"])  
        table.max_width = 25
        print(table)

def viewHomonymCities(originList, destinationList):
    if originList == None or destinationList == None:
        print("No se logró encontrar alguna ciudad, revise la información dada.")
        sys.exit(0)
    else:
        if lt.size(originList) == 1:
            infoOriginCity = lt.getElement(originList, 1)
        elif lt.size(originList) > 1:
            print("\nLa ciudad de origen " + originList + " es homónima con estas ciudades:")
            printCitiesList(originList)
            optionO = int(input("Seleccione el número de la ciudad que desea escoger como origen:"))
            if optionO <= lt.size(originList):
                infoOriginCity = lt.getElement(originList, optionO)
            else:
                print("La opción marca no es válida.")
                sys.exit(0)

        if lt.size(destinationList) == 1:
            infoDestinationCity = lt.getElement(destinationList, 1)

        if lt.size(destinationList) > 1:
            print("\nLa ciudad de destino " + destinationCity + " es homónima con estas ciudades:")
            printCitiesList(destinationList)
            optionD = int(input("Seleccione el número de la ciudad que desea escoger como destino:"))
            if optionD <= lt.size(destinationList):
                infoDestinationCity = lt.getElement(destinationList, optionD)
            else:
                print("La opción marca no es válida.")
                sys.exit(0)
                
    return(infoOriginCity, infoDestinationCity)

def printCitiesList(citiesList):
    x = PrettyTable() 
    x.field_names = ["#", "Ciudad", "País", "Latitud", "Longitud", "Población", "ID"]
    cont = 1
    for i in lt.iterator(citiesList):
        x.add_row([str(cont), str(i["city_ascii"]), str(i["country"]), str(i["lat"]), str(i["lng"]), str(i["population"]), str(i["id"])])
        x.max_width = 25
        cont += 1
    print(x)

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

    elif int(inputs[0]) == 3:
        optionThree(cont)

    elif int(inputs[0]) == 5:
        originCity = input('Escriba el nombre de la ciudad origen: ')
        destinationCity = input('Escriba el nombre de la ciudad destino: ')
        optionFive(cont, originCity, destinationCity)

    else:
        sys.exit(0)
sys.exit(0)
