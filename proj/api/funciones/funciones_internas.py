import requests
from hashlib import sha1
import hmac
import base64
import json
import math
import time
from requests_files import *
from datos import *

def obtener_id_producto(sku, cantidad, almacenId):
    #lista de almacenes con el producto
    cantidad_id = 0
    lista_id_productos = []
    lista_productos = obtener_sku_con_stock(almacenId)
    for producto in lista_productos:
        if producto['_id'] == sku:
            lista_productos_almacen = obtener_productos_almacen(almacenId, sku)
            for producto_unitario in lista_productos_almacen:
                lista_id_productos.append(producto_unitario['_id'])
                cantidad_id += 1
                if cantidad_id == cantidad:
                    return lista_id_productos
    # en caso de que la cantidad sea mayor que lo que se tiene, igual se entrega la lista con todos los existentes
    return lista_id_productos

def liberar_almacen(almacen):
    #funcion que deja recepcion vacia, se mandan productos a almcanen1 o almacen2
    datos_bodegas = revisarBodega().json()
    #espacio en recepcion
    espacio_usado = datos_bodegas[0]['usedSpace']
    if espacio_usado == 0:
        #almacen ya esta vacion
        return
    else:
        lista_almacen = obtener_sku_con_stock(almacen_id_dict[almacen])
        for producto in lista_almacen:
            #se actualizan datos de bodega
            datos_bodegas = revisarBodega().json()
            #revisa si cabe en almacen1
            if producto['total'] <= datos_bodegas[2]['totalSpace'] - datos_bodegas[2]['usedSpace']:
                #traspasa todos esos productos a almacen1
                mover_entre_almacenes(producto['_id'], producto['total'], almacen_id_dict[almacen], almacen_id_dict["almacen_1"])
            #revisa si cabe en almacen2
            elif producto['total'] <= datos_bodegas[3]['totalSpace'] - datos_bodegas[3]['usedSpace']:
                #traspasa todos esos productos a almacen2
                mover_entre_almacenes(producto['_id'], producto['total'], almacen_id_dict[almacen], almacen_id_dict["almacen_2"])
    return
# MUEVE LA CANTIDAD QUE SE QUIERA DE UN SKU HACIA EL ALMACEN DE DESPACHO
def buscar_mover_producto(almacen_destino, sku, cantidad):
    #cantidad que se ha envidado a despacho
    datos_bodegas = revisarBodega().json()
    capacidad_despacho = datos_bodegas[1]['totalSpace'] - datos_bodegas[1]['usedSpace']
    if capacidad_despacho == 0:
        return
    elif capacidad_despacho >= cantidad:
        cantidad_despachar = cantidad
    else:
        cantidad_despachar = capacidad_despacho
    #revisa si producto esta en pulmon
    lista_pulmon = obtener_sku_con_stock(almacen_id_dict["pulmon"])
    for producto in lista_pulmon:
        if producto['_id'] == sku:
            if producto['total'] >= cantidad_despachar:
                # se tiene la cantidad que se necesita
                return mover_entre_almacenes(sku, cantidad_despachar, almacen_id_dict["pulmon"], almacen_id_dict[almacen_destino])

            elif producto['total'] < cantidad_despachar:
                # no se tiene la cantidad que se necesita, se manda lo que se tiene
                mover_entre_almacenes(sku, producto['total'], almacen_id_dict["pulmon"], almacen_id_dict[almacen_destino])
                cantidad_despachar -= producto['total']
            break
    #revisa si producto esta en recepcion
    lista_recepcion = obtener_sku_con_stock(almacen_id_dict["recepcion"])
    for producto in lista_pulmon:
        if producto['_id'] == sku:
            if producto['total'] >= cantidad_despachar:
                # se tiene la cantidad que se necesita
                return mover_entre_almacenes(sku, cantidad_despachar, almacen_id_dict["recepcion"], almacen_id_dict[almacen_destino])

            elif producto['total'] < cantidad_despachar:
                # no se tiene la cantidad que se necesita, se manda lo que se tiene
                mover_entre_almacenes(sku, producto['total'], almacen_id_dict["recepcion"], almacen_id_dict[almacen_destino])
                cantidad_despachar -= producto['total']
            break
    #revisa si producto esta en almacen1
    lista_almacen1 = obtener_sku_con_stock(almacen_id_dict["almacen_1"])
    for producto in lista_almacen1:
        if producto['_id'] == sku:
            if producto['total'] >= cantidad_despachar:
                #se tiene la cantidad que se necesita
                return mover_entre_almacenes(sku, cantidad_despachar, almacen_id_dict["almacen_1"], almacen_id_dict[almacen_destino])

            elif producto['total'] < cantidad_despachar:
                #no se tiene la cantidad que se necesita, se manda lo que se tiene
                mover_entre_almacenes(sku, producto['total'], almacen_id_dict["almacen_1"], almacen_id_dict[almacen_destino])
                cantidad_despachar -= producto['total']
            break
    #revisa si producto esta en almacen2
    lista_almacen2 = obtener_sku_con_stock(almacen_id_dict["almacen_2"])
    for producto in lista_almacen2:
        if producto['_id'] == sku:
            if producto['total'] >= cantidad_despachar:
                # se tiene la cantidad que se necesita
                return mover_entre_almacenes(sku, cantidad_despachar, almacen_id_dict["almacen_2"], almacen_id_dict[almacen_destino])

            elif producto['total'] < cantidad_despachar:
                # no se tiene la cantidad que se necesita, se manda lo que se tiene
                mover_entre_almacenes(sku, producto['total'], almacen_id_dict["almacen_2"], almacen_id_dict[almacen_destino])
                cantidad_despachar -= producto['total']
            break
    return

def cantidad_producto(sku):
    cantidad = 0
    for almacen in almacen_id_dict:
        lista_productos = obtener_sku_con_stock(almacen_id_dict[almacen])
        for producto in lista_productos:
            if producto['_id'] == sku:
                cantidad += producto['total']
                break
    return cantidad



def update_dictionary_stocks(dictionary, stock_type):
    for sku in stock_type:
        if not sku["_id"] in dictionary:
            dictionary.update({sku["_id"] : sku["total"] })
        else:
            dictionary[sku["_id"]] += sku["total"]
    return dictionary

def stock(view = False):
    stock_recepcion = obtener_sku_con_stock(almacen_id_dict['recepcion'])
    stock_almacen_1 = obtener_sku_con_stock(almacen_id_dict['almacen_1'])
    stock_almacen_2 = obtener_sku_con_stock(almacen_id_dict['almacen_2'])
    stock_pulmon = obtener_sku_con_stock(almacen_id_dict['pulmon'])

    dict = update_dictionary_stocks({}, stock_recepcion)
    dict = update_dictionary_stocks(dict, stock_almacen_1)
    dict = update_dictionary_stocks(dict, stock_almacen_2)
    dict = update_dictionary_stocks(dict, stock_pulmon)


    datos = productos()
    lista = []
    for sku,total in dict.items():
        if view:
            if sku in sku_producidos:
                lista.append({"sku": str(sku), "nombre": str(datos[sku]["nombre"]), "total": total})
        else:
            lista.append({"sku": str(sku), "nombre": str(datos[sku]["nombre"]), "total": total})

    return lista

def entregar_id_almacen(almacen):
    revisar_bodega = revisarBodega()
    if revisar_bodega.status_code == 200:
        for almacenes in revisar_bodega.json():
            if almacenes[almacen] == True:
                return almacenes['_id']
    else:
        return revisar_bodega.status_code

def devolver_cantidad(stock_actual, sku1):
    for elemento in stock_actual:
        if elemento["sku"] == sku1:
            return elemento["total"]
    return 0

def mover_entre_almacenes(sku, cantidad, almacenId_origen, almacenId_destino):
    lista_id = obtener_id_producto(sku, cantidad, almacenId_origen)
    for productoId in lista_id:
        request_mover_entre_almacenes(sku, cantidad, almacenId_origen, almacenId_destino, productoId)

def mover_entre_bodegas(sku, cantidad, almacenId_destino, oc, precio=1):
    lista_id = obtener_id_producto(sku, cantidad, almacen_id_dict["despacho"])
    for productoId in lista_id:
        request_mover_entre_bodegas(sku, cantidad, almacenId_destino, oc, productoId, precio=1)
