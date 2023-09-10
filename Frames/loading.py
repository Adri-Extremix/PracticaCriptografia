import tkinter as tk
from .  import window
### Frame transición
frm_loading = tk.Frame(master=window.window, width=500, height=500, bg="#d3d3d0")
frm_loading.pack_propagate(0)

label_loading = tk.Label(master=frm_loading, text="ENTRANDO", font=("Arial", 40, "bold"), fg="#4CBD49", bg="#D3D3D0")
label_loading.place(x=100, y=200)