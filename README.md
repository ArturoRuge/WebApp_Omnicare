TP OMNICARE

Detalles de la aplicación

El desarrollo de Omnicare consiste en una simulaci{on de aplicación web que le permite al usuario poder iniciar sesión y realizar diferentes consultas a una base de datos compuesta por un archivo csv.

- El flujo del programa empieza en el archivo main.py, donde estan definidas las diferentes app.route de la aplicación, donde cada una:
 1- Devuelve su respectivo archivo html dependiendo del requerimiento del usuario 2- Si es necesario, muestra un formulario, el cual esta alojado en el archivo form.py. 
 3- Valida si existen cookies y hace consultas a archivos .csv, a través de llamadas a funciones que estan creadas en el archivo functions.py 
 4- Hacen el llamado de archivos de imágenes y css que están alojados en la carpeta static.

 - La estructura que se utiliza para representar la información son en primer lugar, archivos .py que se encargan de gestionar las consultas del usuario, los datos que se envian al navegador su estructuran en archivos .html y el resultado de las consultas a los archivos csv que realiza el usuario se estructuran en tablas, creadas dinamicamente con html.


- El usuario ingresa a la aplicación a traves de la página index.html, donde el usuario debe digitar sus credenciales de usuario y contraseña, las cuales se van a validar con los datos que están alojados en el archivo usuarios.csv, si la combinación es correcta, el usuario será redirigido a la página ventas.html, donde podrá ver las últimas 10 ventas del mes, además, aparecerán más opciones en el menú de navegación, como lo son: Productos por cliente, Clientes por producto, productos mas vendidos, mejores clientes; en ellas el usuario prodrá realizar diferentes consultas al archivo sales.csv, y también aparecerá el botón salir, donde el usuario podrá cerrar sesión.
