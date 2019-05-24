import pysftp

myHostname = "fierro.ing.puc.cl"
myUsername = "grupo2_dev"
myPassword = "jefPFs1p7mSt8rx"


with pysftp.Connection(host = myHostname, username=myUsername, password=myPassword) as sftp:
	pass