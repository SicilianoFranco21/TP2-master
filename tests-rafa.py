from geopy.geocoders import Nominatim


# obtener coordenadas a partir de un lugar:
def get_coords(place):
        geolocator = Nominatim(user_agent="tp2")
        location = geolocator.geocode(place)
        return location.latitude, location.longitude

def main():
        cerrar: bool = False
        while not cerrar:
                lugar: str = input("Ingrese un lugar: ")
                if lugar == "cerrar":
                        cerrar = True
                else:
                        lat, lon = get_coords(lugar)
                        print(f"{lat}, {lon}")

main()