import requests
import csv
from matplotlib import pyplot as plt
from geopy.geocoders import Nominatim
from geopy import distance


#CONSTANTES
API_TOKEN: str = 'Token 8e0fee00a18a82f4e672f4f1239252435727dbfe'


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



# Punto 1 del tp (COMPLETO)
def leer_archivo() -> list[dict]:
    infracciones: list = []
    with open('multas.csv', 'r') as archivo_csv:
        lector = csv.reader(archivo_csv, delimiter=',')
        for linea in lector:
            
            timestamp: str = linea[0]
            telefono: str = linea[1]
            latitud: int = linea[2]
            longitud: int = linea[3]
            ruta_foto: str = linea[4]
            descripcion: str = linea[5]
            #ruta_audio: str = linea[6]

            informe = {
                "timestamp": timestamp, 
                "telefono": telefono, 
                "latitud": latitud, 
                "longitud": longitud,
                "ruta_foto": ruta_foto,
                "descripcion": descripcion
                    }
            infracciones.append(informe)
    return infracciones



# Punto 2 del tp (COMPLETO) - Corresponde a opcion 1 del programa
def crear_archivo(infracciones: list[dict]) -> list[dict]:
    for infraccion in range(len(infracciones)):
        timestamp: str = infracciones[infraccion]['timestamp']
        telefono: str = infracciones[infraccion]['telefono']
        latitud: int = infracciones[infraccion]['latitud']
        longitud: int = infracciones[infraccion]['longitud']
        ruta_foto: str = infracciones[infraccion]['ruta_foto']
        
        #Agregamos patente al diccionario
        patente: str = obtener_patente(ruta_foto)
        infracciones[infraccion]['patente'] = patente
        descripcion_texto: str = infracciones[infraccion]['descripcion']
        
        #Agregamos coordenadas al diccionario
        coordenadas: str = latitud + "," + longitud 
        infracciones[infraccion]['coordenadas'] = coordenadas
        
        #Agregamos ubicacion al diccionario
        direccion, localidad, provincia = obtener_direccion(coordenadas)
        infracciones[infraccion]['ubicacion'] = direccion, localidad, provincia
        #descripcion_audio: str = obtener_texto_audio(infracciones[infraccion][6])
    return infracciones



# Punto 3 del tp (COMPLETO) - Corresponde a opcion 2 del programa

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
                print('Estadio no valido')
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
    lista_impresa: bool = False
    while not lista_impresa:
        lista_infracciones_estadio: list = []
        
        for index in range(len(infracciones)):
            fecha = fecha_a_partir_de_timestamp(infracciones[index]["timestamp"])
            telefono: str = infracciones[index]['telefono']
            latitud: int = infracciones[index]['latitud']
            longitud: int = infracciones[index]['longitud']
            ruta_foto: str = infracciones[index]['ruta_foto']
            descripcion_texto: str = infracciones[index]['descripcion']
            patente: str = obtener_patente(ruta_foto)
            coordenadas: str = latitud + "," + longitud 
            distancia: float = round(distance.distance(coordenadas_estadio, coordenadas).km, 3)
            ubicacion = obtener_direccion(coordenadas)
            
            informe: dict = {"fecha": fecha, 
                            "telefono": telefono, 
                            "latitud": latitud, 
                            "longitud": longitud,
                            "ruta_foto": ruta_foto,
                            "descripcion": descripcion_texto,
                            "patente": patente,
                            "coordenadas": coordenadas,
                            "distancia": distancia,
                            "ubicacion": ubicacion}
            
            if informe['distancia'] <= 1:    
                lista_infracciones_estadio.append(informe)
                             
        print(f"Infracciones cercanas a este estadio: {len(lista_infracciones_estadio)}")
        for index in range(len(lista_infracciones_estadio)):
            print(f"[{index + 1}] {lista_infracciones_estadio[index]['descripcion']}")
            print(f"En {lista_infracciones_estadio[index]['ubicacion']}")
            print(f"El dia {lista_infracciones_estadio[index]['fecha']}\n")

        lista_impresa = True



# Punto 4 del tp (COMPLETO) - Corresponde a opcion 3 del programa
# INFRACCIONES MICROCENTRO
def infracciones_microcentro(infracciones: dict):
    lista_impresa: bool = False
    while not lista_impresa:
    # CUADRANTE APROXIMADO A PARTIR DE COORDENADAS OPUESTAS (ALEM Y CORDOBA, RIVADAVIA Y CALLAO)
    # CORDOBA_Y_ALEM = '-34.5983795, -58.3725168'
    # ALEM_Y_RIVADAVIA = '-34.6091603, -58.3725168'
    # RIVADAVIA_Y_CALLAO = '-34.6091603, -58.3924939'
    # CALLAO_Y_CORDOBA = '-34.5983795, -58.3924939'

        tope_arriba_cuadrante: str = '-34.5983795'
        tope_abajo_cuadrante: str = '-34.6091603'
        tope_izquierdo_cuadrante: str = '-58.3924939'
        tope_derecho_cuadrante: str = '-58.3725168'
        # --------------------------------------------------------------------------------------------------------
        lista_infracciones_microcentro: list = []
        for index in range(len(infracciones)):
            fecha = fecha_a_partir_de_timestamp(infracciones[index]["timestamp"])
            latitud = infracciones[index]['latitud']
            longitud = infracciones[index]['longitud']
            ruta_foto: str = infracciones[index]['ruta_foto']
            patente: str = obtener_patente(ruta_foto)
            coordenadas: str = latitud + "," + longitud
            ubicacion = obtener_direccion(coordenadas)
            
            informe: dict = {"fecha": fecha,
                            "latitud": latitud, 
                            "longitud": longitud,
                            "ruta_foto": ruta_foto,
                            "patente": patente,
                            "ubicacion": ubicacion
                                }
            #El resto de la funcion funciona bien, el problema esta en la condicion como tal, va a haber que pensar otra cosa para el if.            
            if (tope_arriba_cuadrante <= informe['latitud'] <= tope_abajo_cuadrante) and (tope_derecho_cuadrante <= informe['longitud'] <= tope_izquierdo_cuadrante):
                lista_infracciones_microcentro.append(informe[index])

        print(f"Infracciones cercanas a este estadio: {len(lista_infracciones_microcentro)}")
        for index in range(len(lista_infracciones_microcentro)):
            print(f"[{index + 1}] {lista_infracciones_microcentro[index]['descripcion']}")
            print(f"En {lista_infracciones_microcentro[index]['ubicacion']}")
            print(f"El dia {lista_infracciones_microcentro[index]['fecha']}\n")

        lista_impresa = True



# funcion para leer las patentes del archivo de texto(COMPLETO)
def leer_archivo_txt() -> list:
    patentes_robadas: list = []  
    with open('robados.txt', 'r') as archivo_txt:
        for linea in archivo_txt:
            patentes_robadas.append(linea.strip())
    return patentes_robadas



# Punto 4 del programa- Funcion que se encarga de mostrar los autos robados(COMPLETO)
def robados(infracciones: list[dict]) -> None:       
    patentes_robadas: list = leer_archivo_txt()
    lista_de_infracciones: list = []
    
    for index in range(len(infracciones)):
        fecha = fecha_a_partir_de_timestamp(infracciones[index]["timestamp"])
        telefono: str = infracciones[index]['telefono']
        latitud: int = infracciones[index]['latitud']
        longitud: int = infracciones[index]['longitud']
        ruta_foto: str = infracciones[index]['ruta_foto']
        descripcion_texto: str = infracciones[index]['descripcion']
        patente: str = obtener_patente(ruta_foto)
        coordenadas: str = latitud + "," + longitud 
        ubicacion = obtener_direccion(coordenadas)
        informe: dict = {"fecha": fecha, 
                        "telefono": telefono, 
                        "latitud": latitud, 
                        "longitud": longitud,
                        "ruta_foto": ruta_foto,
                        "descripcion": descripcion_texto,
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



# Punto 6 del tp (COMPLETO) - Corresponde a opcion 6 del programa
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



# MENU PRINCIPAL
def menu_principal(opcion: str) -> None:
    infracciones: list[dict] = leer_archivo()
   
    while opcion != "7":
        if opcion == "1":
            print("Ha seleccionado --> [1]\n")
            multas: list[dict] = crear_archivo(infracciones)
            for multa in multas:
                print(multa)
            opcion: str = input("\n\nElija una opcion del menu para realizar otra accion: ")
                
        elif opcion == "2":
            print("Ha seleccionado --> [2]\n")
            estadio: str = mostrar_estadios()
            infracciones_estadio(infracciones, estadio)
            opcion: str = input("\n\nElija una opcion del menu para realizar otra accion: ")
            
        elif opcion == "3":
            print("Ha seleccionado --> [3]\n")
            infracciones_microcentro(infracciones)
            opcion: str = input("\n\nElija una opcion del menu para realizar otra accion: ") 
            
        elif opcion == "4":
            print("Ha seleccionado --> [4]\n")
            robados(infracciones)
            opcion: str = input("\n\nElija una opcion del menu para realizar otra accion: ")
                   
        elif opcion == "5":
            print("Ha seleccionado --> [5]\n")
            
            opcion: str = input("\n\nElija una opcion del menu para realizar otra accion: ")

        elif opcion == "6":
            print("Ha seleccionado --> [6]\n")
            grafico(infracciones)
            opcion: str = input("\n\nElija una opcion del menu para realizar otra accion: ")
                   
        else:
            opcion: str = input("Ingrese una opcion VALIDA para continuar: ")

    else:
        print("\n\nHa seleccionado --> [7]")
        print("Hasta luego, vuelva pronto!!")



# INICIALIZADOR DEL PROGRAMA
def main() -> None:
    print("**** BIENVENIDO ****\n")
    print("========================")
    print("**** MENU PRINCIPAL ****")
    print("========================\n")
    print("[1] - Crear un nuevo archivo de multas")
    print("[2] - Listar las multas cercanas (1km) a los estadios")
    print("[3] - Listar las multas de microcentro")
    print("[4] - Emitir una alerta de vehiculos robados")
    print("[5] - Informacion a partir de dominio, mostrar foto y mapa de google con la ubicacion marcada con un punto")
    print("[6] - Grafico a partir de las denuncias recibidas por mes")
    print("[7] - Salir del programa\n")
    opcion: str = input("Ingrese una opcion para continuar: ")
    menu_principal(opcion)
main()
