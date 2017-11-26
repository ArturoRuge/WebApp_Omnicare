from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask_wtf import CSRFProtect
from flask import session
from flask import redirect
from flask import url_for

import time
import forms
import csv

def is_user(user, password):
	"""
	input: user- dato ingresado en la casilla de usuario
			password- dato ingresado en la casilla de password
	output: valida si el usuario y password existen en
			el archivo usuarios.csv
	"""
	listUsers = []
	with open("usuarios.csv") as archive:
		listData = csv.reader(archive)
		for listUsers in listData:
			for data in listUsers:
				if data == user and listUsers[1] == password:
					return True
	return False

def messageLogin(userLog, user):
	"""
	input: userLog- valida si los datos ingresados en las casillas
					de login existen en el archivo usuarios.csv
			user- dato de la casilla de usuario
	output: Mensaje de bienvenida o error 
	"""
	if userLog:
			session["username"] = user
			welcomeMessage = "Bienvenido {}".format(user)
			flash(welcomeMessage)
	else:
		errorMessage = "El usuario no existe"
		flash(errorMessage)

def readSales():
	"""
	output: lista de los datos que se encuentra en sales.csv 
	"""
	CANTIDAD_CAMPOS = 5
	dataSales = []
	try: 
		with open("sales.csv") as archive:
			list = csv.reader(archive)
			data = next(list, None)
			while data:
				dataSales.append(data)
				data = next(list,None)
		for line in dataSales:
			if len(line) != CANTIDAD_CAMPOS:
				dataSales = [["EL ARCHIVO CSV NO TIENE TODOS LOS CAMPOS"]]
				break
	except:
		dataSales.append(["EL ARCHIVO CSV NO EXISTE"])
	return dataSales

def dataResultSerch(dataSales, client):
	"""
	input: dataSales- Lista de datos de sales.csv
			client- cliente que busca el usuario
	output: lista datos cliente seleccionado por el usuario
	"""
	dataSalesClient = []
	cont = 0
	for list in dataSales:
		if cont == 0:
			dataSalesClient.append(list)
			cont += 1
		if client in list:
			dataSalesClient.append(list)
	return dataSalesClient

def dataResult(topProducts, numberItems):
	dataSalesItems = []
	cont = 0
	for list in topProducts:
		if cont == 0:
			dataSalesItems.append(list)
		if 0 < cont <= numberItems:
			dataSalesItems.append(list)
		cont += 1
	return dataSalesItems



def userInSession():
	"""
	output: valida si el usuario esta logueado
	"""
	if "username" in session:
		username = session["username"]
		return username
	else: 
		return False

def positionData(title):
	"""
	input: title- dato que se va a buscar en archivo sales.csv
	output: posicion de title en el archivo sales.csv 
	"""
	data = readSales()
	position = data[0].index(title)
	return position

def searchData(client, dataSales, positionClient):
	"""
	input: client- dato ingresado en la casilla de busqueda de cliente
			datasales- lista de datos del archivo sales.csv
			positionClient- posicion de los datos a buscar
	output: lista de clientes que se encuentrasn en sales.csv 
	"""
	listClients = []
	for list in dataSales[1:]:
		if client in list[positionClient] and list[positionClient] not in listClients:
			listClients.append(list[positionClient])
	return listClients


def orderProducts(dataSales, positionProduct, positionAmount, positionCode):
	listTotalProducts = sumAmountProducts(dataSales, positionProduct, positionAmount, positionCode);
	listAmount = []
	finalListAmount = [["CODIGO","PRODUCTO","CANTIDAD"]]

	for list in listTotalProducts:
		if list[2] not in listAmount:
			amount = list[2]
			listAmount.append(amount)
	
	temp = False

	while temp == False:
		temp = True;
		for i in range(len(listAmount) - 1):
			if listAmount[i] < listAmount[i + 1]:
				aux = listAmount[i]
				listAmount[i] = listAmount[i + 1]
				listAmount[i + 1] = aux
				temp = False

	for amount in listAmount:
		for product in listTotalProducts:
			if product[2] == amount:
				finalListAmount.append(product)

	return finalListAmount



def sumAmountProducts(dataSales, positionProduct, positionAmount, positionCode):
	listTotalProducts = []
	listProducts = []
	listCodes = []
	counter = 0

	for list in dataSales[1:]:
		if list[positionProduct] not in listProducts:
			product = list[positionProduct]
			listProducts.append(product)
			code = list[positionCode]
			listCodes.append(code)

	for product in listProducts:
		sumProducts = 0
		for list in dataSales[1:]:
			if list[positionProduct] == product:
				sumProducts += float(list[positionAmount])
		newList = [listCodes[counter], product, sumProducts]
		listTotalProducts.append(newList)
		counter += 1

	return listTotalProducts


def orderClients(dataSales, positionClient, positionPrice):
	listTotalClients = []
	listClients = []

	for list in dataSales[1:]:
		if list[positionClient] not in listClients:
			listClients.append(list[positionClient])

	for client in listClients:
		sumPrice = 0
		for list in dataSales:
			if list[positionClient] == client:
				sumPrice += float(list[positionPrice])
		newList = [client, sumPrice]
		listTotalClients.append(newList)

	temp = False

	while temp == False:
		temp = True
		for i in range(len(listTotalClients)-1):
			if listTotalClients[i][1] < listTotalClients[i+1][1]:
				aux = listTotalClients[i]
				listTotalClients[i] = listTotalClients[i+1]
				listTotalClients[i+1] = aux
				temp = False
	finalListTotalClient = [["CLIENTE", "TOTAL COMPRAS"]] + listTotalClients
	return finalListTotalClient

def messageUserSession(session):
	if session:
		usuario_registrado = "Estas registrado como {}".format(session)
		flash(usuario_registrado)
		login = True
	else:
		login = False
	return login

def newUser(user, password1, password2):
	new_user = True
	new_pass = True
	with open("usuarios.csv") as archivo:
			datos = csv.reader(archivo)
			for linea in datos:
				for dato in linea:
					if dato == user:
						new_user = False
						reject_message = "Este nombre de usuario ya esta registrado, digita uno nuevo!"
						flash(reject_message)

	if password1 != password2:
		new_pass = False
		reject_message2 = "Las contrasenas no coinciden!"
		flash(reject_message2)

	if new_user and new_pass:
		mensaje = "\n" + user + "," + password1
		with open("usuarios.csv", "a") as archivo:
			writer = csv.writer(archivo)
			archivo.write(mensaje)

		welcome_message = "Gracias por registrate, ya puedes hacer Login!!"
		flash(welcome_message)
	
	print("Registro correcto")


def newPass(user, password1, password2):

	userList = []
	if password1 != password2:
		new_pass = False
		reject_message2 = "Las contrasenas no coinciden!"
		flash(reject_message2)
	else:
		with open("usuarios.csv") as archivo:
			for linea in archivo:
				columnas = linea.split(",")
				if columnas[0]==user:
					columnas[1]=password1+"\n"
				userList.append(",".join(columnas))
				
		with open("usuarios.csv", "w") as archivo:
			archivo.writelines(userList)

		newpass_success = "Tu password ha sido modificado. Utilizalo en tu proxima sesion"
		flash(newpass_success)

def generatecsv(dataSales):
	"""
	input: dataSales- Contenido que se va a guardar en un nuevo csv
	output: url del archivo generado
	"""
	actualDate = time.strftime('%y%b%d_%H%M%S')
	pathcsv = "static/consultas/resultados_" + actualDate + ".csv"
	with open(pathcsv, "w") as archivo:
		writer = csv.writer(archivo)
		writer.writerows(dataSales)
	return pathcsv

