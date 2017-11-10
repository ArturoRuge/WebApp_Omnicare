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



@app.route("/logout")
def logout():
	if "username" in session:
		session.pop("username")
		closeMessage = "Has cerrado sesion correctamente"
		flash(closeMessage)
	return redirect(url_for("index"))


@app.route("/ventas")
def ventas():
	session = functions.userInSession()
	if session: 
		login = functions.messageUserSession(session)

		dataSales = functions.readSales()
		countSales = len(dataSales)

		title = "Consulta las ventas del mes"
		return render_template("ventas.html", title=title, dataSales = dataSales, countSales = countSales , login = login)
	else:
		return redirect(url_for("index"))


@app.route("/productosporcliente", methods=["GET", "POST"])
@app.route("/productosporcliente/<client>", methods=["GET", "POST"])
def productosPorClientes(client=None):
	clientSearch = None
	positionClient = None
	listClients = None
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
			
		title = "Consulta las compras realizadas por cliente"
		return render_template("productos_por_cliente.html", client = client, form = client_form, title=title, login = login, dataSales = dataSales, option = clientSearch, listClients = listClients)
	else:
		return redirect(url_for("index"))


@app.route("/clientesporproducto", methods=["GET", "POST"])
@app.route("/clientesporproducto/<product>", methods=["GET", "POST"])
def clientesPorProducto(product=None):
	productSearch = None
	positionProduct = None
	listProducts = None
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
			
		title = "Consulta los clientes que compraron un producto"
		return render_template("clientes_por_producto.html", product = product, form = product_form, title=title, login = login, dataSales = dataSales, option = productSearch, listProducts = listProducts)
	else:
		return redirect(url_for("index"))

@app.route("/productosmasvendidos", methods = ["GET", "POST"])
def productosMasVendidos():

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

		title= "Los productos mas vendidos este mes"
		return render_template("productosmasvendidos.html", title = title, login = login, topProducts = topProducts, numberItems = numberItems, form = numberForm)
	else:
		return redirect(url_for("index"))

@app.route("/clientesmascompradores", methods = ["GET", "POST"])
def clientesmascompradores():

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


		title= "Clientes mas compradores de este mes"
		return render_template("clientesmascompradores.html", title = title, login = login, topClients = topClients, numberItems = numberItems, form = numberForm)
	else:
		return redirect(url_for("index"))


if __name__ == "__main__":
	app.run()