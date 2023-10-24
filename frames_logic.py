"""Fichero que lleva la lógica de la aplicación"""
import tkinter as tk
import sqlite3 as sql
from datetime import datetime
import os
from criptografia import guarrear, verificar, derivar_key, derivar_key_sign_up, encriptado_autenticado, desencriptado_autenticado
from random import randint
from Frames.log_in import *
from Frames.sign_up import *
from Frames.loading import *
from Frames.app import *
from Frames.deposit_withdraw import *
from Frames.historial import *
from Frames.window import window

#Variables que sirven para conectarse a la base de datos
con = sql.connect("base_de_datos.db")
cur = con.cursor()
# Variable global para saber que tipo de operación hay que realizar
deposit_withdraw = None


"""Funciones que tienen la lógica de los cambios de frame"""
def calculate_date():
	"""Función que devuelve la fecha del día en formato DD/MM/YYYY"""
	now = datetime.now()
	day = now.day
    #Si el día es menor que 10, hay que concatenarle un 0 delante
	if day < 10:
		day = "0" + str(day)
	month = now.month
	#Si el mes es menor que 10, hay que concatenarle un 0 delante
	if month < 10:
		month = "0" + str(month)
	return str(day) +"/"+ str(month) +"/"+ str(now.year)

def loading_to_app():
	"""Función que cambia del frame de cargando al frame de la aplicación"""
	#Llamada a calculate balance para que obtenga el balance del usuario
	calculate_balance()

	#Borra el frame actual y dibujas el de la app
	frm_loading.pack_forget()
	frm_app.pack(fill="both")

	#Borra el contenido de las entradas de login y de sign up, para que cuando vuelvas a esos frames no haya info escrita
	entry_log_in_name.delete(0,len(entry_log_in_name.get()))
	entry_log_in_pwd.delete(0,len(entry_log_in_pwd.get()))

	entry_sign_up_name.delete(0,len(entry_sign_up_name.get()))
	entry_sign_up_pwd.delete(0,len(entry_sign_up_pwd.get()))
	entry_sign_up_pwd_rep.delete(0,len(entry_sign_up_pwd_rep.get()))

	return

def log_in_to_sign_up(event):
	"""Función que cambia el frame de log_in al frame de sign_up"""
	#Borra el frame anterior y dibuja el nuevo
	frm_log_in.pack_forget()
	frm_sign_up.pack(fill="both")

	#Borra los entrys de log in
	entry_log_in_name.delete(0,len(entry_log_in_name.get()))
	entry_log_in_pwd.delete(0,len(entry_log_in_pwd.get()))

	return

def sign_up_to_log_in(event):
    """Función que cambia el frame de sing_up al frame de log_in"""
    #Borra el frame anterior y dibuja el nuevo
    frm_sign_up.pack_forget()
    frm_log_in.pack(fill="both")
    
    #Borra los entrys de sign-up
    entry_sign_up_name.delete(0,len(entry_sign_up_name.get()))
    entry_sign_up_pwd.delete(0,len(entry_sign_up_pwd.get()))
    entry_sign_up_pwd_rep.delete(0,len(entry_sign_up_pwd_rep.get()))

    return

def app_to_login(event):
	"""Función que cambia el frame de app al frame de log in"""
	#Borra el frame anterior y dibuja el nuevo
	frm_app.pack_forget()
	frm_log_in.pack(fill="both")

	#Le quitas el valor a user_name
	global user_name
	global user_key_dev
	user_name = ""
	user_key_dev = ""
	return

def app_to_deposit(event):
	"""Función que cambia el frame de app al de operaciones de ingreso"""
	#Borra el frame anterior y dibuja el nuevo
	frm_app.pack_forget()
	frm_deposit_withdraw.pack(fill="both")

	#Pone el título correcto
	label_title_deposit_withdraw.config(text = "Ingresar")

	#Bool que indica el tipo de operación
	deposit_withdraw = 0
	return
	
def app_to_withdraw(event):
	"""Función que cambia el frame de app al de operaciones de retirada"""
	#Borra el frame anterior y dibuja el nuevo
	frm_app.pack_forget()
	frm_deposit_withdraw.pack(fill="both")

	#Pone el título correcto 
	label_title_deposit_withdraw.config(text = "Retirada")

	#Bool que indica el tipo de operacion
	deposit_withdraw = 1
	return

def app_to_record(event):
	"""Función que cambia el frame de app al de historial"""
	#Obtienes las operaciones del usuario y las guardas en una lista
	res = cur.execute("""Select dinero, dinero_nonce, tipo, tipo_nonce, concepto, concepto_nonce, fecha 
						from operaciones where usuario = ? order by id desc""", (user_name,))
	lista = res.fetchall()
	#Usas lista_dev para guardar los valores desencriptados
	lista_dev = []
	for j in range(len(lista)):
		row = []
		for i in range(3):
			#Llamas a desencriptado_autenticado para desencriptar las operaciones del usuario
		    row.append(desencriptado_autenticado(lista[j][2*i], lista[j][2*i + 1], user_key_dev))
		#Append de la fecha que nunca está encriptada
		row.append(lista[j][6])
		#Guardas la operacion en lista_dev
		lista_dev.append(row)

	#For que sirve para guardar las operaciones desencriptadas en un listbox, y que se muestre por pantalla
	for row in lista_dev:
		fila = "Fecha:" + str(row[3]) + " - Tipo:" + row[1] + " - Dinero:" + str(row[0]) + " - Concepto:" + row[2]
		listbox_record.insert(tk.END,fila)

	#Una vez que se desencriptan las operaciones, dibuja el nuevo frame
	frm_app.forget()
	frm_record.pack(fill="both")
	return
        
def deposit_withdraw_to_app(event):
	"""Función que cambia el frame de operaciones al de app"""
	#Borra los entrys de tus operaciones
	entry_deposit_withdraw_money.delete(0,len(entry_deposit_withdraw_money.get()))
	entry_deposit_withdraw_concept.delete(0,len(entry_deposit_withdraw_concept.get()))

	#Calcula el balance y dibuja el frame
	calculate_balance()
	frm_deposit_withdraw.forget()
	frm_app.pack(fill = "both")
	return

def record_to_app(event):
	"""Función que cambia el frame de historial al de app"""
	#Borra la lista de operaciones
	listbox_record.delete(0,tk.END)

	#Borra el frame anterior y dibuja el nuevo
	frm_record.pack_forget()
	frm_app.pack(fill="both")
	return

"""Funciones que contienen la lógica de la base de datos y las op"""

def try_to_log_in(event):
	"""Funciónb que se encarga de gestionar el log in"""
	#Se obtienen los datos de las entry
	name = entry_log_in_name.get()
	pwd = entry_log_in_pwd.get()

	#Busca en la base de datos al usuario con esa contraseña
	cur.execute("SELECT pwd_token, salt_token, salt_dev from usuarios where usuario = ?", (name,))
	res = cur.fetchall()

	if res == []:
		#Si no se encuentra al usuario, imprime un mensaje de error
		label_user_not_found_log_in.place(x=240,y=350)
		window.after(2000, delete_mssg, label_user_not_found_log_in)
		return 
	else:
		#Si se encuentra al usuario, intenta verificarlo con la contraseña, el token y el salt
		try: 
			verificar(pwd, res[0][0], res[0][1])
		except:
			#Si no se verifica el usuario, se imprime un mensaje de error
			label_user_not_found_log_in.place(x=240, y=350)
			window.after(2000, delete_mssg, label_user_not_found_log_in)
			return
		#Si se encuentra al usuario y se verifica, cambia al frame de loading
		frm_log_in.pack_forget()
		frm_loading.pack()
		
		#Al cabo de 500-1500 ms se cambia al frame de app
		window.after(randint(500,1500), loading_to_app)
		
		#Se inicializan las variables globales que durarán lo mismo que la sesión, que sirven para poder hacer operaciones y poder desencriptarlas
		global user_name
		global user_key_dev
		user_name = name
		user_key_dev = derivar_key(pwd, res[0][2])
	return name

def try_to_sign_up(event):
	"""Función que se encarga de gestionar el sign up"""
	#Obtiene los datos de los entrys, realizando comprobaciones sobre los mismos
	name = entry_sign_up_name.get()
	if (len(name) == 0):
		#Si el nombre es una cadena vacía, dibuja un mensaje de error
		delete_mssg(label_incorrect_sign_up_pwd)
		delete_mssg(label_incorrect_pwd_len)
		label_incorrect_sign_up_name.place(x=190, y=325)
		window.after(3500, delete_mssg, label_incorrect_sign_up_name)
		return
	pwd = entry_sign_up_pwd.get()
	pwd_rep = entry_sign_up_pwd_rep.get()

	#Si la longitud de la pwd es menor a 8, se imprime un mensaje de error
	if (len(pwd) < 8):
		delete_mssg(label_incorrect_sign_up_name)
		delete_mssg(label_incorrect_sign_up_pwd)
		label_incorrect_pwd_len.place(x=100, y=325)
		window.after(3500, delete_mssg, label_incorrect_pwd_len)
		return
		
	#Si las contraseñas no son iguales, dibuja un mensaje de error
	if (pwd != pwd_rep):
		delete_mssg(label_incorrect_sign_up_name)
		delete_mssg(label_incorrect_pwd_len)
		label_incorrect_sign_up_pwd.place(x=100, y=325)
		window.after(3500, delete_mssg, label_incorrect_sign_up_pwd)
		return
	else:
		#Intenta insertar el dato nuevo, pero si ya está en la base de datos, da un error
		try:
			#Obtiene la contraseña derivada y el salt con el que se ha derivado
		    salt_token, pwd_token = guarrear(pwd)
		    #Obtiene la contraseña para desencriptar los datos y el salt
		    key_dev, salt_dev = derivar_key_sign_up(pwd)    
		    #Se guardan los datos en la base de datos, encriptando el balance del nuevo usuario
		    cur.execute("INSERT INTO usuarios VALUES(?, ?, ?, ?)", (name, pwd_token, salt_token, salt_dev))
		    balance, balance_nonce = encriptado_autenticado("0", key_dev)
		    cur.execute("INSERT INTO balance VALUES(?,?,?)", (name, balance, balance_nonce,))
		    con.commit()
		except sql.IntegrityError:
			#Si da un mensaje de error de integridad, significa que el nombre de usuario ya está elegido, por lo que se dibuja un mensaje de error
		    delete_mssg(label_incorrect_sign_up_pwd)
		    delete_mssg(label_incorrect_pwd_len)
		    label_incorrect_sign_up_name.place(x=190, y=325)
		    window.after(3500, delete_mssg, label_incorrect_sign_up_name)
		    return 
	#Guarda el nombre del usuario y su contraseña de desencriptado 
	global user_name
	global user_key_dev
	user_name = name
	user_key_dev = key_dev

	#Borra el frame anterior y dibuja el nuevo
	frm_sign_up.pack_forget()
	frm_loading.pack()
	window.after(randint(500,1500), loading_to_app)
	return

def calculate_balance():
	"""Función que sirve para dibujar el balance"""
	#Obtiene el balance encriptado
	res = cur.execute("Select balance, balance_nonce from balance where usuario = ?", (user_name,))
	resultado = res.fetchall()

	#Desencripta el balance con la contraseña de desencriptado
	balance = desencriptado_autenticado(resultado[0][0], resultado[0][1], user_key_dev)

	#Si el balance es negativo, se dibuja en rojo, si no, se dibuja en verde
	if int(balance) < 0:
		color = "red"
	else:
		color = "green"

	#Se dibuja el balance
	label_app_balance.config(text = balance, fg = color)

def delete_mssg(label):
	"""Funcion que se encarga de borrar los mensajes de error"""
	label.place_forget()

def insert_deposit_withdraw(event):
	"""Función que se encarga de realizar la operacion"""
	#Obtienes el tipo de operacion y el dinero
	tipo = label_title_deposit_withdraw.cget("text")
	money = entry_deposit_withdraw_money.get()

	#Se intenta un cast a int del dinero, si no se consigue, el dinero no es un número, por lo tanto no se puede ingresar
	try:
		money = int(money)
	except:
		delete_mssg(label_concept_invalid)
		label_money_invalid.place(x=150, y=400)
		window.after(3500, delete_mssg, label_money_invalid)
		return

	#Obtiene el concepto de la operacion
	concept = entry_deposit_withdraw_concept.get()
	
	#El dinero ha de ser positivo
	if money < 0:
		delete_mssg(label_concept_invalid)
		label_money_invalid.place(x=150, y=400)
		window.after(3500, delete_mssg, label_money_invalid)
		return

	#La operación ha de tener un concepto
	if len(concept) == 0:
		delete_mssg(label_money_invalid)
		label_concept_invalid.place(x=125, y=400)
		window.after(3500, delete_mssg, label_concept_invalid)
		return

	#Cuando se verifican los datos, se calcula el id de la operacion y la fecha
	res = cur.execute("Select Count(usuario) from operaciones where usuario = ?", (user_name,))
	id = int(res.fetchall()[0][0])
	id = id + 1
	fecha = calculate_date()

	#Se encriptan todos los datos y se guardan en la base de datos, junto con los nonce necesarios
	money_encrypt, money_nonce = encriptado_autenticado(str(money), user_key_dev)
	tipo_encrypt, tipo_nonce = encriptado_autenticado(tipo[0:1], user_key_dev)
	concept_encrypt, concept_nonce = encriptado_autenticado(concept, user_key_dev)
	cur.execute("Insert into operaciones values(?, ?, ?, ?, ?, ?, ?, ?, ?)", 
	(user_name, str(id), fecha, money_encrypt, money_nonce, tipo_encrypt, tipo_nonce, concept_encrypt, concept_nonce))
	
	#Se calcula el balance nuevo, desencriptandolo debidamente
	res = cur.execute("Select balance, balance_nonce from balance where usuario = ?", (user_name,))
	resultado = res.fetchall()
	balance = int(desencriptado_autenticado(resultado[0][0], resultado[0][1], user_key_dev))
	if tipo == "Ingresar":
		balance = balance + money
	elif tipo == "Retirada":
		balance = balance - money
	
	#El nuevo balance se encripta, para así guardarlo en la base de datos
	balance, balance_nonce = encriptado_autenticado(str(balance), user_key_dev)
	cur.execute("Update balance set balance = ?, balance_nonce = ? where usuario = ?", (balance, balance_nonce, user_name))
	con.commit()
	deposit_withdraw_to_app(event)


"""Bindeo de botones a las funciones"""

# Frames log in
frm_log_in.pack(fill="both")
log_in_button.bind("<Button-1>", try_to_log_in)
sign_up_button.bind("<Button-1>", log_in_to_sign_up)

# Frames sign_up
try_to_sign_up_button.bind("<Button-1>", try_to_sign_up)
return_to_log_in.bind("<Button-1>", sign_up_to_log_in)

# Frames app
app_close_button.bind("<Button-1>",app_to_login)
app_deposit_button.bind("<Button-1>",app_to_deposit)
app_withdraw_button.bind("<Button-1>",app_to_withdraw)
app_record_button.bind("<Button-1>",app_to_record)

# Frames deposit/withdraw
deposit_withdraw_button.bind("<Button-1>",insert_deposit_withdraw)
return_deposit_withdraw.bind("<Button-1>",deposit_withdraw_to_app)

# Frames record
record_close_button.bind("<Button-1>",record_to_app)
#Mainloop
tk.mainloop()
