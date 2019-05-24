import requests
from hashlib import sha1
import hmac
import base64
import json
import math
import time
from datos import *

api_key = 'A#soL%kRvHX2qHm'
api_url_base = 'https://integracion-2019-dev.herokuapp.com/bodega/'
api_oc_url_base = 'https://integracion-2019-dev.herokuapp.com/oc/'

almacen_id_dict = {"recepcion": "5cc7b139a823b10004d8e6d3",
                    "despacho": "5cc7b139a823b10004d8e6d4",
                    "almacen_1": "5cc7b139a823b10004d8e6d5",
                    "almacen_2": "5cc7b139a823b10004d8e6d6",
                    "pulmon": "5cc7b139a823b10004d8e6d7",
                    "cocina": "5cc7b139a823b10004d8e6d8"}

sku_stock_dict = {  "1101": 100, "1111": 100, "1301" : 50, "1201" : 250, "1209" : 20, "1109" : 50,"1309" : 170,
                    "1106": 400,"1114": 50,"1215" : 20,"1115" : 30,"1105" : 50,
                    "1216": 50,"1116": 250,"1110" : 80,"1310" : 20,
                    "1210": 150,"1112": 130,"1108" : 10,"1407" : 40,"1207" : 20,
                    "1107": 50,"1307": 170,"1211" : 60}

sku_producidos = ["1001", "1002", "1006", "1010", "1011", "1012", "1014", "1016"]

pedidos_nuestros = list()

# AMBIENTE DE DESARROLLO
id_grupos = {1: "5cbd31b7c445af0004739be3", 2: "5cbd31b7c445af0004739be4", 3: "5cbd31b7c445af0004739be5",
             4: "5cbd31b7c445af0004739be6", 5: "5cbd31b7c445af0004739be7", 6: "5cbd31b7c445af0004739be8",
             7: "5cbd31b7c445af0004739be9", 8: "5cbd31b7c445af0004739bea", 9: "5cbd31b7c445af0004739beb",
             10: "5cbd31b7c445af0004739bec", 11: "5cbd31b7c445af0004739bed", 12: "5cbd31b7c445af0004739bee",
             13: "5cbd31b7c445af0004739bef", 14: "5cbd31b7c445af0004739bf0"}

# AMBIENTE DE PRODUCCION
"""
id_grupos_prod = {1: "5cc66e378820160004a4c3bc", 2: "5cc66e378820160004a4c3bd", 3: "5cc66e378820160004a4c3be",
             4: "5cc66e378820160004a4c3bf", 5: "5cc66e378820160004a4c3c0", 6: "5cc66e378820160004a4c3c1",
             7: "5cc66e378820160004a4c3c2", 8: "5cc66e378820160004a4c3c3", 9: "5cc66e378820160004a4c3c4",
             10: "5cc66e378820160004a4c3c5", 11: "5cc66e378820160004a4c3c6", 12: "5cc66e378820160004a4c3c7",
             13: "5cc66e378820160004a4c3c8", 14: "5cc66e378820160004a4c3c9"}
"""




###FUNCION DE HASH NO UTILIZAR###
def sign_request(string):

    # key = b"CONSUMER_SECRET&" #If you dont have a token yet
    key = str.encode(api_key)
    # The Base String as specified here:
    raw = str.encode(string) # as specified by OAuth

    hashed = hmac.new(key, raw, digestmod=sha1)

    hashed_bytes = hashed.digest()
    # The signature
    encoded = base64.b64encode(hashed_bytes)
    encoded = str(encoded, 'UTF-8')
    return encoded


# METODOS DE OC
def anular_oc(id_oc, motivo_anulacion):
    message = 'DELETE'
    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    url = '{}crear'.format(api_oc_url_base)
    body = {"id": id_oc, "anulacion": motivo_anulacion}

    result = requests.delete(url, headers=headers, data=json.dumps(body))
    return result.json()


def crear_oc(grupo_proveedor, sku, cantidad, preciounitario, canal):
    message = 'PUT'
    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    url = '{}crear'.format(api_oc_url_base)
    body = {"cliente": id_grupos[2], "proveedor": id_grupos[grupo_proveedor], "sku": sku, "fechaEntrega": int(time.time()*1000+10*60*1000),
            "cantidad": int(cantidad), "precioUnitario": preciounitario, "canal": canal, "urlNotificacion":
                "http://tuerca2.ing.puc.cl/oc/{_id}/notification/"}

    result = requests.put(url, headers=headers, data=json.dumps(body))
    return result.json()


def obtener_oc(id_oc):
    message = 'GET'
    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    url = '{}obtener/{}'.format(api_oc_url_base, id_oc)
    result = requests.get(url, headers=headers)
    return result.json()


def recepcionar_oc(id_oc):
    message = 'POST'
    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    url = '{}recepcionar/{}'.format(api_oc_url_base, id_oc)
    body = {"id": id_oc}
    result = requests.post(url, headers=headers, data=json.dumps(body))
    return result.json()


def rechazar_oc(id_oc, motivo_rechazo):
    message = 'POST'
    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    url = '{}rechazar/{}'.format(api_oc_url_base, id_oc)
    body = {"id": id_oc, "rechazo": motivo_rechazo}
    result = requests.post(url, headers=headers, data=json.dumps(body))
    return result.json()
"""
print(crear_oc(3, 1006, 3, 1000, "b2b"))
print(obtener_oc("5cdf2ec978171f00042fb823"))
print(recepcionar_oc("5cdf2ec978171f00042fb823"))
print(rechazar_oc("5cdf336978171f00042fb831", "hola")) """
#print(anular_oc("5cdf346478171f00042fb833", "chao"))

def aviso_aceptar_pedido(oc, grupo):
    url = 'http://tuerca' + str(grupo) + '.ing.puc.cl/oc/{}/notification'.format_map(oc)
    headers = {'Content-Type': 'application/json'}
    body = {"status": "accept"}
    result = requests.post(url, headers=headers, data=json.dumps(body))
    return result.json()

def aviso_rechazar_pedido(oc, grupo):
    url = 'http://tuerca' + str(grupo) + '.ing.puc.cl/oc/{}/notification'.format_map(oc)
    headers = {'Content-Type': 'application/json'}
    body = {"status": "reject"}
    result = requests.post(url, headers=headers, data=json.dumps(body))
    return result.json()

#ENTREGA SKU DE PRODUCTOS CON STOCK EN UN ALMACEN Y SU CANTIDAD
def obtener_sku_con_stock(almacenId):
    message = 'GET' + almacenId
    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    url = '{}skusWithStock?almacenId={}'.format(api_url_base, almacenId)
    result = requests.get(url, headers=headers).json()
    return result

#for almacen in almacen_id_dict:
#    print(obtener_sku_con_stock(almacen_id_dict[almacen]))

# ENTREGA EL TIPO DE ALMACEN, CAPACIDAD Y ESPACIO USADO
def revisarBodega():
    url = '{}almacenes/'.format(api_url_base)

    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request('GET'))}

    result = requests.get(url, headers=headers)
    return result

#for almacen in revisarBodega().json():
#    print(obtener_sku_con_stock(almacen['_id']))


def entregar_id_almacen(almacen):
    revisar_bodega = revisarBodega()
    if revisar_bodega.status_code == 200:
        for almacenes in revisar_bodega.json():
            if almacenes[almacen] == True:
                return almacenes['_id']
    else:
        return revisar_bodega.status_code


#print(revisarBodega())
#print(entregar_id_almacen("recepcion"))

# FABRICA PRODUCTOS PROCESADOS SI SE TIENEN LAS MATERIAS PRIMAS NECESARIAS EN EL DESPACHO

def fabricarSinPago(sku, cantidad):
    message = 'PUT' + sku + str(cantidad)
    url = '{}fabrica/fabricarSinPago'.format(api_url_base)
    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    body = {"sku": sku, "cantidad": int(cantidad)}

    result = requests.put(url, headers=headers, data=json.dumps(body))
    return result.json()

    #if result.status_code == 200:
    #    return result.json()
    #else:
    #    return result.json()

#print(fabricarSinPago("1006", 10))

######TODO ESTO ES PARA INVENTORIES GET
def update_dictionary_stocks(dictionary, stock_type):
    for sku in stock_type:
        if not sku["_id"] in dictionary:
            dictionary.update({sku["_id"] : sku["total"] })
        else:
            dictionary[sku["_id"]] += sku["total"]
    return dictionary

def stock_fixed():
    stock_recepcion = obtener_sku_con_stock(almacen_id_dict['recepcion'])
    print("Stock recepcion")
    print(type(stock_recepcion))
    print(stock_recepcion)
    stock_almacen_1 = obtener_sku_con_stock(almacen_id_dict['almacen_1'])
    print("Stock almacen 1")
    print(type(stock_almacen_1))
    print(stock_almacen_1)
    stock_almacen_2 = obtener_sku_con_stock(almacen_id_dict['almacen_2'])
    print("Stock almacen 2")
    print(type(stock_almacen_2))
    print(stock_almacen_2)
    stock_pulmon = obtener_sku_con_stock(almacen_id_dict['pulmon'])
    print("Stock pulmon")
    print(type(stock_pulmon))
    print(stock_pulmon)
    #print("Recepcion", stock_recepcion)
    #print("Almacen 1", stock_almacen_1)
    #print("Almacen 2", stock_almacen_2)
    #print("Pulmon", stock_pulmon)

    #[{'_id': '1012', 'total': 1}, {'_id': '1310', 'total': 48},
    dict_response = dict()
    for item in stock_recepcion:
        if item["_id"] in dict_response.keys():
            dict_response[item["_id"]] += item["total"]
        else:
            dict_response[item["_id"]] = item["total"]
    for item in stock_almacen_1:
        if item["_id"] in dict_response.keys():
            dict_response[item["_id"]] += item["total"]
        else:
            dict_response[item["_id"]] = item["total"]
    for item in stock_almacen_2:
        if item["_id"] in dict_response.keys():
            dict_response[item["_id"]] += item["total"]
        else:
            dict_response[item["_id"]] = item["total"]
    for item in stock_pulmon:
        if item["_id"] in dict_response.keys():
            dict_response[item["_id"]] += item["total"]
        else:
            dict_response[item["_id"]] = item["total"]

    datos = productos()
    list_skus = dict_response.keys()
    list_response = list()
    for sku in list_skus:
        if sku in sku_producidos:
            list_response.append({"sku": sku, "nombre": datos[sku]["nombre"], "total": dict_response[sku]})
    #print(list_response)
    return list_response


def stock(view = False):
    stock_recepcion = obtener_sku_con_stock(almacen_id_dict['recepcion'])
    stock_almacen_1 = obtener_sku_con_stock(almacen_id_dict['almacen_1'])
    stock_almacen_2 = obtener_sku_con_stock(almacen_id_dict['almacen_2'])
    stock_pulmon = obtener_sku_con_stock(almacen_id_dict['pulmon'])
    #print("Recepcion", stock_recepcion)
    #print("Almacen 1", stock_almacen_1)
    #print("Almacen 2", stock_almacen_2)
    #print("Pulmon", stock_pulmon)
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

#####################################

# PARA UN SKU DADO EN UN ALMACEN, ENTREGA TODAS LAS UNIDADES
def obtener_productos_almacen(almacenId, sku):
    message = 'GET' + almacenId + sku
    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    url = '{}stock?almacenId={}&sku={}'.format(api_url_base, almacenId, sku)
    result = requests.get(url, headers=headers).json()
    return result

# ENTREGA UNA LISTA CON LA CANTIDAD DE ID'S QUE SE QUIERA Y QUE ESTEN EN UN ALMACEN ENTREGANDO UN SKU
def obtener_id_producto(sku, cantidad, almacenId):
    #lista de almacenes con el producto
    cantidad_id = 0
    lista_id_productos = []
    lista_productos = obtener_sku_con_stock(almacenId)
    for producto in lista_productos:
        if producto['_id'] == sku:
            lista_productos_almacen = obtener_productos_almacen(almacenId, sku)
            #print(lista_productos_almacen)
            for producto_unitario in lista_productos_almacen:
                lista_id_productos.append(producto_unitario['_id'])
                cantidad_id += 1
                if cantidad_id == cantidad:
                    return lista_id_productos
    # en caso de que la cantidad sea mayor que lo que se tiene, igual se entrega la lista con todos los existentes
    return lista_id_productos

def mover_entre_almacenes(sku, cantidad, almacenId_origen, almacenId_destino):
    lista_id = obtener_id_producto(sku, cantidad, almacenId_origen)
    for productoId in lista_id:
        message = 'POST' + productoId + almacenId_destino
        url = '{}moveStock'.format(api_url_base)
        headers_ = {'Content-Type': 'application/json',
                    'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
        body = {"productoId": productoId, "almacenId": almacenId_destino}

        requests.post(url, headers=headers_, data=json.dumps(body))

def mover_entre_bodegas(sku, cantidad, almacenId_destino, precio=0, oc=''):
    lista_id = obtener_id_producto(sku, cantidad, almacen_id_dict["despacho"])
    for productoId in lista_id:
        message = 'POST' + productoId + almacenId_destino
        url = '{}moveStockBodega'.format(api_url_base)
        headers_ = {'Content-Type': 'application/json',
                    'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
        body = {"productoId": productoId, "almacenId": almacenId_destino}
        respuesta = requests.post(url, headers=headers_, data=json.dumps(body))
        return respuesta

# ENTREGA LA CANTIDAD DE UNIDADES QUE SE TIENEN DE UN SKU
def cantidad_producto(sku):
    cantidad = 0
    for almacen in almacen_id_dict:
        lista_productos = obtener_sku_con_stock(almacen_id_dict[almacen])
        for producto in lista_productos:
            if producto['_id'] == sku:
                cantidad += producto['total']
                break
    return cantidad
#pedir_productos_sku('1001', 1)


# MUEVE LOS PRODUCTOS DE LA RECEPCION AL ALMACEN 1 O ALMACEN 2
def liberar_recepcion():
    #funcion que deja recepcion vacia, se mandan productos a almcanen1 o almacen2
    datos_bodegas = revisarBodega().json()
    #espacio en recepcion
    espacio_usado = datos_bodegas[0]['usedSpace']
    if espacio_usado == 0:
        #recepcion ya esta vacia
        return
    else:
        lista_recepcion = obtener_sku_con_stock(almacen_id_dict["recepcion"])
        for producto in lista_recepcion:
            #se actualizan datos de bodega
            datos_bodegas = revisarBodega().json()
            #revisa si cabe en almacen1
            if producto['total'] <= datos_bodegas[2]['totalSpace'] - datos_bodegas[2]['usedSpace']:
                #traspasa todos esos productos a almacen1
                mover_entre_almacenes(producto['_id'], producto['total'], almacen_id_dict["recepcion"], almacen_id_dict["almacen_1"])
            #revisa si cabe en almacen2
            elif producto['total'] <= datos_bodegas[3]['totalSpace'] - datos_bodegas[3]['usedSpace']:
                #traspasa todos esos productos a almacen2
                mover_entre_almacenes(producto['_id'], producto['total'], almacen_id_dict["recepcion"], almacen_id_dict["almacen_2"])
    return



# MUEVE LA CANTIDAD QUE SE QUIERA DE UN SKU HACIA EL ALMACEN DE DESPACHO
def despachar_producto(sku, cantidad):
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
                mover_entre_almacenes(sku, cantidad_despachar, almacen_id_dict["pulmon"], almacen_id_dict["despacho"])
                return
            elif producto['total'] < cantidad_despachar:
                # no se tiene la cantidad que se necesita, se manda lo que se tiene
                mover_entre_almacenes(sku, producto['total'], almacen_id_dict["pulmon"], almacen_id_dict["despacho"])
                cantidad_despachar -= producto['total']
            break
    #revisa si producto esta en almacen1
    lista_almacen1 = obtener_sku_con_stock(almacen_id_dict["almacen_1"])
    for producto in lista_almacen1:
        if producto['_id'] == sku:
            if producto['total'] >= cantidad_despachar:
                #se tiene la cantidad que se necesita
                mover_entre_almacenes(sku, cantidad_despachar, almacen_id_dict["almacen_1"], almacen_id_dict["despacho"])
                return
            elif producto['total'] < cantidad_despachar:
                #no se tiene la cantidad que se necesita, se manda lo que se tiene
                mover_entre_almacenes(sku, producto['total'], almacen_id_dict["almacen_1"], almacen_id_dict["despacho"])
                cantidad_despachar -= producto['total']
            break
    #revisa si producto esta en almacen2
    lista_almacen2 = obtener_sku_con_stock(almacen_id_dict["almacen_2"])
    for producto in lista_almacen2:
        if producto['_id'] == sku:
            if producto['total'] >= cantidad_despachar:
                # se tiene la cantidad que se necesita
                mover_entre_almacenes(sku, cantidad_despachar, almacen_id_dict["almacen_2"], almacen_id_dict["despacho"])
                return
            elif producto['total'] < cantidad_despachar:
                # no se tiene la cantidad que se necesita, se manda lo que se tiene
                mover_entre_almacenes(sku, producto['total'], almacen_id_dict["almacen_2"], almacen_id_dict["despacho"])
                cantidad_despachar -= producto['total']
            break
    return


#######FUNCION PARA EL STOCK MINIMO CUANTO TENGO QUE PEDIR DE CADA ELEMENTO
def devolver_cantidad(stock_actual, sku1):
    for elemento in stock_actual:
        if elemento["sku"] == sku1:
            return elemento["total"]
    return 0


def calcular_stock_unidades(stock_actual, diccionario):
    dict_compras_cantidad = dict()
    #print("\t2.1.1")
    for sku in diccionario:
        #print("\t2.1.2")
        element = diccionario[sku]
        if element['stock_minimo'] is not None:
            cantidad_actual = devolver_cantidad(stock_actual, sku)#funcion_que retorna int(element.sku)
            if cantidad_actual < element['stock_minimo']:
                #print("what")
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
                #print(dict_producto[str(sku)]['nombre'], sku, dict_producto[str(sku)]['receta'])
                for element in dict_producto[str(sku)]['receta']:
                    cantidad_element = dict_producto[str(sku)]['receta'][element] * cantidad / dict_producto[str(sku)]['lote']
                    dict_aux[element] = cantidad_element
                    #time.sleep(1)

                    dict_compra_final.update(calcular_cantidad_comprar(dict_producto, dict_aux, dict_compra_final))

    #time.sleep(2)
    #print("RETORNANDO", dict_compra_final)
    return dict_compra_final


# LLAMA A calcular_cantidad_comprar RESTANDO LAS MATERIAS PRIMAS DEL INVENTARIO
def generar_dict_compras():
    datos_productos = productos()
    stock_actual = stock()
    #print("\t2.1")
    calcular_stock_unidades_ = calcular_stock_unidades(stock_actual, datos_productos)
    #print("\t2.2")
    dict_compra_final = calcular_cantidad_comprar(datos_productos, calcular_stock_unidades_)

    for materias_primas in stock_actual:
        sku = materias_primas['sku']
        if sku in dict_compra_final:
            if dict_compra_final[sku] < materias_primas['total']:
                del dict_compra_final[sku]
            else:
                dict_compra_final[sku] -= materias_primas['total']

    return dict_compra_final

########
# BUSCA INVENTARIO DE UN GRUPO
def get_inventories_grupox(grupo, url_changed=False):
    if not url_changed:
        url = 'http://tuerca' + str(grupo) + '.ing.puc.cl/inventories'
    else:
        url = 'http://tuerca' + str(grupo) + '.ing.puc.cl/inventories/'

    headers_ = {'Content-Type': 'application/json', 'group': '2'}
    try:
        result = requests.get(url, headers=headers_)
        return result.json()
    except:
        return list()

def cantidad_sku_grupox(grupo, sku):
    inventario = get_inventories_grupox(grupo, url_changed=False)
    for elem in inventario:
        if elem['sku'] == sku:
            return elem["total"]
    return 0

def post_orders_grupox(grupo, oc_id, cantidad, sku, url_changed=False):
    if not url_changed:
        url = 'http://tuerca' + str(grupo) + '.ing.puc.cl/orders'
    else:
        url = 'http://tuerca' + str(grupo) + '.ing.puc.cl/orders/'
    headers_ = {'Content-Type': 'application/json', 'group': '2'}
    body = {'sku': sku, 'cantidad': cantidad, 'almacenId': almacen_id_dict['recepcion'], 'oc': oc_id}
    result = requests.post(url, headers=headers_, data=json.dumps(body))
    return result

# PIDE MATERIAS PRIMAS QUE NO PRODUZCA NUESTRO GRUPO
# SE LE ENTREGA UN SKU Y UNA CANTDIAD
"""SE DEBE PEDIR CON OC"""
def pedir_productos_sku(sku, cantidad, url_changed=False):
    datos = productos()
    productores = datos[sku]["productores"]
    total_pedido = 0
    if datos[sku]["propio"] != True:
        for grupo in productores:
            try:
                result = get_inventories_grupox(grupo)
                if result.status_code == 200 or result.status_code == 201:
                    if not url_changed:
                        result_2 = post_orders_grupox(grupo, cantidad, sku)
                    else:
                        result_2 = post_orders_grupox(grupo, cantidad, sku, url_changed=True)
                        #print("Le estamos pidiendo", str(cantidad), "al grupo", str(grupo), "STA_COD: " , result_2.status_code)
                else:
                    pass
            except:
                pass
    else:
        cantidad = datos[sku]['lote'] * math.ceil(cantidad/datos[sku]['lote'])
        #print(fabricarSinPago(sku, cantidad))


# FABRICA PRODUCTOS PROCESADOS EN CASO DE NO CUMPLIR STOCK
# REVISA QUE SE TENGAN MATERIAS PRIMAS PARA FABRICAR
def enviar_fabricar():
    productos_ = productos()
    stock2 = stock()
    for element in sku_stock_dict: # recorro elementos con stock minimo
        quantity = devolver_cantidad(stock2, element) # calculo cantidad del elemento en inventario
        #print(element,quantity)
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
                        despachar_producto(str(sku), productos_[element]["receta"][sku])
                    fabricarSinPago(element,lote)

                else:
                    break

        else:
            pass
    else:
        pass


def vaciar_almacen_despacho(todos_productos):
    for prod in todos_productos:
        productos_prod_en_almacen = obtener_productos_almacen(almacen_id_dict["despacho"], prod)
        for elemento in productos_prod_en_almacen:
            productoId = elemento["_id"]
            message = "DELETE"+productoId+"direc"+"20"+"4af9f23d8ead0e1d32000900"
            url = '{}stock'.format(api_url_base)
            headers_ = {'Content-Type': 'application/json',
                        'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
            body = {"productoId": productoId, "oc": "4af9f23d8ead0e1d32000900", "direccion": "direc", "precio": 20}
            result = requests.delete(url, headers=headers_, data=json.dumps(body))
            print(result)

###############################
#### ENTREGA 2 - PEDIDOS ######
###############################

# Esta función crea un pedido a un grupo con su respectiva orden de compra y
# pone la orden en "pedidos_nuestros" para que se mantenga al tanto
def pedir_prod_grupox(sku, cantidad, grupo, pedidos_nuestros):
    json_crear_oc = crear_oc(grupo_proveedor=grupo, sku=sku, cantidad=cantidad, preciounitario=1, canal = 'b2b')
    oc_id = json_crear_oc["_id"]
    response = post_orders_grupox(grupo = grupo, oc_id=oc_id, cantidad=cantidad, sku=sku, url_changed=False)
    #TENEMOS QUE PREOCUPARNOS DE LA RESPONSE????
    pedidos_nuestros.append({"sku": sku, "oc": oc_id, "cantidad": cantidad, "grupo": grupo, "fecha_pedido": int(time.time()*1000+10*60*1000)})
    return

# Pedir producto ENTREGA 2
# Cuando queremos pedir un producto ejecutamos esta función. Luego celery se
# encargará en "pedidos_nuestros_celery_control" en caso de que no nos respondan
# si hay un rechazo se encarga el metodo de "view.py"
def iniciar_orden(sku, cantidad, pedidos_nuestros):
    print("SE INICIA PEDIDO")
    datos = productos()
    productores = datos[sku]["productores"]

    cantidad
    for grupo in productores:
        c_disponible = cantidad_sku_grupox(grupo, sku)
        print("grupo: "+str(grupo)+" C_disponible: "+str(c_disponible))
        if c_disponible > 0 and grupo != 2:
            if cantidad <= c_disponible:
                pedir_prod_grupox(sku, cantidad, grupo, pedidos_nuestros)
                print("-pedido completado")
                print(pedidos_nuestros)
                break
            else:
                pedir_prod_grupox(sku, c_disponible, grupo, pedidos_nuestros)
                cantidad -= c_disponible
                print("-falta aún")
                print(pedidos_nuestros)

iniciar_orden("1007", 10, pedidos_nuestros)

# Este metodo toma un pedido cuyo tiempo de respuesta expiró y busca otros proveedores para esa cantidad de elementos
# FALTA que vuelva a poner la orden para los grupos 1 en adelante una vez que ya intentó pedirselo a todos
def pedir_siguiente_proveedor(i_pedido, pedidos_nuestros):
    productores = datos[pedidos_nuestros[i_pedido]["sku"]]["productores"] # busco los productores del sku
    i_productor = productores.index(pedidos_nuestros[i_pedido]["grupo"])
    sku = pedidos_nuestros[i_pedido]["sku"]
    cantidad = pedidos_nuestros[i_pedido]["cantidad"]
    while i_productor < len(productores)-1:
        i_productor += 1
        grupo = productores[i_productor]
        c_disponible = cantidad_sku_grupox(grupo, sku)
        if c_disponible > 0 and grupo != 2:
            if cantidad <= c_disponible:
                pedir_prod_grupox(sku, cantidad, grupo, pedidos_nuestros)
                break # ya habremos pedido todo lo necesario
            else:
                pedir_prod_grupox(sku, c_disponible, grupo, pedidos_nuestros)
                cantidad -= c_disponible
    return

# este metodo debe estar corriendo constantemente revisando si es que hay algún
# grupo que no nos haya respondido.
def pedidos_nuestros_celery_control(pedidos_nuestros):
    datos = productos()
    i_to_delete = list() # en esta lista se agregan los indices a eliminar de la lista
    for i_pedido in range(0, len(pedidos_nuestros)):
        if int(time.time()*1000) > pedidos_nuestros[i_pedido]["fecha_pedido"]:
            i_to_delete.append(i_pedido) # agrego a la lista el indice del elemento a eliminar
            pedir_siguiente_proveedor(i_pedido, pedidos_nuestros)
    #elimino los elementos seleccionados anteriormente
    i_to_delete.reverse()
    for i in i_to_delete:
        del pedidos_nuestros[i]

###################################################
###################################################

"""
def pedir_stock_minimo_grupos():
    datos = productos()
    pedir = generar_dict_compras()
    liberar_recepcion()
    for sku, cantidad in pedir.items():
        print(datos[sku]['nombre'], sku)
        pedir_productos_sku(sku, 3)
        liberar_recepcion()
        enviar_fabricar()
        print(" ")
"""
"""
pedir_stock_minimo_grupos()

enviar_fabricar()
liberar_recepcion()

#####PALTA
for i in range(34):
    pedir_productos_sku('1010', 1)
liberar_recepcion()
for i in range(50):
    pedir_productos_sku('1012', 1)



i = 0
while i < 15:
    mover_entre_almacenes("1003",86,almacen_id_dict["almacen_1"],almacen_id_dict["despacho"])
    vaciar_almacen_despacho(['1003'])
    i += 1

"""
