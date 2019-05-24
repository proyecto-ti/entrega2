import pysftp
from xml.dom import minidom
from funciones_bodega import obtener_oc



	

myHostname = "fierro.ing.puc.cl"
myUsername = "grupo2_dev"
myPassword = "jefPFs1p7mSt8rx"

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None    # disable host key checking.
lista_aux = []
with pysftp.Connection(myHostname, username=myUsername ,password=myPassword,cnopts=cnopts) as sftp : 
	sftp.cwd('/pedidos')
	structure = sftp.listdir_attr()
	for element in structure:
		lista_aux.append(element.filename)
	for element in lista_aux:
		a = sftp.open(element,mode = "r")
		my_doc = minidom.parse(a)
		id_ = my_doc.getElementsByTagName('id')
		print(id_[0].firstChild.data)
		sku_ = my_doc.getElementsByTagName('sku')
		qty_ = my_doc.getElementsByTagName("qty")
		print(obtener_oc(id_[0].firstChild.data))
		
		



	
