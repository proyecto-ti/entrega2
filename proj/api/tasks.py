from __future__ import absolute_import, unicode_literals
from celery import task
import requests
from .funciones_bodega import *
from datos import *

@task
def pedir_stock_minimo_grupos():
    print("hola")
    # pedir = generar_dict_compras()
    # liberar_recepcion()
    # # Se revisan los tiempos de los pedidos y se cambia de proveedor en caso de no cumplir
    # ordenes_por_confirmar_celery_control(ordenes_por_confirmar)
    # for sku, cantidad in pedir.items():
    #     iniciar_orden(sku, cantidad, ordenes_por_confirmar)
    #     liberar_recepcion()

@task
def crear_productos():
    print("Hola")
    #enviar_fabricar()
