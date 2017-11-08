from wtforms import Form 
from wtforms import StringField, TextField
from wtforms import PasswordField
from wtforms import validators


class LoginForm(Form):
	username = StringField("Usuario",
		[
		validators.Required("Digita tu usuario")
		])
	password = PasswordField("Contrasena",
		[
		validators.Required("Escribe tu contrasena")
		])

class ClientsForm(Form):
	client = StringField("Cliente",
		[
		validators.Required("Digita el nombre de un cliente"),
		validators.Length(min=4, message="Ingresa al menos 4 caracteres")
		])

class ProductForm(Form):
	product = StringField("Producto",
		[
		validators.Required("Digita el nombre de un producto"),
		validators.Length(min=4, message="Ingresa al menos 4 caracteres")
		])

class numberForm(Form):
	numberItems = StringField("",
		[
		validators.Required("Digita la cantidad de items que quieres consultar")
		])


	