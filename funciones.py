from manejo_de_archivos import *
from utils import *
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from geopy import distance
from msvcrt import getch
import webbrowser
import os


def cls() -> None:
    # funcion que permite limpiar la consola
    os.system('cls' if os.name=='nt' else 'clear')


def mostrar_estadios() -> str:

    # funcion que permite mostrar los estadios disponibles y permitir al usuario elegir uno
    # precondicion: no recibe parametros
    # postcondicion: devuelve un string con las coordenadas del estadio elegido

    cls()
    print('''
┌────────────────────────────────────────────────────────────────────────────────┐
│                             ESTADIOS DISPONIBLES                               │
└────────────────────────────────────────────────────────────────────────────────┘''')
    estadios: dict = {'RIVER': '-34.5479338, -58.4561614', 'BOCA': '-34.6353183, -58.3650225'}
    for estadio in estadios:
        print(f'''┌────────────────────────────────────────────────────────────────────────────────┐
│                                   {estadio}                                        │
└────────────────────────────────────────────────────────────────────────────────┘''')
    cancha: bool = False
    while not cancha:
        try:
            estadio: str = input('\nIngrese el estadio: ').upper()
            if estadio in estadios:
                cancha = True
            else:
                raise ValueError
        except ValueError:
            print('Estadio no valido')
    coordenadas_del_estadio: str = estadios[estadio]
    return coordenadas_del_estadio


def infracciones_estadio(infracciones: list[dict], coordenadas_estadio: str) -> None:

    # funcion que permite mostrar las infracciones que se realizaron cerca de un estadio
    # precondicion: recibe una lista de diccionarios con las infracciones y un string con las coordenadas del estadio
    # postcondicion: imprime por pantalla la cantidad de infracciones que se realizaron cerca del estadio y los datos de cada infraccion, pero no devuelve nada

    lista_infracciones_estadio: list = []
    for index in range(len(infracciones)):
        latitud: int = infracciones[index]['latitud']
        longitud: int = infracciones[index]['longitud']
        coordenadas: str = latitud + "," + longitud 
        distancia: float = round(distance.distance(coordenadas_estadio, coordenadas).km, 3)
        if distancia <= 1:
            lista_infracciones_estadio.append(infracciones[index])                        
    print(f'''
┌────────────────────────────────────────────────────────────────────────────────┐
│  Infracciones cercanas a este estadio: {len(lista_infracciones_estadio)}                                       │
└────────────────────────────────────────────────────────────────────────────────┘''')
    for index in range(len(lista_infracciones_estadio)):
        print(f'''
┌────────────────────────────────────────────────────────────────────────────────┐
│  [{index +1}] {lista_infracciones_estadio[index]['patente']}                                                                   │
├────────────────────────────────────────────────────────────────────────────────┤
│  En {lista_infracciones_estadio[index]['direccion']},
│     {lista_infracciones_estadio[index]['localidad']},
│     {lista_infracciones_estadio[index]['provincia']}
│                                                                                
│  El dia {fecha_a_partir_de_timestamp(lista_infracciones_estadio[index]['timestamp'])}
│                                                                                
└────────────────────────────────────────────────────────────────────────────────┘
''')
        
    print("presione cualquier tecla para continuar")
    getch()


def infracciones_microcentro(infracciones: dict) -> None:

    # funcion que permite mostrar las infracciones que se realizaron en el microcentro
    # precondicion: recibe una lista de diccionarios con las infracciones
    # postcondicion: imprime por pantalla la cantidad de infracciones que se realizaron en el microcentro y los datos de cada infraccion, pero no devuelve nada

    cls()
    rivadavia_y_callao: tuple = (-34.6090112, -58.3919037)
    cordoba_y_callao: tuple = (-34.5994954, -58.3929758)
    rivadavia_y_alem: tuple = (-34.6070402, -58.3703629)
    cordoba_y_alem: tuple = (-34.5982236, -58.3709155)
    lista_infracciones_microcentro: list = []
    for index in infracciones:
        latitud: int = index['latitud']
        longitud: int = index['longitud']
        if ((float(latitud) >= rivadavia_y_callao[0] or float(latitud) >= rivadavia_y_alem[0]) and (float(latitud) <= cordoba_y_callao[0] or float(latitud) <= cordoba_y_alem[0])) and ((float(longitud) >= cordoba_y_callao[1] or float(longitud) >= rivadavia_y_callao[1]) and (float(longitud) <= rivadavia_y_alem[1] or cordoba_y_alem[1])):
            lista_infracciones_microcentro.append(index)
    if len(lista_infracciones_microcentro) == 0:
        print('No hay infracciones en el microcentro')
    else:
        print(f'''┌────────────────────────────────────────────────────────────────────────────────┐
│  Infracciones cercanas microcentro: {len(lista_infracciones_microcentro)}                                          │
└────────────────────────────────────────────────────────────────────────────────┘''')
        for index in range(len(lista_infracciones_microcentro)):
            print(f'''
┌────────────────────────────────────────────────────────────────────────────────┐
│  [{index +1}] {lista_infracciones_microcentro[index]['patente']}                                                                   │
├────────────────────────────────────────────────────────────────────────────────┤
│  En {lista_infracciones_microcentro[index]['direccion']},
│     {lista_infracciones_microcentro[index]['localidad']},
│     {lista_infracciones_microcentro[index]['provincia']}
│                                                                                
│  El dia {fecha_a_partir_de_timestamp(lista_infracciones_microcentro[index]['timestamp'])}
│                                                                                
└────────────────────────────────────────────────────────────────────────────────┘
''')
    print("presione cualquier tecla para continuar")
    getch()


def robados(infracciones: list[dict]) -> None:
    
    # funcion que permite mostrar las infracciones que se realizaron a autos robados
    # precondicion: recibe una lista de diccionarios con las infracciones
    # postcondicion: imprime por pantalla la cantidad de infracciones que se realizaron a autos robados y los datos de cada infraccion, pero no devuelve nada

    cls()   
    patentes_robadas: list = leer_archivo_txt()
    print('''
┌────────────────────────────────────────────────────────────────────────────────┐
│                        AUTOS REPORTADOS COMO ROBADOS:                          │
└────────────────────────────────────────────────────────────────────────────────┘''')
    for index in range(len(infracciones)):
        patente: str = infracciones[index]['patente']
        if patente in patentes_robadas:
            print(f'''
┌────────────────────────────────────────────────────────────────────────────────┐
│  PATENTE: {infracciones[index]['patente']}                                                              │
├────────────────────────────────────────────────────────────────────────────────┤
│  En {infracciones[index]['direccion']},
│     {infracciones[index]['localidad']},
│     {infracciones[index]['provincia']}
│                                                                                
│  Reportado el dia {fecha_a_partir_de_timestamp(infracciones[index]['timestamp'])}
│                                                                                
└────────────────────────────────────────────────────────────────────────────────┘
''')
    print("presione cualquier tecla para continuar")
    getch()


def buscar_patente(infracciones: list) -> None:

    # funcion que permite buscar una patente en la lista de infracciones
    # precondicion: recibe una lista de diccionarios con las infracciones
    # postcondicion: imprime por pantalla la cantidad de infracciones que se realizaron a esa patente y los datos de cada infraccion, pero no devuelve nada

    cls()
    
    patente_correcta: bool = False
    while not patente_correcta:
        try:
            print('''
┌────────────────────────────────────────────────────────────────────────────────┐
│                             PATENTES REGISTRADAS                               │
└────────────────────────────────────────────────────────────────────────────────┘''')
            f: int = 0
            for infraccion in infracciones:
                f += 1
                print(f'''┌────────────────────────────────────────────────────────────────────────────────┐
│  [{f}] {infraccion['patente']}                                                                   │
└────────────────────────────────────────────────────────────────────────────────┘''')
            patente: str = input("\nIngrese la patente que desea buscar, en caso de ser erronea le consultaremos nuevamente \nPara volver al menu, presione enter: ").lower()
            if patente != "":
                for infraccion in infracciones:
                    if infraccion['patente'] == patente:
                        patente_correcta = True
            elif patente == "":
                patente_correcta = True
            else:
                raise ValueError
        except ValueError:
            print("Ingrese una patente valida")
            
        if patente_correcta == True and patente != "":
            for infraccion in infracciones:
                if infraccion['patente'] == patente:
                    ruta_foto: str = infraccion['ruta_foto']
                    img = mpimg.imread(ruta_foto)
                    imgplot = plt.imshow(img)
                    plt.show()
                    webbrowser.open("https://www.google.com/maps/search/?api=1&query=" + infraccion['latitud'] + "," + infraccion['longitud'])
            print("presione cualquier tecla para continuar")
            getch()
        elif patente_correcta == True and patente == "":
            print("presione cualquier tecla para continuar")
            getch()
        cls()


def grafico(infracciones:dict) -> None:

    # funcion que permite mostrar un grafico con la cantidad de infracciones por mes
    # precondicion: recibe una lista de diccionarios con las infracciones
    # postcondicion: imprime por pantalla un grafico con la cantidad de infracciones por mes, pero no devuelve nada

    infracciones_enero: int = 0
    infracciones_febrero: int = 0
    infracciones_marzo: int = 0
    infracciones_abril: int = 0
    infracciones_mayo : int = 0
    infracciones_junio : int = 0
    infracciones_julio: int = 0
    infracciones_agosto: int = 0
    infracciones_septiembre: int = 0
    infracciones_octubre: int = 0
    infracciones_noviembre: int = 0
    infracciones_diciembre: int = 0
    for index in range(len(infracciones)):
       if infracciones[index]["timestamp"][5:7] == '01':
           infracciones_enero += 1
       elif infracciones[index]["timestamp"][5:7] == '02':
           infracciones_febrero += 1
       elif infracciones[index]["timestamp"][5:7] == '03':
           infracciones_marzo += 1
       elif infracciones[index]["timestamp"][5:7] == '04':
           infracciones_abril += 1
       elif infracciones[index]["timestamp"][5:7] == '05':
           infracciones_mayo += 1
       elif infracciones[index]["timestamp"][5:7] == '06':
           infracciones_junio += 1
       elif infracciones[index]["timestamp"][5:7] == '07':
           infracciones_julio += 1
       elif infracciones[index]["timestamp"][5:7] == '08':
           infracciones_agosto += 1
       elif infracciones[index]["timestamp"][5:7] == '09':
           infracciones_septiembre += 1
       elif infracciones[index]["timestamp"][5:7] == '10':
           infracciones_octubre += 1
       elif infracciones[index]["timestamp"][5:7] == '11':
           infracciones_noviembre += 1
       elif infracciones[index]["timestamp"][5:7] == '12':
           infracciones_diciembre += 1    
    infracciones_por_mes: list = [infracciones_enero, infracciones_febrero, infracciones_marzo, infracciones_abril, infracciones_mayo, infracciones_junio, infracciones_julio, infracciones_agosto, infracciones_septiembre, infracciones_octubre, infracciones_noviembre, infracciones_diciembre]
    meses: list = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    plt.bar(meses, infracciones_por_mes)
    plt.title('Infracciones por mes')
    plt.xlabel('Meses')
    plt.ylabel('Infracciones')
    plt.show()
    print("presione cualquier tecla para continuar")
    getch()


def imprimmir_menu() -> None:

    # funcion que imprime por pantalla el menu principal

    print('''
    
    ┌─────────────────────────────────────────────────────────────────────────────┐    
    │      __  __                               _            _             _      │
    │     |  \/  | ___ _ __  _   _   _ __  _ __(_)_ __   ___(_)_ __   __ _| |     │
    │     | |\/| |/ _ \ '_ \| | | | | '_ \| '__| | '_ \ / __| | '_ \ / _` | |     │
    │     | |  | |  __/ | | | |_| | | |_) | |  | | | | | (__| | |_) | (_| | |     │
    │     |_|  |_|\___|_| |_|\__,_| | .__/|_|  |_|_| |_|\___|_| .__/ \__,_|_|     │  
    │                               |_|                       |_|                 │
    ├─────┬───────────────────────────────────────────────────────────────────────┤
    │  1  │                Crear un nuevo archivo de infracciones                 │
    ├─────┼───────────────────────────────────────────────────────────────────────┤
    │  2  │        Listar las infracciones cercanas (1km) de los estadios         │
    ├─────┼───────────────────────────────────────────────────────────────────────┤
    │  3  │                Listar las infracciones de microcentro                 │
    ├─────┼───────────────────────────────────────────────────────────────────────┤
    │  4  │            Mostrar en pantalla lista de vehiculos robados             │
    ├─────┼───────────────────────────────────────────────────────────────────────┤
    │  5  │       Mostrar informacion, foto y ubicacion a partir de dominio       │
    ├─────┼───────────────────────────────────────────────────────────────────────┤
    │  6  │   Mostrar grafico de barras en base a los datos de las infracciones   │
    ├─────┼───────────────────────────────────────────────────────────────────────┤
    │  7  │                                 Salir                                 │
    └─────┴───────────────────────────────────────────────────────────────────────┘
''')
def menu_principal(infracciones: list) -> None:

    # funcion que permite mostrar el menu principal y ejecutar las funciones correspondientes a cada opcion
    # precondicion: recibe una lista de diccionarios con las infracciones para poder utilizarlas en las funciones
    # postcondicion: ejecuta las funciones correspondientes a cada opcion, pero no devuelve nada
    
    cerrar_menu: bool = False
    while not cerrar_menu:
        opcion_ok = False
        while not opcion_ok:
            try:
                opcion: int = int(input('Ingrese una opcion: '))
                if 0 < opcion < 8:
                    opcion = str(opcion)
                    opcion_ok = True
                else: 
                    raise ValueError
            except ValueError:
                print('Opcion invalida, ingrese una opcion valida')
            else:
                if opcion == "1":
                    print("Ha seleccionado --> [1]\n")
                    crear_archivo_csv(infracciones)
                    cls()
                    imprimmir_menu()
                elif opcion == "2":
                    print("Ha seleccionado --> [2]\n")
                    estadio: str = mostrar_estadios()
                    infracciones_estadio(infracciones, estadio)
                    cls()
                    imprimmir_menu()
                elif opcion == "3":
                    print("Ha seleccionado --> [3]\n")
                    infracciones_microcentro(infracciones)
                    cls()
                    imprimmir_menu()
                elif opcion == "4":
                    print("Ha seleccionado --> [4]\n")
                    robados(infracciones)
                    cls()
                    imprimmir_menu()
                elif opcion == "5":
                    print("Ha seleccionado --> [5]\n")
                    buscar_patente(infracciones)
                    cls()
                    imprimmir_menu()
                elif opcion == "6":
                    print("Ha seleccionado --> [6]\n")
                    grafico(infracciones)
                    cls()
                    imprimmir_menu()
                elif opcion == "7":
                    print("Ha seleccionado --> [7]\n")
                    print("Gracias por utilizar el programa")
                    cerrar_menu = True
                    exit()
                opcion_ok = False