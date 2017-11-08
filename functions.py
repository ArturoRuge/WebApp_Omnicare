from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask_wtf import CSRFProtect
from flask import session
from flask import redirect
from flask import url_for

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