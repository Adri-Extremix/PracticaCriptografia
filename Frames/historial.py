import tkinter as tk
from tkinter import ttk
from . import window
###Frame historial
frm_record = tk.Frame(master=window.window, width=500, height=500, bg="#d3d3d0")
frm_record.pack_propagate(0)

#Título de la app y widgets del login
label_record = tk.Label(master=frm_record, text="Historial de operaciones", fg="#000001", font=('Arial', 20, "bold"), bg="Blue")
label_record.pack(side="top", pady=60, ipady=15, ipadx=250)


record_close_button = tk.Button(
    master=frm_record, 
    text="Atrás",
    width=10,
    height=2,
    bg="white",
    fg="red",
    )

record_close_button.place(x=385, y = 10)

record_sign_button = tk.Button(
	master=frm_record,
	text="Firmar",
	width=10,
	height=2,
	bg="white",
	fg="blue",
)

record_sign_button.place(x=90, y=130)

listbox_record = tk.Listbox()

scroll_record = ttk.Scrollbar(master=frm_record, orient=tk.VERTICAL)
listbox_record = tk.Listbox(master=frm_record, yscrollcommand=scroll_record.set, width=450, height = 150)
scroll_record.config(command=listbox_record.yview)

scroll_record.pack(side=tk.RIGHT, fill=tk.Y)
listbox_record.pack()
