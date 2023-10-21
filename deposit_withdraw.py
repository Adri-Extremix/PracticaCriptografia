import tkinter as tk
from . import window
###Frame log_in
frm_deposit_withdraw = tk.Frame(master=window.window, width=500, height=500, bg="#d3d3d0")
frm_deposit_withdraw.pack_propagate(0)

#Título de la app y widgets del login
label_title_deposit_withdraw = tk.Label(master=frm_deposit_withdraw, text="PlaceHolder", fg="#000001", font=('Arial', 20, "bold"), bg="Blue")
label_title_deposit_withdraw.pack(side="top", pady=60, ipady=15, ipadx=250)

label_deposit_withdraw_money = tk.Label(master=frm_deposit_withdraw, text="Dinero", fg="Blue", bg="#d3d3d0")
label_deposit_withdraw_money.pack(side="top")

entry_deposit_withdraw_money = tk.Entry(master=frm_deposit_withdraw)
entry_deposit_withdraw_money.pack(side="top")

label_deposit_withdraw_concept = tk.Label(master=frm_deposit_withdraw, text="Concepto", fg="Blue", bg="#d3d3d0")
label_deposit_withdraw_concept.pack(side="top")

entry_deposit_withdraw_concept = tk.Entry(master=frm_deposit_withdraw)
entry_deposit_withdraw_concept.pack(side="top")


deposit_withdraw_button = tk.Button(
    master=frm_deposit_withdraw, 
    text="Enter",
    width=10,
    height=2,
    bg="white",
    fg="blue",
    )

deposit_withdraw_button.pack(side = "top", pady=20)

return_deposit_withdraw = tk.Button(
    master=frm_deposit_withdraw,
    text="Go back",
    width=10,
    height=2,
    bg="red",
    fg="black",
)
return_deposit_withdraw.place(x=385,y= 10)

label_money_invalid = tk.Label(master=frm_deposit_withdraw, text="Dinero no válido", fg="Red", bg = "#d3d3d0", font=("Arial", 20, "bold"))
label_concept_invalid = tk.Label(master=frm_deposit_withdraw, text="Concepto necesario", fg="Red", bg = "#d3d3d0", font=("Arial", 20, "bold"))
