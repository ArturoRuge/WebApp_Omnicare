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
import functions

app = Flask(__name__)
app.secret_key = "my_secret-key"
Csrf = CSRFProtect(app)

@app.errorhandler(404)
def notFound(e):
	title = "Error 404 - Pagina no encontrada"
	return render_template("404.html", title = title), 404

@app.route("/", methods=["GET", "POST"])
def index():
	login = False
	login_form = forms.LoginForm(request.form)
	if request.method == "POST":
		user = login_form.username.data
		password = login_form.password.data
		userLog = functions.is_user(user, password)
		if userLog:
			login= True
			functions.messageLogin(userLog, user)
			return redirect(url_for("ventas"))
		
		
	title = "Pagina de inicio"
	return render_template("index.html", title = title, form = login_form, login = login)


@app.route("/registro", methods = ["GET", "POST"])
def registro():
	session = functions.userInSession()
	if session: 
		login = functions.messageUserSession(session)

	formulario_registro = forms.FormularioRegistro(request.form)
	if request.method == "POST" and formulario_registro.validate():
		user = formulario_registro.username.data
		password1 = formulario_registro.password1.data
		password2 = formulario_registro.password2.data

		functions.newUser(user, password1, password2)

	title = "Registrate completando este formulario"
	return render_template("registro.html", title=title, form=formulario_registro)



@app.route("/logout")
def logout():
	if "username" in session:
		session.pop("username")
		closeMessage = "Has cerrado sesion correctamente"
		flash(closeMessage)
	return redirect(url_for("index"))


@app.route("/cambiarpass", methods=["GET", "POST"])
def cambiarPass():
	session = functions.userInSession()
	if session:
		login = functions.messageUserSession(session)
		newpass_form = forms.newPassForm(request.form)
		if request.method == "POST":
			user = str(session)
			password1 = newpass_form.password1.data
			password2 = newpass_form.password2.data
			functions.newPass(user, password1, password2)

		title = "Cambia tu password"
		return render_template("cambiarpass.html", title = title, form = newpass_form, login=login)
	else:
		return redirect(url_for("index"))


@app.route("/ventas")
def ventas(client=None):
	session = functions.userInSession()
	if session: 
		login = functions.messageUserSession(session)

		dataSales = functions.readSales()
		countSales = len(dataSales)

		pathcsv = functions.generatecsv(dataSales)

		title = "Consulta las ventas del mes"
		return render_template("ventas.html", title=title, dataSales = dataSales, countSales = countSales , login = login, pathcsv = pathcsv)
	else:
		return redirect(url_for("index"))


@app.route("/productosporcliente")
@app.route("/productosporcliente", methods=["GET", "POST"])
@app.route("/productosporcliente/<client>", methods=["GET", "POST"])
def productosPorClientes(client=None):
	clientSearch = None
	positionClient = None
	listClients = None
	pathcsv = None
	dataSalesClient = None
	session = functions.userInSession()
	if session:
		login = functions.messageUserSession(session)

		dataSales = functions.readSales()
		client_form = forms.ClientsForm(request.form)

		if request.method == "POST" and client_form.validate():
			clientSearchOriginal = client_form.client.data
			clientSearch = clientSearchOriginal.upper()
			positionClient = functions.positionData("CLIENTE")
			listClients = functions.searchData(clientSearch, dataSales, positionClient)
			if len(listClients) == 0:
				listClients = None

		if client:	
			dataSalesClient = functions.dataResultSerch(dataSales, client)
			pathcsv = functions.generatecsv(dataSalesClient)

		title = "Consulta las compras realizadas por cliente"
		return render_template("productos_por_cliente.html", client = client, form = client_form, title=title, login = login, dataSalesClient = dataSalesClient, option = clientSearch, listClients = listClients, pathcsv = pathcsv)
	else:
		return redirect(url_for("index"))


@app.route("/clientesporproducto", methods=["GET", "POST"])
@app.route("/clientesporproducto/<product>", methods=["GET", "POST"])
def clientesPorProducto(product=None):
	productSearch = None
	positionProduct = None
	listProducts = None
	pathcsv = None
	dataSalesProduct = None
	session = functions.userInSession()
	if session:
		login = functions.messageUserSession(session)

		dataSales = functions.readSales()
		product_form = forms.ProductForm(request.form)

		if request.method == "POST" and product_form.validate():
			productSearchOriginal = product_form.product.data
			productSearch = productSearchOriginal.upper()
			positionProduct = functions.positionData("PRODUCTO")
			listProducts = functions.searchData(productSearch, dataSales, positionProduct)
			if len(listProducts) == 0:
				listProducts = None

		if product:	
			dataSalesProduct = functions.dataResultSerch(dataSales, product)
			pathcsv = functions.generatecsv(dataSalesProduct)
			
		title = "Consulta los clientes que compraron un producto"
		return render_template("clientes_por_producto.html", product = product, form = product_form, title=title, login = login, dataSalesProduct = dataSalesProduct, option = productSearch, listProducts = listProducts, pathcsv=pathcsv)
	else:
		return redirect(url_for("index"))

@app.route("/productosmasvendidos", methods = ["GET", "POST"])
def productosMasVendidos():
	dataSalesProduct = None
	session = functions.userInSession()
	if session:
		login = functions.messageUserSession(session)
		numberItems = None
		
		numberForm = forms.numberForm(request.form)
		if request.method == "POST" and numberForm.validate():
			numberItems = int(numberForm.numberItems.data)

			dataSales = functions.readSales()
			positionProduct = functions.positionData("PRODUCTO")
			positionAmount = functions.positionData("CANTIDAD")
			positionCode = functions.positionData("CODIGO")
			topProducts = functions.orderProducts(dataSales, positionProduct, positionAmount, positionCode)

			dataSalesProduct = functions.dataResult(topProducts, numberItems)
			pathcsv = functions.generatecsv(dataSalesProduct)

		title= "Los productos mas vendidos este mes"
		return render_template("productosmasvendidos.html", title = title, login = login, dataSalesProduct = dataSalesProduct, numberItems = numberItems, form = numberForm)
	else:
		return redirect(url_for("index"))

@app.route("/clientesmascompradores", methods = ["GET", "POST"])
def clientesmascompradores():
	topClients = None
	dataSalesClients = None
	session = functions.userInSession()
	if session:
		login = functions.messageUserSession(session)
		numberItems = None

		numberForm = forms.numberForm(request.form)
		if request.method == "POST" and numberForm.validate():
			if numberForm.numberItems.data:
				numberItems = int(numberForm.numberItems.data)

			dataSales = functions.readSales()
			positionClient = functions.positionData("CLIENTE")
			positionPrice = functions.positionData("PRECIO")
			topClients = functions.orderClients(dataSales, positionClient, positionPrice)

			dataSalesClients = functions.dataResult(topClients, numberItems)
			pathcsv = functions.generatecsv(dataSalesClients)



		title= "Clientes mas compradores de este mes"
		return render_template("clientesmascompradores.html", title = title, login = login, dataSalesClients = dataSalesClients, numberItems = numberItems, form = numberForm)
	else:
		return redirect(url_for("index"))




if __name__ == "__main__":
	app.run()