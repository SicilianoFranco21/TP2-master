# en este archivo se busca demostrar que el detector de patente funciona correctamente.

from utils import *

def main():
    patente = obtener_patente('imgs/perro.jpg')
    print(f'patente: {patente}')

    patente_2 = obtener_patente('imgs/000.png')
    print(f'patente 2: {patente_2}')

main()