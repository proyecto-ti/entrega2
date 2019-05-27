from __future__ import absolute_import, unicode_literals
from celery import task
import requests
from .funciones_bodega import *
from datos import *

@task
def pedir_stock_minimo_grupos():
    pedir = generar_dict_compras()
    liberar_recepcion()
    # Se revisan los tiempos de los pedidos y se cambia de proveedor en caso de no cumplir
    for sku, cantidad in pedir.items():
        iniciar_orden(sku, cantidad, ordenes_por_confirmar)
        liberar_recepcion()

@task
def crear_productos():
    enviar_fabricar()
