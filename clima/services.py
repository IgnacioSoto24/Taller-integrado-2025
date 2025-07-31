import requests
from .models import Ciudad, Clima
from django.utils import timezone

API_KEY = '1a794296b088fc37c4a065704422a10a'

def obtener_coordenadas_ciudad(nombre_ciudad, pais='CL'):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={nombre_ciudad},{pais}&limit=1&appid={API_KEY}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return None
    
    datos = response.json()
    if not datos:
        return None

    return {
        'latitud': datos[0]['lat'],
        'longitud': datos[0]['lon']
    }

def obtener_datos_clima(ciudad):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={ciudad.latitud}&lon={ciudad.longitud}&appid={API_KEY}&units=metric&lang=es"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    datos = response.json()
    clima = Clima.objects.create(
        ciudad=ciudad,
        fecha_consulta=timezone.now(),
        temperatura=datos['main']['temp'],
        humedad=datos['main']['humidity'],
        presion=datos['main']['pressure'],
        descripcion=datos['weather'][0]['description'],
        icono=datos['weather'][0]['icon']
    )
    return clima
