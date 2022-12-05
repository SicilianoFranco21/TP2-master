# GESTOR DE INFRACCIONES

### Universidad de Buenos Aires - Facultad de Ingenieria
### Trabajo Practico N°2 - Algoritmos y Programación 1 - Catedra Costa
### 2do Cuatrimestre 2022
### Grupo 1 - Alabes, Florio Siciliano

## Requisitos previos:
Para poder utilizar este programa correctamente, se debe tener una cuenta creada en la pagina:
https://platerecognizer.com/
Una vez registrado, la misma provee un token para poder utilizar la API de deteccion de placas.
## Como correr el programa:

- Instalar las dependencias: `pip install -r requisitos. txt`
- Reemplazar el token de `https://platerecognizer.com/` en el archivo `utils.py` (constante API_TOKEN)
- Ejecutar el script principal: `python3 main.py`

# Aclaraciones utiles:

El programa utiliza la API de ALPR para el reconocimiento de placas. Esta pagina provee al usuario con un token, el cual le permite realizar 2500 llamados a dicha API. en caso de que el programa rompa antes de mostrar el menu principal, por favor verifique:
- Haber instalado correctamente todas las dependencias
- Revisar la cantidad de llamados a la API disponibles.
