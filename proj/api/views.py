from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from hashlib import sha1
import hmac
from .funciones_bodega import *
from .datos import *
import json
from django.shortcuts import render, render_to_response
from django.http.response import JsonResponse, HttpResponse

name_sku_dict = {"Sesamo": "1011",
                "Nori_Entero": "1016",
                "Camaron": "1006",
                "Azucar": "1003",
                "Arroz_Grano_Corto": "1001"}

almacen_dict_id = { "5cbd3ce444f67600049431b9" : "recepcion",
                     "5cbd3ce444f67600049431ba" : "despacho",
                     "5cbd3ce444f67600049431bb" : "almacen_1",
                     "5cbd3ce444f67600049431bc" : "almacen_2",
                     "5cbd3ce444f67600049431bd" : "pulmon",
                     "5cbd3ce444f67600049431be" : "cocina"}

sku_stock_dict = {  "1301" : 50, "1201" : 250, "1209" : 20, "1109" : 50,"1309" : 170,
                    "1106" : 400,"1114" : 50,"1215" : 20,"1115" : 30,"1105" : 50,
                    "1216" : 50,"1116" : 250,"1110" : 80,"1310" : 20,
                    "1210" : 150,"1112" : 130,"1108" : 10,"1407" : 40,"1207" : 20,
                    "1107" : 50,"1307" : 170,"1211" : 60}


def inventories_view(request):
    lista = stock()
    query = {"query": lista}
    return render_to_response('inventoriestotal.html', query)


def bodegas_view(request):
    lista = []
    for item in revisarBodega().json():
        dict = {"almacen": almacen_dict_id[item['_id']], "total" : item['totalSpace'], "used": item['usedSpace']}
        lista.append(dict)

    query = {"query": lista}
    return render_to_response('bodegas.html', query)


def estadisticas_view(request):
    datos = productos()
    lista_ = []
    lista = stock()
    for sku, information in datos.items():
        if information['stock_minimo'] is not None:
            dict = {"sku": sku, "stock_minimo": str(information['stock_minimo']), "name": information['nombre']}
            cantidad_actual = 0
            for items in lista:
                if items['sku'] == sku:
                    cantidad_actual += items["total"]

            dict["cantidad_actual"] = str(cantidad_actual)


            porcentaje = cantidad_actual * 100 / information['stock_minimo']
            dict["porcentaje"] = porcentaje
            lista_.append(dict)

    query = {"query": lista_}
    return render_to_response('index.html', query)


class InventoriesView(APIView):
    def get(self, request):
        #ESTA ES LA FUNCIÓN QUE HAY QUE MODIFICAR PARA LOS GET
        #SOLO SE MUESTRAN PRODUCTOS DE ALMACEN DESPACHO, ALMACENES GENERALES Y PULMON
        lista = stock_fixed()
        return JsonResponse(lista, status=200, safe=False)


# Cuando hagan post con POSTMAN hay que ponerle un / al final de la URL, así:
# http://127.0.0.1:8000/api/orders/
class OrdersView(APIView):
    def post(self, request):
        #ESTA ES LA FUNCION QUE HAY QUE MODIFICAR PARA LOS POST
        grupo = request.headers.get("group")
        sku = request.data.get("sku")
        cantidad = request.data.get("cantidad")
        almacenId = request.data.get("almacenId")
        oc = request.data.get("oc")

        if not sku or not cantidad or not almacenId or not oc:
            return Response(data="No se creó el pedido por un error del cliente en la solicitud", status=400)
        elif sku not in sku_producidos or int(cantidad) > int(cantidad_producto(sku)):
            ## SE MANDA A ENDPOINT DEL GRUPO QUE SE RECHAZA LA ENTREGA
            aviso_rechazar_pedido(oc, grupo)
            return Response(data="Producto no se encuentra o cantidad no disponible", status=404)
        else:
            ## SE MANDA A ENDPOINT DEL GRUPO QUE SE ACEPTA LA ENTREGA
            aviso_aceptar_pedido(oc, grupo)
            despachar_producto(sku, cantidad)
            mover_entre_bodegas(sku, cantidad, almacenId, oc)
            dictionary = {"sku": sku, "cantidad": cantidad, "almacenId": almacenId, "grupoProveedor": "2", "aceptado": True, "despachado": True}
            return JsonResponse(dictionary, status=201, safe=False)


class OCView(APIView):
    def post(self, request, oc_id):
        #FUNCION ENDOPOINT DE OC
        #SE LLAMA CUANDO PEDIMOS A OTRO GRUPO
        status = request.data.get("status")
        grupo_id = obtener_oc(oc_id)["proveedor"]
        # Se va a recibir el pedido
        if status == "accept":
            # Quitamos el track a la orden de compra en "pedidos nuestros"
            for index in range(0, len(ordenes_por_confirmar)):
                if ordenes_por_confirmar[index]["oc"] == oc_id:
                    ordenes_aceptadas.append(ordenes_por_confirmar[index])
                    del ordenes_por_confirmar[index]
                    break

            return HttpResponse(status=204)

        # El pedido fue rechazado
        elif status == "reject":
            for index in range(0, len(ordenes_por_confirmar)):
                if ordenes_por_confirmar[index]["oc"] == oc_id:
                    i_pedido = index
                    break
            pedir_siguiente_proveedor(i_pedido, ordenes_por_confirmar)
            del ordenes_por_confirmar[i_pedido]
            return HttpResponse(status=204)
