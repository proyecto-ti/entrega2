import requests
from hashlib import sha1
import hmac
import base64
import json
import math
import time

api_key = 'A#soL%kRvHX2qHm'
api_url_base = 'https://integracion-2019-dev.herokuapp.com/bodega/'
api_oc_url_base = 'https://integracion-2019-dev.herokuapp.com/oc/'

almacen_id_dict = {"recepcion" : "5cbd3ce444f67600049431b9",
                    "despacho" : "5cbd3ce444f67600049431ba",
                    "almacen_1" : "5cbd3ce444f67600049431bb",
                    "almacen_2" : "5cbd3ce444f67600049431bc",
                    "pulmon" : "5cbd3ce444f67600049431bd",
                    "cocina" : "5cbd3ce444f67600049431be"}

sku_stock_dict = {  "1101": 100, "1111": 100, "1301" : 50, "1201" : 250, "1209" : 20, "1109" : 50,"1309" : 170,
                    "1106": 400,"1114": 50,"1215" : 20,"1115" : 30,"1105" : 50,
                    "1216": 50,"1116": 250,"1110" : 80,"1310" : 20,
                    "1210": 150,"1112": 130,"1108" : 10,"1407" : 40,"1207" : 20,
                    "1107": 50,"1307": 170,"1211" : 60}

sku_producidos = ["1001", "1002", "1006", "1010", "1011", "1012", "1014", "1016"]

ordenes_por_confirmar = list()
ordenes_aceptadas = list()
mins_espera_pedido = 5

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

    key = str.encode(api_key)
    raw = str.encode(string) # as specified by OAuth
    hashed = hmac.new(key, raw, digestmod=sha1)
    hashed_bytes = hashed.digest()
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
    return result

def crear_oc(grupo_proveedor, sku, cantidad, preciounitario, canal):
    message = 'PUT'
    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    url = '{}crear'.format(api_oc_url_base)
    body = {"cliente": id_grupos[2], "proveedor": id_grupos[grupo_proveedor], "sku": sku, "fechaEntrega": int(time.time()*1000+mins_espera_pedido*60*1000),
            "cantidad": int(cantidad), "precioUnitario": preciounitario, "canal": canal, "urlNotificacion":
                "http://tuerca2.ing.puc.cl/oc/{_id}/notification/"}

    result = requests.put(url, headers=headers, data=json.dumps(body))
    return result

def obtener_oc(id_oc):
    message = 'GET'
    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    url = '{}obtener/{}'.format(api_oc_url_base, id_oc)
    result = requests.get(url, headers=headers)
    return result

def recepcionar_oc(id_oc):
    message = 'POST'
    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    url = '{}recepcionar/{}'.format(api_oc_url_base, id_oc)
    body = {"id": id_oc}
    result = requests.post(url, headers=headers, data=json.dumps(body))
    return result

def rechazar_oc(id_oc, motivo_rechazo):
    message = 'POST'
    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    url = '{}rechazar/{}'.format(api_oc_url_base, id_oc)
    body = {"id": id_oc, "rechazo": motivo_rechazo}
    result = requests.post(url, headers=headers, data=json.dumps(body))
    return result

def aviso_aceptar_pedido(oc, grupo):
    url = 'http://tuerca' + str(grupo) + '.ing.puc.cl/oc/{}/notification'.format(oc)
    headers = {'Content-Type': 'application/json'}
    body = {"status": "accept"}
    result = requests.post(url, headers=headers, data=json.dumps(body))
    return result

def aviso_rechazar_pedido(oc, grupo):
    url = 'http://tuerca' + str(grupo) + '.ing.puc.cl/oc/{}/notification'.format(oc)
    headers = {'Content-Type': 'application/json'}
    body = {"status": "reject"}
    result = requests.post(url, headers=headers, data=json.dumps(body))
    return result

#ENTREGA SKU DE PRODUCTOS CON STOCK EN UN ALMACEN Y SU CANTIDAD
def obtener_sku_con_stock(almacenId):
    message = 'GET' + almacenId
    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    url = '{}skusWithStock?almacenId={}'.format(api_url_base, almacenId)
    result = requests.get(url, headers=headers).json()
    return result

# ENTREGA EL TIPO DE ALMACEN, CAPACIDAD Y ESPACIO USADO
def revisarBodega():
    url = '{}almacenes/'.format(api_url_base)

    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request('GET'))}

    result = requests.get(url, headers=headers)
    return result

# FABRICA PRODUCTOS PROCESADOS SI SE TIENEN LAS MATERIAS PRIMAS NECESARIAS EN EL DESPACHO

def fabricarSinPago(sku, cantidad):
    message = 'PUT' + sku + str(cantidad)
    url = '{}fabrica/fabricarSinPago'.format(api_url_base)
    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    body = {"sku": sku, "cantidad": int(cantidad)}

    result = requests.put(url, headers=headers, data=json.dumps(body))
    return result.json()
#####################################

# PARA UN SKU DADO EN UN ALMACEN, ENTREGA TODAS LAS UNIDADES
def obtener_productos_almacen(almacenId, sku):
    message = 'GET' + almacenId + sku
    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    url = '{}stock?almacenId={}&sku={}'.format(api_url_base, almacenId, sku)
    result = requests.get(url, headers=headers).json()
    return result

def request_mover_entre_almacenes(sku, cantidad, almacenId_origen, almacenId_destino, productoId):
    message = 'POST' + productoId + almacenId_destino
    url = '{}moveStock'.format(api_url_base)
    headers_ = {'Content-Type': 'application/json',
                'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    body = {"productoId": productoId, "almacenId": almacenId_destino}

    result = requests.post(url, headers=headers_, data=json.dumps(body))

# ENTREGA UNA LISTA CON LA CANTIDAD DE ID'S QUE SE QUIERA Y QUE ESTEN EN UN ALMACEN ENTREGANDO UN SKU
def request_mover_entre_bodegas(sku, cantidad, almacenId_destino, oc, productoId, precio=1):
    message = 'POST' + productoId + almacenId_destino
    url = '{}moveStockBodega'.format(api_url_base)
    headers_ = {'Content-Type': 'application/json',
                'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    body = {"productoId": productoId, "almacenId": almacenId_destino, "oc": oc, "precio": precio}
    respuesta = requests.post(url, headers=headers_, data=json.dumps(body))

#función despachar de la documentación
def despachar_producto(sku, cantidad, almacenId_destino, oc, productoId, precio=1):
    message = 'DELETE' + productoId + almacenId_destino + precio + oc
    url = '{}stock'.format(api_url_base)
    headers_ = {'Content-Type': 'application/json',
                'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    body = {"productoId": productoId, "oc": oc, "direccion": almacenId_destino, "precio": precio}
    respuesta = requests.post(url, headers=headers_, data=json.dumps(body))


# BUSCA INVENTARIO DE UN GRUPO
def get_inventories_grupox(grupo, url_changed=False):
    if not url_changed:
        url = 'http://tuerca' + str(grupo) + '.ing.puc.cl/inventories'
    else:
        url = 'http://tuerca' + str(grupo) + '.ing.puc.cl/inventories/'

    headers_ = {'Content-Type': 'application/json', 'group': '2'}
    try:
        result = requests.get(url, headers=headers_)
        return result
    except:
        return list()

def post_orders_grupox(grupo, oc_id, cantidad, sku):
    url = 'http://tuerca' + str(grupo) + '.ing.puc.cl/orders'
    headers_ = {'Content-Type': 'application/json', 'group': '2'}
    body = {'sku': sku, 'cantidad': cantidad, 'almacenId': almacen_id_dict['recepcion'], 'oc': oc_id}
    result = requests.post(url, headers=headers_, data=json.dumps(body))
    return result

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
