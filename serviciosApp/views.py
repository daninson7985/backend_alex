import json
from pathlib import Path
from django.shortcuts import render

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'


def leer_json(nombre_archivo):
    ruta = DATA_DIR / nombre_archivo
    with open(ruta, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)


def servicios(request):
    servicios_lista = leer_json('servicios_detalle.json')
    busqueda = request.GET.get('q', '').strip()

    if busqueda:
        servicios_lista = [
            item for item in servicios_lista
            if busqueda.lower() in item.get('nombre', '').lower()
            or busqueda.lower() in item.get('categoria', '').lower()
            or busqueda.lower() in item.get('descripcion', '').lower()
        ]

    cantidad = len(servicios_lista)
    contexto = {
        "servicios_lista": servicios_lista,
        "cantidad": cantidad,
        "busqueda": busqueda,
    }
    return render(request, 'servicios.html', contexto)


def detalle_servicio(request):
    servicios_lista = leer_json('servicios_detalle.json')
    primer_servicio = servicios_lista[0] if servicios_lista else {}
    contexto = {
        "servicio": primer_servicio,
        "servicios_lista": servicios_lista,
    }
    return render(request, 'servicios_detalle.html', contexto)

