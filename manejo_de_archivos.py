from funciones import *
from utils import *
import csv
import os
from msvcrt import getch

def cls() -> None:
    # funcion que permite limpiar la consola
    os.system('cls' if os.name=='nt' else 'clear')



def leer_archivo_csv() -> list[dict]:

    # Función que lee el archivo de infracciones y devuelve una lista de diccionarios con los datos de cada infracción.
    # Cada infracción es un diccionario con los siguientes campos:
    # timestamp, telefono, latitud, longitud, ruta_foto, descripcion_texto, ruta_audio, direccion, localidad, provincia, patente, descripcion_audio

    cls()
    infracciones: list = []
    with open('Infracciones.csv', 'r') as archivo_csv:
        lector = csv.reader(archivo_csv, delimiter=',')
        for linea in lector:
            timestamp: str = linea[0]
            telefono: int = linea[1]
            latitud: float = linea[2]
            longitud: float = linea[3]
            ruta_foto: str = linea[4]
            descripcion: str = linea[5]
            ruta_audio: str = linea[6]
            coordenadas: str = str(latitud + "," + longitud)
            ubicacion : str = obtener_direccion(coordenadas)
            direccion: str = ubicacion[0]
            localidad: str = ubicacion[1]
            provincia: str = ubicacion[2]
            patente: str = obtener_patente(ruta_foto)
            descripcion_audio: str = obtener_audio(ruta_audio)
            
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


def crear_archivo_csv(infracciones: list[dict]) -> None:

    # Función que crea un archivo CSV con los datos de las infracciones.
    # precondición: recibe una lista de diccionarios con los datos de las infracciones.
    # postcondición: crea un archivo CSV con los datos de las infracciones, pero no devuelve nada.
    
    cls()
    with open("informe_infracciones.csv", "w", newline="") as archivo_csv:
        writer = csv.writer(archivo_csv, delimiter=',')
        writer.writerow(
            ["timestamp", 
            "telefono", 
            "direccion", 
            "localidad", 
            "provincia", 
            "patente", 
            "descripcion_texto", 
            "descripcion_audio"]
            )
        for infraccion in infracciones:
            writer.writerow(
                [infraccion['timestamp'], 
                infraccion['telefono'], 
                infraccion['direccion'], 
                infraccion['localidad'], 
                infraccion['provincia'], 
                infraccion['patente'], 
                infraccion['descripcion_texto'], 
                infraccion['descripcion_audio']]
                )
    print("\nEl archivo informe_infracciones.csv se ha creado exitosamente!\n Presione cualquier tecla para continuar...")
    getch()


def leer_archivo_txt() -> list:

    # funcion que permite leer un archivo txt y guardar los datos en una lista
    # precondicion: recibe un archivo txt
    # postcondicion: devuelve una lista con los datos del archivo txt

    patentes_robadas: list = []  
    with open('robados.txt', 'r') as archivo_txt:
        for linea in archivo_txt:
            patentes_robadas.append(linea.strip())
    return patentes_robadas
