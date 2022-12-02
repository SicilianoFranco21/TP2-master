#Archivo previsorio para testear y guardar progreso de "x" funcion, sin adulterar totalmente el codigo principal

infracciones: list[dict] = [
        {'timestamp': '2022-11-12 19:21:59', 
        'telefono': ' "1160504268"', 
        'latitud': ' -34.576324', 
        'longitud': ' -58.374165', 
        'ruta_foto': 'imgs/023.png', 
        'patente': 'ae410he', 
        'descripcion': ' "descripcion de la foto"', 
        'coordenadas': ' -34.576324,  -58.374165'
        },     
        {
        'timestamp': '2022-11-13 09:47:59', 
         'telefono': ' "1135774367"', 
         'latitud': ' -34.577912', 
         'longitud': ' -58.419308', 
         'ruta_foto': 'imgs/024.png', 
         'patente': 'ae444jh', 
         'descripcion': ' "descripcion de la foto"', 
         'coordenadas': ' -34.577912,  -58.419308'
         }
            ]

#Primer experimento
#for elemento in data:
#    print(elemento)
#OUTPUT: {'timestamp': '2022-11-12 19:21:59', 'telefono': ' "1160504268"', 'latitud': ' -34.576324', 'longitud': ' -58.374165', 'ruta_foto': 'imgs/023.png', ... }


#Segundo experimento
#for elemento in data:
#    print(elemento['timestamp'][5:7])
#OUTPUT: 11 
# Significa que nos imprime el caracter de los meses


lista_impresa: bool = False
while not lista_impresa:
    lista_infracciones_estadio: list = []
    
    for index in range(len(infracciones)):
        latitud = infracciones[index]["latitud"]
        longitud = infracciones[index]["longitud"]
        coordenadas = latitud + "," + longitud
        
        lista_infracciones_estadio.append(latitud)
        lista_infracciones_estadio.append(longitud)
        lista_infracciones_estadio.append(coordenadas)
    
    lista_impresa: bool = True
    
print(lista_infracciones_estadio)
# ----------------------------------------------
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