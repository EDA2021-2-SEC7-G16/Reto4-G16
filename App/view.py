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
from DISClib.ADT import stack as stk
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

cont = None

airportsFile = "airports-utf8-small.csv"
routesFile = "routes-utf8-small.csv"
citiesFile = "worldcities.csv"

def printMenu():
    print("Bienvenido")
    print("1- Inicializar analizador")
    print("2- Cargar datos al analizador")
    print("4- Encontrar clústeres de tráfico aéreo")
    print("6- Utilizar las millas de viajero")
    print("7- Cuantificar el efecto de un aeropuerto cerrado")

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

def optionFour(cont,airport_1,airport_2):


    total_clusters, Same_cluster = controller.total_clusters(cont,airport_1,airport_2)

    print('En total hay ', total_clusters, 'clusters')
    if Same_cluster:
        print('Ambos aeropuertos estan en el mismo cluster')
    else:
        print('Los aeropuertos no estan en el mismo cluster')    

    
def optionsix(cont,origen,millas):


    peso,size_lista, caminos, longest_root_size, longest_root = controller.min_tree(cont,origen,millas)

    print('tipo: ', str(type(longest_root)))

    print('El peso total para el aarbol de expansion minima es de :', peso)

    print('Hay ',size_lista,' aeropuertos posibles')


    print('La rama mas larga es de tamaño ', longest_root_size, 'y se compone de:')
    n = 1

    z = 0

    lista = lt.newList()

    while z < longest_root_size:
        uwu= (stk.pop(longest_root))
        print(uwu)
        lt.addLast(lista,str(uwu))
        z += 1
    
    distancia = controller.diferenciakm(cont,lista)

    print('la diferencia entre las millas del usuario y la distancia que recorre la rama es de :', str((millas*1.6) -distancia))

def optionseven(cont,airport):

    lista = controller.affectedairports(cont,airport)

    size = lt.size(lista)
    
    print('Se afectaron ', str(size), 'aeopuertos')

    n = [1,2,3,size-2,size-1,size]

    print('Los aeropuertos afectados son los siguientes: ')

    if size <= 6:

        n = 1
        for y in lt.iterator(lista):
            print(n)
            print(y)
    else:
        for y in n:
            m = 1
            while m <= 6:

                print(y)
                print(lt.getElement(lista,y))
                m += 1





    pass
    

    
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

    elif int(inputs[0]) == 4:
        print("Cargando información de los archivos al analizador...")
        airport_1 = input('Ingrese el codigo IATA del primer aeropuerto')
        airport_2 = input('Ingrese el codigo IATA del segundo aeropuerto')
        optionFour(cont,airport_1,airport_2) 

    elif int(inputs[0]) == 6:
        origen = input('Ingrese el codigo IATA de su ciudad de origen')
        millas =int(input('Ingrese su numero de millas'))    
        optionsix(cont,origen,millas)

    elif int(inputs[0]) == 7:
          
        airport = input('Digite el codigo IATA del aeropuerto del cual se quiere tomar el ejemplo de no funcionamiento')  
        optionseven(cont,airport)

    else:
        sys.exit(0)
sys.exit(0)
