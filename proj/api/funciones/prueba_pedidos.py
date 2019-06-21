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

id_grupos = {1: "5cbd31b7c445af0004739be3", 2: "5cbd31b7c445af0004739be4", 3: "5cbd31b7c445af0004739be5",
             4: "5cbd31b7c445af0004739be6", 5: "5cbd31b7c445af0004739be7", 6: "5cbd31b7c445af0004739be8",
             7: "5cbd31b7c445af0004739be9", 8: "5cbd31b7c445af0004739bea", 9: "5cbd31b7c445af0004739beb",
             10: "5cbd31b7c445af0004739bec", 11: "5cbd31b7c445af0004739bed", 12: "5cbd31b7c445af0004739bee",
             13: "5cbd31b7c445af0004739bef", 14: "5cbd31b7c445af0004739bf0"}

mins_espera_pedido = 240


def sign_request(string):

    key = str.encode(api_key)
    raw = str.encode(string) # as specified by OAuth
    hashed = hmac.new(key, raw, digestmod=sha1)
    hashed_bytes = hashed.digest()
    encoded = base64.b64encode(hashed_bytes)
    encoded = str(encoded, 'UTF-8')
    return encoded

def obtener_oc(id_oc):
    message = 'GET'
    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    url = '{}obtener/{}'.format(api_oc_url_base, id_oc)
    result = requests.get(url, headers=headers)
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

print(crear_oc(3, '1006', 1, 1, 'b2b').json())
print(obtener_oc('5d0d03e46b154b00041b762a').json())