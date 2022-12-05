from funciones import *
from manejo_de_archivos import *
import os


def cls() -> None:
    # funcion que permite limpiar la consola
    os.system('cls' if os.name=='nt' else 'clear')


def main() -> None:
    infracciones: list[dict] = leer_archivo_csv()
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
