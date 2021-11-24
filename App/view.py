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
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

airportsFile = "airports_full.csv"
routesFile = "routes_full.csv"
citiesFile = "worldcities.csv"

def printMenu():
    print("Bienvenido")
    print("1- Inicializar analizador")
    print("2- Cargar datos al analizador")

def optionTwo(cont):
    # controller.loadAirports(cont, airportsFile)
    controller.loadRoutes(cont, routesFile)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Numero de vértices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El límite de recursión actual es de ' + str(sys.getrecursionlimit()))

cont = None

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
