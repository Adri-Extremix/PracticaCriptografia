import tkinter as tk
import sqlite3 as sql

con = sql.connect("base_de_datos.db")
cur = con.cursor()

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

def try_to_log_in(event):
    """Se encarga de gestionar el log in"""
    #Obtienes los datos de las entry
    name = entry_log_in_name.get()
    pwd = entry_log_in_pwd.get()
    #Buscas en la base de datos al usuario con esa contraseña
    res = cur.execute("SELECT * from usuario where usuario = '" + name + "' and contraseña = '" + pwd + "'")
    if res.fetchall() == []:
        #Si no has encontrado al usuario, imprimes un mensaje de error
        label_user_not_found_log_in.place(x=240,y=350)
        window.after(2000, delete_mssg, label_user_not_found_log_in)
    else:
        #Si has encontrado al usuario, cambias al frame de loading
        frm_log_in.pack_forget()
        frm_loading.pack()
    return

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
            cur.execute("INSERT INTO usuario VALUES('" + name + "','" + pwd + "')")
            con.commit()
        except sql.IntegrityError:
            delete_mssg(label_incorrect_sign_up_pwd)
            label_incorrect_sign_up_name.place(x=190, y=325)
            window.after(3500, delete_mssg, label_incorrect_sign_up_name)
            return 
    #Una vez insertado el dato, pasas al frame de loading
    frm_sign_up.pack_forget()
    frm_loading.pack()
    return

def delete_mssg(label):
    """Funcion que se encarga de borrar los mensajes de error"""
    label.place_forget()


#Ventana principal
window = tk.Tk()
window.title("Banki")
window.geometry("500x500")
window.resizable(width=False, height=False)

###Frame log_in
frm_log_in = tk.Frame(master=window, width=500, height=500, bg="#d3d3d0")
frm_log_in.pack_propagate(0)
frm_log_in.pack(fill="both")

#Título de la app y widgets del login
label_title = tk.Label(master=frm_log_in, text="Banki", fg="#000001", font=('Arial', 20, "bold"), bg="Blue")
label_title.pack(side="top", pady=60, ipady=15, ipadx=250)

label_log_in_name = tk.Label(master=frm_log_in, text="Nombre de usuario", fg="Blue", bg="#d3d3d0")
label_log_in_name.pack(side="top")

entry_log_in_name = tk.Entry(master=frm_log_in)
entry_log_in_name.pack(side="top")

label_log_in_pwd = tk.Label(master=frm_log_in, text="Contraseña", fg="Blue", bg="#d3d3d0")
label_log_in_pwd.pack(side="top")

entry_log_in_pwd = tk.Entry(master=frm_log_in, show= "*")
entry_log_in_pwd.pack(side="top")

log_in_button = tk.Button(
    master=frm_log_in, 
    text="Log in",
    width=10,
    height=2,
    bg="white",
    fg="blue",
    )
log_in_button.bind("<Button-1>", try_to_log_in)
log_in_button.pack(after=entry_log_in_pwd, pady=20)

sign_up_button = tk.Button(
    master=frm_log_in, 
    text="Sign up",
    width=10,
    height=2,
    bg="white",
    fg="blue",
    )
sign_up_button.bind("<Button-1>", log_in_to_sign_up)
sign_up_button.pack(side="bottom", pady=0)

sing_up_label = tk.Label(master=frm_log_in, text="Si no tienes una cuenta, haz click arriba", bg="#D3D3D0", fg="Blue")
sing_up_label.pack(side= "bottom", before=sign_up_button, pady=10)

label_user_not_found_log_in = tk.Label(master=frm_log_in, text="x", fg="Red", bg = "#d3d3d0", font=("Arial", 20, "bold"))

####Frame sign-in
frm_sign_up = tk.Frame(master=window, width=500, height=500, bg="#d3d3d0")
frm_sign_up.pack_propagate(0)

label_sign_up = tk.Label(master=frm_sign_up, text="SIGN UP", fg="#000001", bg="Blue", font=("Arial", 20, "bold"))
label_sign_up.pack(side="top", pady=60, ipady=15, ipadx=250)

label_sign_up_name = tk.Label(master=frm_sign_up, text="Usuario", fg="Blue", bg="#D3D3D0")
label_sign_up_name.pack()

entry_sign_up_name = tk.Entry(master=frm_sign_up)
entry_sign_up_name.pack(side="top")

label_sign_up_pwd = tk.Label(master=frm_sign_up, text="Introduce la contraseña", fg="Blue", bg="#D3D3D0")
label_sign_up_pwd.pack()

entry_sign_up_pwd = tk.Entry(master=frm_sign_up,show = "*")
entry_sign_up_pwd.pack(side="top")

label_sign_up_pwd_rep = tk.Label(master=frm_sign_up, text="Vuelve a introducir la contraseña", fg="Blue", bg="#D3D3D0")
label_sign_up_pwd_rep.pack()

entry_sign_up_pwd_rep = tk.Entry(master=frm_sign_up,show = "*")
entry_sign_up_pwd_rep.pack(side="top")

try_to_sign_up_button = tk.Button(
    master=frm_sign_up,
    text="Sign up",
    width=10,
    height=2,
    bg="white",
    fg="blue",
)
try_to_sign_up_button.place(x=150, y = 400)
try_to_sign_up_button.bind("<Button-1>", try_to_sign_up)

return_to_log_in = tk.Button(
    master=frm_sign_up,
    text="Go back",
    width=10,
    height=2,
    bg="red",
    fg="black",
)
return_to_log_in.place(x=275, y=400)
return_to_log_in.bind("<Button-1>", sign_up_to_log_in)

label_incorrect_sign_up_name = tk.Label(master=frm_sign_up, text="Usuario no válido", fg="Red", bg = "#d3d3d0", font=("Arial", 10, "bold"))
label_incorrect_sign_up_pwd = tk.Label(master=frm_sign_up, text="Las contraseñas no coinciden o no son válidas", fg="Red", bg = "#d3d3d0", font=("Arial", 10, "bold"))

### Frame transición
frm_loading = tk.Frame(master=window, width=500, height=500, bg="#d3d3d0")
frm_sign_up.pack_propagate(0)

label_loading = tk.Label(master=frm_loading, text="ENTRANDO", font=("Arial", 40, "bold"), fg="#4CBD49", bg="#D3D3D0")
label_loading.place(x=100, y=200)

#Mainloop
tk.mainloop()