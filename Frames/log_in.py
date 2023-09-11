import tkinter as tk
from . import window
###Frame log_in
frm_log_in = tk.Frame(master=window.window, width=500, height=500, bg="#d3d3d0")
frm_log_in.pack_propagate(0)

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

log_in_button.pack(after=entry_log_in_pwd, pady=20)

sign_up_button = tk.Button(
    master=frm_log_in, 
    text="Sign up",
    width=10,
    height=2,
    bg="white",
    fg="blue",
    )
log_in_button.pack(after=entry_log_in_pwd, pady=20)

sign_up_button = tk.Button(
    master=frm_log_in, 
    text="Sign up",
    width=10,
    height=2,
    bg="white",
    fg="blue",
    )
sign_up_button.pack(side="bottom", pady=0)

sing_up_label = tk.Label(master=frm_log_in, text="Si no tienes una cuenta, haz click arriba", bg="#D3D3D0", fg="Blue")
sing_up_label.pack(side= "bottom", before=sign_up_button, pady=10)

label_user_not_found_log_in = tk.Label(master=frm_log_in, text="x", fg="Red", bg = "#d3d3d0", font=("Arial", 20, "bold"))
