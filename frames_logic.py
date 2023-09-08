import sqlite3 as sql
import tkinter as tk

def delete_prueba() -> None:
    try:
        cur.execute("DROP TABLE prueba")
        print("Table deleted!")
    except sql.OperationalError:
        print("Table does not exist!")
    return

def create_table_prueba() -> None:
    try:
       cur.execute("CREATE TABLE prueba(name TEXT, PRIMARY KEY (name))")
       print("Table created!")
    except sql.OperationalError:
        print("Table already created!")
    return

def insert_on_prueba(name:str) -> None:
    try:
        cur.execute("INSERT INTO prueba VALUES ('" +  name + "')")
    except sql.IntegrityError:
        print("Ese dato ya esta en la tabla")
    con.commit()
    return

def buscar_en_prueba(name: str) -> None:
    res = cur.execute("SELECT * FROM prueba where name = '" + name + "'")
    print(res.fetchall())
    return

con = sql.connect("Prueba.db")
cur = con.cursor()
 

def log_in_to_sign_up(event):
    """Función que cambia el frame de log_in al frame de sign_in"""
    frm_log_in.pack_forget()
    frm_sign_up.pack()
    return

def try_to_log_in(event):
    name = entry_log_in_name.get()
    res = cur.execute("SELECT * from prueba where name = '" + name + "'")
    if res.fetchall() == []:
        label_user_not_found.pack(side="top", after=log_in_button)
        window.after(2000, delete_cross)
    return

def delete_cross():
    label_user_not_found.pack_forget()

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
label_title.pack(side="top", pady=75, ipadx=250)

label_log_in_name = tk.Label(master=frm_log_in, text="Nombre de usuario", fg="Blue", bg="#d3d3d0")
entry_log_in_name = tk.Entry(master=frm_log_in)

label_log_in_name.pack(side="top")
entry_log_in_name.pack(side="top")

log_in_button = tk.Button(
    master=frm_log_in, 
    text="Log in",
    width=10,
    height=2,
    bg="white",
    fg="blue",
    )
log_in_button.bind("<Button-1>", try_to_log_in)
log_in_button.pack(after=entry_log_in_name, pady=20)

sign_up_button = tk.Button(
    master=frm_log_in, 
    text="Sign up",
    width=10,
    height=2,
    bg="white",
    fg="blue",
    )
sign_up_button.bind("<Button-1>", log_in_to_sign_up)
sign_up_button.pack(side="bottom", pady=50)

label_user_not_found = tk.Label(master=frm_log_in, text="x", fg="Red", bg = "#d3d3d0", font=("Arial", 20, "bold"))

####Frame sign-in
frm_sign_up = tk.Frame()

label_sign_up = tk.Label(master=frm_sign_up, text="Sign up here please")
label_sign_up.pack()


#Mainloop
tk.mainloop()