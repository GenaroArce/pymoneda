import tkinter as tk
import customtkinter as ctk

from funcs import *

class Currency(tk.Tk):

    simbolos_monedas = ["USD", "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD"]

    def __init__(self):
        tk.Tk.__init__(self)
        self.menu()  

    def menu(self):

        self.pantalla = ctk.CTkFrame(self, width=600, height=300, corner_radius=5)
        self.geometry("600x300+1970+200")
        self.title("$$$ - PyMoneda V1.0 - $$$")
        self.maxsize(width=600, height=300)
        self.minsize(width=600, height=300)

        titulo = ctk.CTkLabel(self.pantalla, text="PyMoneda - V1.0", corner_radius=10, fg_color="cyan", text_color="black", width=200)
        titulo.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        simbolo = ctk.CTkLabel(self.pantalla, text="$", fg_color="gray", text_color="black", corner_radius=8, width=30)
        simbolo.place(relx=0.25, rely=0.4, anchor=tk.CENTER)

        valorMsg = "0.00"
        valorVar = ctk.StringVar(value=valorMsg)

        valor = ctk.CTkEntry(self.pantalla, textvariable=valorVar) 
        valor.place(relx=0.4, rely=0.4, anchor=tk.CENTER)
        valor.bind("<FocusIn>", lambda event: limpiar_texto(event, valor, valorMsg))
        valor.bind("<FocusOut>", lambda event: restaurar_texto(event, valor, valorMsg))
        valor.bind("<KeyRelease>", lambda event: validar_numeros(event, valorVar))

        defaultvariable = ctk.StringVar(value="Moneda")
        defaultvariable2 = ctk.StringVar(value="Moneda")

        opciones = ctk.CTkOptionMenu(self.pantalla, width=100, corner_radius=8, fg_color="gray", text_color="black", values=self.simbolos_monedas, variable=defaultvariable, button_color="white", button_hover_color="black")
        opciones.place(relx=0.8, rely=0.4, anchor=tk.CENTER)

        opciones2 = ctk.CTkOptionMenu(self.pantalla, width=100, corner_radius=8, fg_color="gray", text_color="black", values=self.simbolos_monedas, variable=defaultvariable2, button_color="white", button_hover_color="black")
        opciones2.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        boton = ctk.CTkButton(self.pantalla, text="Convertir", text_color="black", fg_color="green", command=lambda: convertir(self, valorVar.get(), defaultvariable.get(), defaultvariable2.get()), width=200)
        boton.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        self.pantalla.bind("<Button-1>", lambda event: quitar_foco(self, event))

        self.pantalla.pack()

if __name__ == "__main__":
    app = Currency()
    app.mainloop()