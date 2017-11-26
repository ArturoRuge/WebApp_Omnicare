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

class FormularioRegistro(Form):
	username = StringField("username",
		[
		validators.Required("Digita un usuario")
		])
	password1 = PasswordField("password", 
		[
		validators.Required("Digita una contrasena"),
		validators.Length(min=5, max=15, message="La contasena sebe tener min 5 y maximo 15 caracteres")
		])
	password2 = PasswordField("repeat password")

class newPassForm(Form):
	password1 = PasswordField("New password", 
		[
		validators.Required("Digita una contrasena"),
		validators.Length(min=5, max=15, message="La contasena sebe tener min 5 y maximo 15 caracteres")
		])
	password2 = PasswordField("repeat password")


	