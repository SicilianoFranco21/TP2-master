import requests
import csv
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from geopy.geocoders import Nominatim
from geopy import distance
from msvcrt import getch
import os
import webbrowser
import cv2
from speech_recognition import Recognizer, AudioFile # modulo que permite la deteccion de voz
# (Token de renovacion) = 4ba713396c65a352502abcbc1902c6d64c7e30ae
#CONSTANTES
API_TOKEN: str = 'Token 06314a64093e9225ccf62c5872988131c9c5909c'

# CLEAR SCREEN
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#Obtencion de patentes mediante el uso de una API
def obtener_patente(ruta_foto: str) -> str:
    regions: list = ['ar', 'us-ca'] 
    with open(ruta_foto, 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            data=dict(regions=regions),  # Optional
            files=dict(upload=fp),
            headers={'Authorization': API_TOKEN})
        patente : str = response.json()['results'][0]['plate']
        return patente

#Obtencion de patentes mediante el uso de una API
def obtener_descripcion_audio(ruta_audio:str) -> str:
    with AudioFile(ruta_audio) as fuente:
        audio = Recognizer().record(fuente)
    texto_audio = Recognizer().recognize_google(audio,language='es-AR')
    return texto_audio

#Obtencion de direcciones
def obtener_direccion(coordenadas: str) -> tuple:
    direccion = ""
    localidad = ""
    provincia = ""
    try:
        geolocator = Nominatim(user_agent="manejo_csv")
        location = geolocator.reverse(coordenadas, language="es", exactly_one=True)
        direccion = location.raw['address']['road'] + " " + location.raw['address']['house_number']
        localidad = location.raw['address']['state']
        provincia = location.raw['address']['city']
    except:
        pass
    return direccion, localidad, provincia

def obtener_descripcion_audio(ruta_audio: str) -> str:
    return "descripcion_audio"

# Punto 1 del tp (COMPLETO)
def leer_archivo() -> list[dict]:
    cls()
    print("\nPor favor, espere mientras se abre el archivo de infracciones...")
    infracciones: list = []
    with open('Infracciones.csv', 'r') as archivo_csv:
        lector = csv.reader(archivo_csv, delimiter=',')
        for linea in lector:

            timestamp: str = linea[0]
            telefono: str = linea[1]
            latitud: int = linea[2]
            longitud: int = linea[3]
            ruta_foto: str = linea[4]
            descripcion: str = linea[5]
            ruta_audio: str = linea[6]
            coordenadas: str = latitud + "," + longitud
            direccion, localidad, provincia = obtener_direccion(coordenadas)
            patente: str = obtener_patente(ruta_foto)
            descripcion_audio: str = obtener_descripcion_audio(ruta_audio)
            
            informe = {
                "timestamp": timestamp, 
                "telefono": telefono, 
                "latitud": latitud, 
                "longitud": longitud,
                "ruta_foto": ruta_foto,
                "descripcion_texto": descripcion,
                "ruta_audio": ruta_audio,
                "direccion": direccion,
                "localidad": localidad,
                "provincia": provincia,
                "patente": patente,
                "descripcion_audio": descripcion_audio
                    }
            infracciones.append(informe)
    return infracciones


# Punto 2 del tp (COMPLETO) - Corresponde a opcion 1 del programa
def crear_archivo(infracciones: list[dict]):
    # crear un archivo csv llamado "informe_infracciones.csv" con la siguiente informacion:
    # timestamp, telefono, direccion, localidad, provincia, patente, descripcion_texto, descripcion_audio
    with open("informe_infracciones.csv", "w", newline="") as archivo_csv:
        writer = csv.writer(archivo_csv, delimiter=',')
        writer.writerow(["timestamp", "telefono", "direccion", "localidad", "provincia", "patente", "descripcion_texto", "descripcion_audio"])
        for infraccion in infracciones:
            writer.writerow([infraccion['timestamp'], infraccion['telefono'], infraccion['direccion'], infraccion['localidad'], infraccion['provincia'], infraccion['patente'], infraccion['descripcion_texto'], infraccion['descripcion_audio']])
    print("\nEl archivo informe_infracciones.csv se ha creado exitosamente!\n Presione cualquier tecla para continuar...")
    getch()

# Punto 2 del tp (COMPLETO) - Corresponde a opcion 2 del programa

# 3.1 (COMPLETO)
# MOSTRAR ESTADIOS DISPONIBLES        
def mostrar_estadios() -> str:
    print('-----Estadios Disponibles-----')
    estadios: dict = {'RIVER': '-34.5479338, -58.4561614', 'BOCA': '-34.6353183, -58.3650225'}
    for estadio in estadios:
        print(f"* {estadio}")
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

# 3.2 (COMPLETO)
def fecha_a_partir_de_timestamp(timestamp: str) -> str:
    fecha = timestamp.split(' ')[0]
    mes = fecha.split('-')[1]
    dia = fecha.split('-')[2]
    
    if mes == '01':
        mes = 'Enero'
    elif mes == '02':
        mes = 'Febrero'
    elif mes == '03':
        mes = 'Marzo'
    elif mes == '04':
        mes = 'Abril'
    elif mes == '05':
        mes = 'Mayo'
    elif mes == '06':
        mes = 'Junio'
    elif mes == '07':
        mes = 'Julio'
    elif mes == '08':
        mes = 'Agosto'
    elif mes == '09':
        mes = 'Septiembre'
    elif mes == '10':
        mes = 'Octubre'
    elif mes == '11':
        mes = 'Noviembre'
    elif mes == '12':
        mes = 'Diciembre'
        
    anio = fecha.split('-')[0]
    fecha = f'{dia} de {mes} de {anio}'
    return fecha

# 3.3 (COMPLETO)
# INFRACCIONES POR ESTADIO 
def infracciones_estadio(infracciones: list[dict], coordenadas_estadio: str) -> None:
    lista_infracciones_estadio: list = []
    for index in range(len(infracciones)):
        latitud: int = infracciones[index]['latitud']
        longitud: int = infracciones[index]['longitud']
        coordenadas: str = latitud + "," + longitud 
        distancia: float = round(distance.distance(coordenadas_estadio, coordenadas).km, 3)
        if distancia <= 1:
            lista_infracciones_estadio.append(infracciones[index])                        
    print(f"Infracciones cercanas a este estadio: {len(lista_infracciones_estadio)}")
    for index in range(len(lista_infracciones_estadio)):
        print(f'''[{index +1}] {lista_infracciones_estadio[index]['patente']}
        En {lista_infracciones_estadio[index]['direccion'], lista_infracciones_estadio[index]['localidad'], lista_infracciones_estadio[index]['provincia']}
        El dia {fecha_a_partir_de_timestamp(lista_infracciones_estadio[index]['timestamp'])}''')
    print("presione cualquier tecla para continuar")
    getch()

# Punto 4 del tp (COMPLETO) - Corresponde a opcion 4 del programa
# INFRACCIONES MICROCENTRO
def infracciones_microcentro(infracciones: dict) -> None:
    rivadavia_y_callao: tuple = (-34.6090112, -58.3919037)
    cordoba_y_callao: tuple = (-34.5994954, -58.3929758)
    rivadavia_y_alem: tuple = (-34.6070402, -58.3703629)
    cordoba_y_alem: tuple = (-34.5982236, -58.3709155)
# ---------------------------------------------------------------------------------
    lista_infracciones_microcentro: list = []
    for index in infracciones:
        latitud: int = index['latitud']
        longitud: int = index['longitud']
        if ((float(latitud) >= rivadavia_y_callao[0] or float(latitud) >= rivadavia_y_alem[0]) and (float(latitud) <= cordoba_y_callao[0] or float(latitud) <= cordoba_y_alem[0])) and ((float(longitud) >= cordoba_y_callao[1] or float(longitud) >= rivadavia_y_callao[1]) and (float(longitud) <= rivadavia_y_alem[1] or cordoba_y_alem[1])):
            lista_infracciones_microcentro.append(index)
    if len(lista_infracciones_microcentro) == 0:
        print('No hay infracciones en el microcentro')
    else:
        print(f"Infracciones en el microcentro: {len(lista_infracciones_microcentro)}")
        for index in range(len(lista_infracciones_microcentro)):
            print(f'''
[{index +1}] {lista_infracciones_microcentro[index]['patente']}
En {lista_infracciones_microcentro[index]['direccion'], lista_infracciones_microcentro[index]['localidad'], lista_infracciones_microcentro[index]['provincia']}
El dia {fecha_a_partir_de_timestamp(lista_infracciones_microcentro[index]['timestamp'])}
''')
    print("presione cualquier tecla para continuar")
    getch()

# funcion para leer las patentes del archivo de texto(COMPLETO)
def leer_archivo_txt() -> list:
    patentes_robadas: list = []  
    with open('robados.txt', 'r') as archivo_txt:
        for linea in archivo_txt:
            patentes_robadas.append(linea.strip())
    return patentes_robadas

# Punto 5 del programa- Funcion que se encarga de mostrar los autos robados(COMPLETO)
def robados(infracciones: list[dict]) -> None:       
    patentes_robadas: list = leer_archivo_txt()
    lista_de_infracciones: list = []
    
    for index in range(len(infracciones)):
        fecha = fecha_a_partir_de_timestamp(infracciones[index]["timestamp"])
        telefono: str = infracciones[index]['telefono']
        latitud: int = infracciones[index]['latitud']
        longitud: int = infracciones[index]['longitud']
        ruta_foto: str = infracciones[index]['ruta_foto']
        descripcion_texto: str = infracciones[index]['descripcion_texto']
        patente: str = obtener_patente(ruta_foto)
        coordenadas: str = latitud + "," + longitud 
        ubicacion = obtener_direccion(coordenadas)
        informe: dict = {"fecha": fecha, 
                        "telefono": telefono, 
                        "latitud": latitud, 
                        "longitud": longitud,
                        "ruta_foto": ruta_foto,
                        "descripcion_texto": descripcion_texto,
                        "patente": patente,
                        "coordenadas": coordenadas,
                        "ubicacion": ubicacion}
        lista_de_infracciones.append(informe)

    lista_de_infracciones_robadas: list = []
    for infraccion in lista_de_infracciones:
        if infraccion['patente'] in patentes_robadas:
            lista_de_infracciones_robadas.append(infraccion)
            
    # imprimo la patente, la fecha y la ubicacion de las infracciones robadas
    for infraccion in lista_de_infracciones_robadas:
        print(f"Patente: {infraccion['patente']}, Fecha: {infraccion['fecha']}, Ubicacion: {infraccion['ubicacion']}\n")

# Punto 6 del programa- Funcion que se encarga de mostrar las infracciones de un autoen base a la patente(COMPLETO)
def buscar_patente(infracciones: list):
    cls()
    print("PATENTES REGISTRADAS:")
    f: int = 0
    for infraccion in infracciones:
        f += 1
        print((f, " - ", infraccion['patente']))
    patente_correcta: bool = False
    while not patente_correcta:
        patente: str = input("\nIngrese la patente que desea buscar, en caso de ser erronea le consultaremos nuevamente(para finalizar coloque fin): ").lower()
        if patente == "fin":
            return
        for infraccion in infracciones:
            if infraccion['patente'] == patente:
                patente_correcta = True
        # abrir la foto de la patente
        if patente_correcta == True:
            for infraccion in infracciones:
                if infraccion['patente'] == patente:
                    # plotear la foto de la patente
                    ruta_foto: str = infraccion['ruta_foto']
                    img = mpimg.imread(ruta_foto)
                    imgplot = plt.imshow(img)
                    plt.show()
                    # mostrar en un mapa la ubicacion de la infraccion
                    webbrowser.open("https://www.google.com/maps/search/?api=1&query=" + infraccion['latitud'] + "," + infraccion['longitud'])         
            print("PATENTES REGISTRADAS:")
            f: int = 0
            for infraccion in infracciones:
                f += 1
                print((f, " - ", infraccion['patente']))
            patente_correcta: bool = False
        cls()


# Punto 6 del tp (COMPLETO) - Corresponde a opcion 7 del programa
def grafico(infracciones:dict):
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


# FUNCION QUE IMPRIME EL MENU PRINCIPAL
def imprimmir_menu() -> None:
    print('''
========================
**** MENU PRINCIPAL ****
========================
[1] - Crear un nuevo archivo de infracciones
[2] - Listar las infracciones cercanas (1km) a los estadios
[3] - Listar las infracciones de microcentro
[4] - Emitir una alerta de vehiculos robados
[5] - Informacion a partir de dominio, mostrar foto y mapa de google con la ubicacion marcada con un punto
[6] - Grafico a partir de las denuncias recibidas por mes
[7] - Salir del programa''')


# MENU PRINCIPAL

def menu_principal(infracciones: list) -> None:
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
                    crear_archivo(infracciones)
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
            
    

# INICIALIZADOR DEL PROGRAMA
def main() -> None:
    infracciones: list[dict] = leer_archivo()
    cls()
    print('''

        dP""b8 888888 .dP"Y8 888888  dP"Yb  88""Yb     8888b.  888888               
       dP   `" 88__   `Ybo."   88   dP   Yb 88__dP      8I  Yb 88__                 
       Yb  "88 88""   o.`Y8b   88   Yb   dP 88"Yb       8I  dY 88""                 
        YboodP 888888 8bodP'   88    YbodP  88  Yb     8888Y"  888888               
                                                                                                                                                                                                              
88 88b 88 888888 88""Yb    db     dP""b8  dP""b8 88  dP"Yb  88b 88 888888 .dP"Y8 
88 88Yb88 88__   88__dP   dPYb   dP   `" dP   `" 88 dP   Yb 88Yb88 88__   `Ybo." 
88 88 Y88 88""   88"Yb   dP__Yb  Yb      Yb      88 Yb   dP 88 Y88 88""   o.`Y8b 
88 88  Y8 88     88  Yb dP""""Yb  YboodP  YboodP 88  YbodP  88  Y8 888888 8bodP' ''')
    imprimmir_menu()
    menu_principal(infracciones)


main()
