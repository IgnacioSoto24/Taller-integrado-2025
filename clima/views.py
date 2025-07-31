import json
from django.shortcuts import render, redirect
from .models import Ciudad, Clima
from .services import obtener_datos_clima, obtener_coordenadas_ciudad
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from django.shortcuts import get_object_or_404

def inicio(request):
    ciudades = Ciudad.objects.all()
    datos = []

    for ciudad in ciudades:
        clima_actual = ciudad.climas.order_by('-fecha_consulta').first()
        if clima_actual:
            icono_url = f"http://openweathermap.org/img/wn/{clima_actual.icono}@2x.png"
            datos.append({
                'ciudad': ciudad.nombre,
                'pais': ciudad.pais,
                'temperatura': clima_actual.temperatura,
                'humedad': clima_actual.humedad,
                'presion': clima_actual.presion,
                'descripcion': clima_actual.descripcion,
                'fecha': clima_actual.fecha_consulta,
                'icono_url': icono_url,
            })

    return render(request, 'clima/inicio.html', {'datos': datos})


def agregar_ciudad(request):
    if request.method == 'POST':
        nombre_ciudad = request.POST.get('nombre')
        pais = request.POST.get('pais', 'CL').upper()

        if Ciudad.objects.filter(nombre__iexact=nombre_ciudad, pais=pais).exists():
            messages.warning(request, 'La ciudad ya existe.')
            return redirect('inicio')

        coords = obtener_coordenadas_ciudad(nombre_ciudad, pais)
        if not coords:
            messages.error(request, 'No se pudo encontrar la ciudad.')
            return redirect('inicio')

        ciudad = Ciudad.objects.create(
            nombre=nombre_ciudad,
            pais=pais,
            latitud=coords['latitud'],
            longitud=coords['longitud']
        )

        obtener_datos_clima(ciudad)
        messages.success(request, 'Ciudad agregada correctamente.')
        return redirect('inicio')

    return render(request, 'clima/agregar_ciudad.html')


def graficos(request):
    ciudades = Ciudad.objects.all()
    datos_temperatura_historica = {}
    datos_actuales = []

    for ciudad in ciudades:
        registros = Clima.objects.filter(ciudad=ciudad).order_by('fecha_consulta')
        temperaturas = [c.temperatura for c in registros]
        fechas = [c.fecha_consulta.strftime("%d-%m %H:%M") for c in registros]

        if registros:
            ultimo = registros.last()
            datos_actuales.append({
                'ciudad': ciudad.nombre,
                'temperatura': ultimo.temperatura,
                'humedad': ultimo.humedad,
                'presion': ultimo.presion
            })

            datos_temperatura_historica[ciudad.nombre] = {
                'fechas': fechas,
                'temperaturas': temperaturas
            }

    return render(request, 'clima/graficos.html', {
        'historico': json.dumps(datos_temperatura_historica),
        'actuales': json.dumps(datos_actuales)
    })

def actualizar_clima(request):
    ciudades = Ciudad.objects.all()
    for ciudad in ciudades:
        obtener_datos_clima(ciudad)
    messages.success(request, 'Datos del clima actualizados correctamente.')
    return redirect('inicio')

def detalle_ciudad(request, ciudad_id):
    ciudad = get_object_or_404(Ciudad, id=ciudad_id)
    climas = ciudad.climas.order_by('-fecha_consulta')[:10]

    return render(request, 'clima/detalle_ciudad.html', {
        'ciudad': ciudad,
        'climas': climas
    })

def sobre_proyecto(request):
    return render(request, 'clima/sobre.html')