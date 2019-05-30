import requests
from hashlib import sha1
import hmac
import base64
import json
import math
import time
# from .requests_files import *
# from .datos import *
from .funciones_internas import *

def calcular_stock_unidades(stock_actual, diccionario):
    dict_compras_cantidad = dict()
    for sku in diccionario:
        element = diccionario[sku]
        if element['stock_minimo'] is not None:
            cantidad_actual = devolver_cantidad(stock_actual, sku)#funcion_que retorna int(element.sku)
            if cantidad_actual < element['stock_minimo']:
                cantidad_pedir = element['lote'] * math.ceil((element['stock_minimo']-cantidad_actual)/element['lote'])
                dict_compras_cantidad[sku] = cantidad_pedir
    return dict_compras_cantidad

# ENTREGA MATERIAS PRIMAS NECESARIAS PARA CUMPLIR STOCK MINIMO
# SE VA ACTUALIZANDO EL DICCIONARIO HASTA LLEGAR A PRODUCTOS QUE NO TIENEN INGREDIENTES
def calcular_cantidad_comprar(dict_producto, dict_comprar, dict_compra_final = {}):
    for sku, cantidad in dict_comprar.items():
        if cantidad != 0:
            if dict_producto[str(sku)]['receta'] == {}:

                if str(sku) in dict_compra_final:
                    dict_compra_final[str(sku)] += cantidad
                else:
                    dict_compra_final[str(sku)] = cantidad
                dict_comprar[sku] = 0
            else:
                dict_aux = {}
                for element in dict_producto[str(sku)]['receta']:
                    cantidad_element = dict_producto[str(sku)]['receta'][element] * cantidad / dict_producto[str(sku)]['lote']
                    dict_aux[element] = cantidad_element
                    #time.sleep(1)

                    dict_compra_final.update(calcular_cantidad_comprar(dict_producto, dict_aux, dict_compra_final))

    return dict_compra_final

# LLAMA A calcular_cantidad_comprar RESTANDO LAS MATERIAS PRIMAS DEL INVENTARIO
def generar_dict_compras():
    datos_productos = productos()
    stock_actual = stock()
    calcular_stock_unidades_ = calcular_stock_unidades(stock_actual, datos_productos)
    dict_compra_final = calcular_cantidad_comprar(datos_productos, calcular_stock_unidades_)

    for materias_primas in stock_actual:
        sku = materias_primas['sku']
        if sku in dict_compra_final:
            if dict_compra_final[sku] < materias_primas['total']:
                del dict_compra_final[sku]
            else:
                dict_compra_final[sku] -= materias_primas['total']

    return dict_compra_final

#le pido a los grupos #
def pedir_prod_grupox(sku, cantidad, grupo):
    json_crear_oc = crear_oc(grupo_proveedor=grupo, sku=sku, cantidad=cantidad, preciounitario=1, canal = 'b2b')
    oc_id = json_crear_oc.json()["_id"]
    response = post_orders_grupox(grupo = grupo, oc_id=oc_id, cantidad=cantidad, sku=sku)
    print("Grupo: ", grupo, "sku:", sku, "Response:", response.json())

#pedimos los productos que no tenemos
def pedir_productos_sku(sku, cantidad, url_changed=False):
    datos = productos()
    productores = datos[sku]["productores"]
    #if datos[sku]["propio"] != True:
    for grupo in productores:
        if grupo != 2:
            try:
                result = get_inventories_grupox(grupo)
                if result.status_code == 200 or result.status_code == 201:
                    result_2 = pedir_prod_grupox(sku, cantidad, grupo)
                    print("GRUPO", grupo, result_2.json())
                else:
                    pass
            except:
                pass
#    else:
    #    cantidad = datos[sku]['lote'] * math.ceil(cantidad/datos[sku]['lote'])
        #print(fabricarSinPago(sku, cantidad))

#print(pedir_productos_sku("1001", 3))

def pedir_prod_profesor(sku, cantidad):
    datos = productos()
    productores = datos[sku]["productores"]
    if datos[sku]["propio"] == True:
        print("SKU", sku, "Cantidad", cantidad)
        cantidad = datos[sku]['lote'] * math.ceil(cantidad/datos[sku]['lote'])
        print(fabricarSinPago(sku, cantidad))

def pedir_stock_minimo_grupos():
    pedir = generar_dict_compras()
    liberar_almacen("recepcion")
    # Se revisan los tiempos de los pedidos y se cambia de proveedor en caso de no cumplir
    for sku, cantidad in pedir.items():
        pedir_productos_sku(sku, 3  )
        liberar_almacen("recepcion")


def pedir_profesor():
    pedir = generar_dict_compras()
    liberar_almacen("recepcion")
    for sku, cantidad in pedir.items():
        pedir_prod_profesor(sku, cantidad)
        liberar_almacen("recepcion")

#pedir_profesor()
#pedir_productos_sku("1007", 3)
#pedir_productos_sku("1007", 3)



#pedir_stock_minimo_grupos()
