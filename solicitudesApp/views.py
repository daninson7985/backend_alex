import json
from pathlib import Path
from django.shortcuts import render

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'


def leer_json(nombre_archivo):
    ruta = DATA_DIR / nombre_archivo
    with open(ruta, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)


def inicio(request):
    titulo = "Municipalidad de La Serena"
    mensaje = "Sistema de gestión y seguimiento de solicitudes ciudadanas"
    servicios = leer_json('servicios.json')
    total_servicios = len(servicios)
    usuario = "Funcionario municipal"
    es_admin = True

    if es_admin:
        estado = "Acceso autorizado"
    else:
        estado = "Acceso restringido"

    contexto = {
        "titulo": titulo,
        "mensaje": mensaje,
        "servicios": servicios,
        "total_servicios": total_servicios,
        "usuario": usuario,
        "estado": estado,
    }
    return render(request, 'inicio.html', contexto)


def solicitudes(request):
    solicitudes_lista = leer_json('solicitudes.json')
    busqueda = request.GET.get('q', '').strip()

    if busqueda:
        solicitudes_lista = [
            item for item in solicitudes_lista
            if busqueda.lower() in item.get('nombre', '').lower()
            or busqueda.lower() in item.get('sector', '').lower()
            or busqueda.lower() in item.get('descripcion', '').lower()
        ]

    cantidad = len(solicitudes_lista)
    contexto = {
        "solicitudes_lista": solicitudes_lista,
        "cantidad": cantidad,
        "busqueda": busqueda,
    }
    return render(request, 'solicitudes.html', contexto)


def acerca(request):
    nombre_proyecto = "Portal de Solicitudes Municipales"
    version = "1.0.0"
    tecnologias = ["Python", "Django", "Bootstrap", "JSON"]
    contexto = {
        "nombre_proyecto": nombre_proyecto,
        "version": version,
        "tecnologias": tecnologias,
    }
    return render(request, 'acerca.html', contexto)