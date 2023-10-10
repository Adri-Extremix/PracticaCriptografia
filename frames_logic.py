import tkinter as tk
import sqlite3 as sql
from datetime import datetime
from random import randint
from Frames.log_in import *
from Frames.sign_up import *
from Frames.loading import *
from Frames.app import *
from Frames.deposit_withdraw import *
from Frames.historial import *
from Frames.window import window

con = sql.connect("PracticaCriptografia-main/base_de_datos.db")
cur = con.cursor()

# Variable global 
deposit_withdraw = None

def calculate_date():
    now = datetime.now()
    day = now.day
    if day < 10:
        day = "0" + str(day)
    month = now.month
    if month < 10:
        month = "0" + str(month)
    return str(day) +"/"+ str(month) +"/"+ str(now.year)

def loading_to_app():

    calculate_balance()
    frm_loading.pack_forget()
    frm_app.pack(fill="both")

    entry_log_in_name.delete(0,len(entry_log_in_name.get()))
    entry_log_in_pwd.delete(0,len(entry_log_in_pwd.get()))

    entry_sign_up_name.delete(0,len(entry_sign_up_name.get()))
    entry_sign_up_pwd.delete(0,len(entry_sign_up_pwd.get()))
    entry_sign_up_pwd_rep.delete(0,len(entry_sign_up_pwd_rep.get()))

    return

def log_in_to_sign_up(event):
    """Función que cambia el frame de log_in al frame de sign_up"""
    # Borramos los entrys del frame anterior

    frm_log_in.pack_forget()
    frm_sign_up.pack(fill="both")

    entry_log_in_name.delete(0,len(entry_log_in_name.get()))
    entry_log_in_pwd.delete(0,len(entry_log_in_pwd.get()))
    
    return

def sign_up_to_log_in(event):
    """Función que cambia el frame de sing_up al frame de log_in"""
    # Borramos los entrys del frame anterior
    

    frm_sign_up.pack_forget()
    frm_log_in.pack(fill="both")
    
    entry_sign_up_name.delete(0,len(entry_sign_up_name.get()))
    entry_sign_up_pwd.delete(0,len(entry_sign_up_pwd.get()))
    entry_sign_up_pwd_rep.delete(0,len(entry_sign_up_pwd_rep.get()))

    return

def app_to_login(event):
    frm_app.pack_forget()
    frm_log_in.pack(fill="both")
    global user_name
    user_name = None
    return

def app_to_deposit(event):
    frm_app.pack_forget()
    frm_deposit_withdraw.pack(fill="both")
    label_title_deposit_withdraw.config(text = "Ingresar")
    deposit_withdraw = 0

def app_to_withdraw(event):
    frm_app.pack_forget()
    frm_deposit_withdraw.pack(fill="both")
    label_title_deposit_withdraw.config(text = "Retirada")
    deposit_withdraw = 1

def app_to_record(event):

    res = cur.execute("Select * from operaciones where usuario = '"+user_name+"' order by id desc")
    list = res.fetchall()
    for row in list:
        fila = "Fecha:" + str(row[4]) + " - Tipo:" + row[3] + " - Dinero:" + str(row[2]) + " - Concepto:" + row[5]
        listbox_record.insert(tk.END,fila)
    frm_app.forget()
    frm_record.pack(fill="both")
    return
        
def deposit_withdraw_to_app(event):
    
    entry_deposit_withdraw_money.delete(0,len(entry_deposit_withdraw_money.get()))
    entry_deposit_withdraw_concept.delete(0,len(entry_deposit_withdraw_concept.get()))
    calculate_balance()
    frm_deposit_withdraw.forget()
    frm_app.pack(fill = "both")

def record_to_app(event):
    listbox_record.delete(0,tk.END)
    frm_record.pack_forget()
    frm_app.pack(fill="both")
    return

def try_to_log_in(event):
    """Se encarga de gestionar el log in"""
    #Obtienes los datos de las entry
    name = entry_log_in_name.get()
    pwd = entry_log_in_pwd.get()
    #Buscas en la base de datos al usuario con esa contraseña
    res = cur.execute("SELECT * from usuarios where usuario = '" + name + "' and contraseña = '" + pwd + "'")
    if res.fetchall() == []:
        #Si no has encontrado al usuario, imprimes un mensaje de error
        label_user_not_found_log_in.place(x=240,y=350)
        window.after(2000, delete_mssg, label_user_not_found_log_in)
        return 
    else:
        #Si has encontrado al usuario, cambias al frame de loading
        frm_log_in.pack_forget()
        frm_loading.pack()
        window.after(randint(500,1500), loading_to_app)
        global user_name
        user_name = name
    return name

def try_to_sign_up(event):
    """Se encarga de gestionar el sign up"""
    #Obtienes los datos de los entrys, realizando comprobaciones sobre los mismos
    name = entry_sign_up_name.get()
    if (len(name) == 0):
        #Si el nombre es una cadena vacía, dibujas un mensaje de error
        delete_mssg(label_incorrect_sign_up_pwd)
        delete_mssg(label_incorrect_pwd_len)
        label_incorrect_sign_up_name.place(x=190, y=325)
        window.after(3500, delete_mssg, label_incorrect_sign_up_name)
        return
    pwd = entry_sign_up_pwd.get()
    pwd_rep = entry_sign_up_pwd_rep.get()
    if (len(pwd) < 8):
    	delete_mssg(label_incorrect_sign_up_name)
    	delete_mssg(label_incorrect_sign_up_pwd)
    	label_incorrect_pwd_len.place(x=100, y=325)
    	window.after(3500, delete_mssg, label_incorrect_pwd_len)
    	return
    if (pwd != pwd_rep):
        #Si las contraseñas no son válidas, dibujas el mensaje de error
        delete_mssg(label_incorrect_sign_up_name)
        delete_mssg(label_incorrect_pwd_len)
        label_incorrect_sign_up_pwd.place(x=100, y=325)
        window.after(3500, delete_mssg, label_incorrect_sign_up_pwd)
        return
    else:
        #Intentas insertar el dato nuevo, pero si ya está en la base de datos, te da un error
        try:
            cur.execute("INSERT INTO usuarios VALUES('" + name + "','" + pwd + "')")
            cur.execute("INSERT INTO balance VALUES('" + name + "',0)")
            con.commit()
        except sql.IntegrityError:
            delete_mssg(label_incorrect_sign_up_pwd)
            label_incorrect_sign_up_name.place(x=190, y=325)
            window.after(3500, delete_mssg, label_incorrect_sign_up_name)
            return 
    #Una vez insertado el dato, pasas al frame de loading
    global user_name
    user_name = name
    frm_sign_up.pack_forget()
    frm_loading.pack()
    window.after(randint(500,1500), loading_to_app)
    return

def calculate_balance():
    res = cur.execute("Select * from balance where usuario = '" + user_name + "'")
    balance = res.fetchall()[0][1]
    if balance < 0:
        color = "red"
    else:
        color = "green"
    label_app_balance.config(text = str(balance)+ "€", fg = color)
    
def delete_mssg(label):
    """Funcion que se encarga de borrar los mensajes de error"""
    label.place_forget()

def insert_deposit_withdraw(event):

    tipo = label_title_deposit_withdraw.cget("text")
    money = entry_deposit_withdraw_money.get()
    try:
        money = int(money)
    except:
        delete_mssg(label_concept_invalid)
        label_money_invalid.place(x=150, y=400)
        window.after(3500, delete_mssg, label_money_invalid)
        return
    concept = entry_deposit_withdraw_concept.get()

    if money < 0:
        delete_mssg(label_concept_invalid)
        label_money_invalid.place(x=150, y=400)
        window.after(3500, delete_mssg, label_money_invalid)
        return
    
    if len(concept) == 0:
        delete_mssg(label_money_invalid)
        label_concept_invalid.place(x=125, y=400)
        window.after(3500, delete_mssg, label_concept_invalid)
        return
    res = cur.execute("Select Count(usuario) from operaciones where usuario = '"+ user_name +"'")
    id = int(res.fetchall()[0][0])
    id = id + 1
    fecha = calculate_date()
    cur.execute("Insert into operaciones values('" + user_name + "'," + str(id)+ "," + str(money) + ",'" + tipo[0:1] + "','" + fecha + "','" + concept + "')")
    res = cur.execute("Select * from balance where usuario = '" + user_name + "'")
    balance = res.fetchall()[0][1]

    if tipo == "Ingresar":
        balance = balance + money

    elif tipo == "Retirada":
        balance = balance - money

    cur.execute("Update balance set balance = "+str(balance)+" where usuario ='" + user_name +"'")
    con.commit()
    deposit_withdraw_to_app(event)

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
