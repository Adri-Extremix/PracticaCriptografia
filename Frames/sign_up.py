import tkinter as tk
from . import window
####Frame sign-in
frm_sign_up = tk.Frame(master=window.window, width=500, height=500, bg="#d3d3d0")
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
try_to_sign_up_button.place(x=275, y = 400)

return_to_log_in = tk.Button(
    master=frm_sign_up,
    text="Go back",
    width=10,
    height=2,
    bg="red",
    fg="black",
)
return_to_log_in.place(x=125, y=400)
label_incorrect_sign_up_name = tk.Label(master=frm_sign_up, text="Usuario no válido", fg="Red", bg = "#d3d3d0", font=("Arial", 10, "bold"))
label_incorrect_sign_up_pwd = tk.Label(master=frm_sign_up, text="Las contraseñas no coinciden o no son válidas", fg="Red", bg = "#d3d3d0",
font=("Arial", 10, "bold"))
label_incorrect_pwd_len = tk.Label(master=frm_sign_up, text="La contraseña ha de tener más de 8 carácteres", fg="Red", bg = "#d3d3d0", font=("Arial", 10, "bold"))
