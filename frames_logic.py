import tkinter as tk
import sqlite3 as sql
from random import randint
from Frames.log_in import *
from Frames.sign_up import *
from Frames.loading import *
from Frames.app import *
from Frames.window import window

con = sql.connect("base_de_datos.db")
cur = con.cursor()
# Variable global para 

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
    pass

def app_to_withdraw(event):
    pass

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
        label_incorrect_sign_up_name.place(x=190, y=325)
        window.after(3500, delete_mssg, label_incorrect_sign_up_name)
        return
    pwd = entry_sign_up_pwd.get()
    pwd_rep = entry_sign_up_pwd_rep.get()
    if (not pwd or not pwd_rep or pwd != pwd_rep):

        #Si las contraseñas no son válidas, dibujas el mensaje de error
        delete_mssg(label_incorrect_sign_up_name)
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
    info = res.fetchall()
    balance = info[0][1]
    label_app_balance.config(text = str(balance))
    

def delete_mssg(label):
    """Funcion que se encarga de borrar los mensajes de error"""
    label.place_forget()


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


#Mainloop
tk.mainloop()