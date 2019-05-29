import pysftp
from xml.dom import minidom
from funciones_internas import  stock , cantidad_producto , cocinar_prod_sku, completar_oc
from requests_files import rechazar_oc , obtener_oc , recepcionar_oc
from time import *


#myHostname = "fierro.ing.puc.cl"
#myUsername = "grupo2_dev"
#myPassword = "jefPFs1p7mSt8rx"

myHostname = "fierro.ing.puc.cl"
myUsername = "grupo2"
myPassword = "Cs8WSk2RgpQGUTNJ2"

#funcion que va verificando si hay nuevas ordenes.
def ver_buzon():
	cnopts = pysftp.CnOpts()
	cnopts.hostkeys = None    # disable host key checking.
	lista_ids = []
	#que pasa si el archivo no esta creado.
	with open ("id_estados.txt",mode = "r") as file:
		for linea in file:
			nueva = linea.replace("\n","")
			lista_ids.append(nueva)
	with pysftp.Connection(myHostname, username=myUsername ,password=myPassword,cnopts=cnopts) as sftp : 
		sftp.cwd('/pedidos')
		structure = sftp.listdir_attr()
		for element in structure:
			archivo = sftp.open(element.filename,mode = "r")
			my_doc = minidom.parse(archivo)
			id_ = my_doc.getElementsByTagName('id')
			if id_[0].firstChild.data in lista_ids:
				pass
			else:
				logica_oc(id_[0].firstChild.data)
			
			#archivo = sftp.open(element,mode = "r")
			#my_doc = minidom.parse(archivo)
			#id_ = my_doc.getElementsByTagName('id')
			#sku_ = my_doc.getElementsByTagName('sku')
			#qty_ = my_doc.getElementsByTagName("qty")
			#orden = obtener_oc(id_[0].firstChild.data)

		
		

def logica_oc(id_compra):
	orden = obtener_oc(id_compra).json()
	sku = orden[0]["sku"]
	qty = orden[0]["cantidad"]
	fecha = orden[0]["fechaEntrega"]
	if not tiempo_real(fecha):
		rechazar_oc(id_compra,"fecha")
		escribir_txt_gen(id_compra)
	elif cocinar_prod_sku(sku,qty): #verificar por que si no funcionar retorna false bien , pero si no retorna solo el mandar a fabricar nunca un true
		recepcionar_oc(id_compra)
		escribir_txt_acep(id_compra,sku,qty)
		escribir_txt_gen(id_compra)
	else:
		rechazar_oc(id_compra,"falta producto")
		escribir_txt_gen(id_compra)

#ingredientes

def escribir_txt_gen(id_):
	with open ("id_estados.txt",mode = "a") as file:
		file.write(id_ +"\n")

def escribir_txt_acep(id_compra,sku,qty):
	with open("id_aceptados.txt",mode = "a") as file:
		file.write(id_compra+","+sku+","+qty+  "\n")

def verficar():
	lista_id = []
	with open("id_aceptados.txt",mode = "r") as file:
		for linea in file:
			nueva_linea = linea.replace("\n","")
			nueva_lista = nueva_linea.split(",")
			lista_id.append(nueva_lista)
	if lista_id != []:
		for orden in lista_id:
			if orden[2] <= cantidad_producto(orden[1]):
				index = lista_id.index(orden)
				lista_id.pop(index)
				completar_oc(orden[0])
			else:
				pass
		with open("id_aceptados.txt",mode = "w") as file:
			for ordenes_espera in lista_id:
				string = ordenes_espera.join(",")
				file.write(string +"\n")

def convertir_time(time):
    datetime_obj = strptime("{}".format(time), '%Y-%m-%dT%H:%M:%S.%fZ')
    return int(mktime(datetime_obj) * 1000)

def tiempo_real(hora):
	if convertir_time(hora) > int(time()*1000+10*60*10000):
		return True
	else:
		return False
