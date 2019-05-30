from __future__ import absolute_import, unicode_literals
from celery import task
import requests
from .funciones.pedir_grupo import *
from .funciones.fabricar import *
from .funciones.ftp import *

@task
def pedir_stock_minimo_grupos():
     pedir = generar_dict_compras()
     liberar_almacen("recepcion")
     #Se revisan los tiempos de los pedidos y se cambia de proveedor en caso de no cumplir
     for sku, cantidad in pedir.items():
         pedir_productos_sku(sku, 3)
         liberar_almacen("recepcion")

@task
def crear_productos():
    enviar_fabricar()

@task
def pedir_profesor():
  pedir = generar_dict_compras()
  liberar_almacen("recepcion")
  for sku, cantidad in pedir.items():
      pedir_prod_profesor(sku, 2)
      liberar_almacen("recepcion")

# 
# @task
# def cocinar_task():
#     ver_buzon()
#
# @task
# def verificar_task():
#     verificar()
