from __future__ import absolute_import, unicode_literals
from celery import task
import requests
from .funciones.pedir_grupo import *
from .funciones.fabricar import *


@task
def pedir_stock_minimo_grupos():
    print("hoal")
    pedir = generar_dict_compras()
    liberar_almacen("despacho")
    # Se revisan los tiempos de los pedidos y se cambia de proveedor en caso de no cumplir
    for sku, cantidad in pedir.items():
        iniciar_orden(sku, cantidad)
        liberar_almacen("despacho")

@task
def crear_productos():
    print("hola")
    enviar_fabricar()
