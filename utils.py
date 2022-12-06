import os
import requests
from geopy.geocoders import Nominatim
import speech_recognition as sr


def cls() -> None:
    # funcion que permite limpiar la consola
    os.system('cls' if os.name=='nt' else 'clear')


API_TOKEN: str = 'Token 06314a64093e9225ccf62c5872988131c9c5909c'


def obtener_patente(ruta_foto: str) -> str:

    # funcion que permite obtener la patente de un vehiculo a partir de una foto
    # precondicion: recibe un string con la ruta de la foto
    # postcondicion: devuelve un string con la patente del vehiculo
    
    regions: list = ['ar', 'us-ca'] 
    try:
        with open(ruta_foto, 'rb') as fp:
            response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                data=dict(regions=regions),
                files=dict(upload=fp),
                headers={'Authorization': API_TOKEN})
            patente : str = response.json()['results'][0]['plate']
            return patente
    except IndexError:
        print('No se detectó patente')

def obtener_audio(ruta_audio) -> str:
    
    # funcion que permite obtener el texto de un audio
    # precondicion: recibe un string con la ruta del audio
    # postcondicion: devuelve un string con el texto del audio

    r = sr.Recognizer()
    with sr.AudioFile(ruta_audio) as source:
        audio : str = r.listen(source)
        texto_audio : str = r.recognize_google(audio,language='es-AR')
    return texto_audio


def obtener_direccion(coordenadas: str):

    # funcion que permite obtener la direccion de un lugar a partir de sus coordenadas
    # precondicion: recibe un string con las coordenadas del lugar
    # postcondicion: devuelve 3 strings, correspondiendo cada uno respectivamente a la direccion, localidad y provincia del lugar
    
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


def fecha_a_partir_de_timestamp(timestamp: str) -> str:

    # funcion que permite obtener la fecha a partir de un timestamp
    # precondicion: recibe un string con el timestamp
    # postcondicion: devuelve un string con la fecha en formato 'dd de mes de aaaa'

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


