from __future__ import absolute_import, unicode_literals
from celery import task
import requests
from .funciones_bodega import *

@task
def pedir_stock_minimo_grupos():
    print("hola")
    # pedir = generar_dict_compras()
    # liberar_recepcion()
    # for sku, cantidad in pedir.items():
    #     pedir_productos_sku(sku, 3)
    #     pedir_productos_sku(sku, 3, url_changed=True)
    #     liberar_recepcion()

@task
def crear_productos():
    print("hola")
    #enviar_fabricar()
