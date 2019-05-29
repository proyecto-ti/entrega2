import requests
from hashlib import sha1
import hmac
import base64
import json
import math
import time
from .funciones_internas import *
from .datos import *


def enviar_fabricar():
    productos_ = productos()
    stock2 = stock()
    for element in sku_stock_dict: # recorro elementos con stock minimo
        quantity = devolver_cantidad(stock2, element) # calculo cantidad del elemento en inventario

        if sku_stock_dict[element] > quantity: # si tengo menos productos que el stock minimo

            resta = sku_stock_dict[element] - quantity #calculo cuanto es lo que me falta
            lote = productos_[element]["lote"]  #valor lote
            parte1 = resta // lote #parte entera
            parte2 = resta % lote #resto

            if parte2 !=0 : #si hay resto cuantificador +1
                cuantificador = parte1 + 1
            else: # si no hay resto la cantidad es precisa
                cuantificador = parte1

            # booleano que se setea si no se puede pedir
            for i in range(cuantificador):

                se_puede_pedir = True

                for sku in productos_[element]["receta"]:
                    unitario = productos_[element]["receta"][sku]
                    if devolver_cantidad(stock2, str(sku)) < unitario:
                        se_puede_pedir = False
                        break

                if se_puede_pedir:
                    for sku in productos_[element]["receta"]:
                        for i in range (productos_[element]["receta"][sku]):
                            buscar_mover_producto("despacho", str(sku), 1)
                    fabricarSinPago(element,lote)

                else:
                    break
        else:
            pass
    else:
        pass

#liberar_almacen("recepcion")
#print(enviar_fabricar())
## print(buscar_mover_producto("despacho", "1007", 1))
#
#
# print(obtener_productos_almacen(almacen_id_dict["despacho"], "1007"))
# print(obtener_productos_almacen(almacen_id_dict["recepcion"], "1007"))
# print(obtener_productos_almacen(almacen_id_dict["cocina"], "1007"))
# print(obtener_productos_almacen(almacen_id_dict["almacen_1"], "1007"))
# print(obtener_productos_almacen(almacen_id_dict["almacen_2"], "1007"))
# print(obtener_productos_almacen(almacen_id_dict["pulmon"], "1007"))
