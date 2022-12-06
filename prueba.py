# en este archivo se busca demostrar que el detector de patente funciona correctamente.
import time
from utils import *

def lista_de_fotos() -> list[str]:
    fotos: list[str] = []
    with open("prueba.csv", "r") as archivo:
        for linea in archivo:
            fotos.append(linea.strip())

    return fotos


def main() -> None:
    fotos: list[str] = lista_de_fotos()
    for foto in fotos:
        time.sleep(1.5)
        print(f"patente: {obtener_patente(foto)}")

main()