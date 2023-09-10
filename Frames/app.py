import tkinter as tk
from . import window
###Frame app
frm_app = tk.Frame(master=window.window, width=500, height=500, bg="#d3d3d0")
frm_app.pack_propagate(0)

#Título de la app y widgets del login
label_title = tk.Label(master=frm_app, text="Balance", fg="#000001", font=('Arial', 20, "bold"), bg="Blue")
label_title.pack(side="top", pady=60, ipady=15, ipadx=250)


app_deposit_button = tk.Button(
    master=frm_app, 
    text="Ingreso",
    width=10,
    height=2,
    bg="white",
    fg="blue",
    )

app_deposit_button.place(x=125, y = 400)

app_withdraw_button = tk.Button(
    master=frm_app, 
    text="Gasto",
    width=10,
    height=2,
    bg="white",
    fg="blue",
    )
app_withdraw_button.place(x=275, y=400)

app_close_button = tk.Button(
    master=frm_app, 
    text="Cerrrar sesión",
    width=10,
    height=2,
    bg="white",
    fg="red",
    )
app_close_button.place(x=385,y= 10)
