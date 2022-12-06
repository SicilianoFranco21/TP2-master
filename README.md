# GESTOR DE INFRACCIONES
 Universidad de Buenos Aires - Facultad de Ingenieria //
 Trabajo Practico N°2 - Algoritmos y Programación 1 - Catedra Costa //
2do Cuatrimestre 2022 //
Grupo 1 - Alabes, Cardenas, Florio, Siciliano

## Requisitos previos:

Para poder utilizar este programa correctamente, se debe tener una cuenta creada en la pagina:
https://platerecognizer.com/ . 
Una vez registrado, la misma provee un token para poder utilizar la API de deteccion de placas.

## Contenido del Repositorio

Dentro del repositorio, podremos encontrar los siguientes archivos y directorios:
- `audios`, carpeta donde se almacenan los audios en formato.wav
- `imgs`, carpeta donde se almacenan las imagenes del programa.
- `infracciones.csv`, archivo csv que se utiliza para crear una estructura de datos.
- `README.md`, archivo de instrucciones y de informacion util.
- `funciones.py`, archivo donde se almacenan las funciones correspondientes al desarrollo de los puntos del tp.
- `main.py`, archivo principal del TP.
- `manejo_de_archivos.py`, archivo que se encarga de interpretar los archivos con formato distinto a py. En este caso, este archivo es el encargado de leer `infracciones.csv` y `robados.txt` para su uso correcto en el programa y de crear el archivo `informe infracciones.csv` cuando el usuario asi lo solicite.
- `prueba.py`, archivo donde se demuestra que el interprete de patentes devuelve patentes unicamente si este las detecta.
- `requisitos.txt`, archivo donde se almacenan las dependencias del TP.
- `robados.txt`, archivo que almacena una lista de patentes a ser utilizadas en uno de los puntos del TP.
- `utils.py`, archivo donde se almacenan funciones utiles para facilitar el desarrollo del TP.

## Como correr el programa:

- Instalar las dependencias: `pip install -r requisitos. txt`
- Reemplazar el token de https://platerecognizer.com/ en el archivo `utils.py` (constante API_TOKEN)
- Ejecutar el script principal: `python main.py`

## Aclaraciones utiles:

El programa utiliza la API de ALPR para el reconocimiento de placas. Esta pagina provee al usuario con un token, el cual le permite realizar 2500 llamados a dicha API. en caso de que el programa rompa antes de mostrar el menu principal, por favor verifique:
- Haber instalado correctamente todas las dependencias
- Revisar la cantidad de llamados a la API disponibles.

