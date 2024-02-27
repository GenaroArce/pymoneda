import tkinter as tk
import customtkinter as ctk

import requests

import pandas as pd
from pandas.io.excel import ExcelWriter

def validar_numeros(event, variable):
    contenido = variable.get()
    if not contenido.isdigit():  
        variable.set(''.join(filter(str.isdigit, contenido)))

def limpiar_texto(event, entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, tk.END)
def restaurar_texto(event, entry, default_text):
    if entry.get() == "":
        entry.insert(0, default_text)

def quitar_foco(self, event):
    self.pantalla.focus_set()

def manejo_errores(self, mensaje, color):
    if hasattr(self, "resultado_label"):
        self.resultado_label.destroy()
    self.resultado_label = ctk.CTkLabel(self.pantalla, text=mensaje, fg_color=color, text_color="black", corner_radius=8)
    self.resultado_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

def manejo_valido(self, mensaje, color, valor, moneda, moneda_convertida, conversion):
    if hasattr(self, "resultado_boton"):
        self.resultado_boton.destroy()
    self.resultado_boton = ctk.CTkButton(self.pantalla, text=mensaje, fg_color=color, text_color="black", corner_radius=8, command=lambda: guardar_excel(self, valor, moneda, moneda_convertida, conversion))
    self.resultado_boton.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
    self.boton_guardar = self.resultado_boton

def convertir(self, valor, moneda, moneda_convertir):
    if not valor.isdigit():
        manejo_errores(self, "ERROR: Solo puedes ingresar NUMEROS", "orange")
        return
    elif int(valor) == 0.00:
        manejo_errores(self, "ERROR: Debes ingresar un valor mayor a 0", "orange")
        return
    elif moneda == "Moneda" and moneda_convertir == "Moneda":
        manejo_errores(self, "ERROR: Debes elegir una moneda", "orange")
        return
    elif moneda == moneda_convertir or moneda_convertir == moneda:
        manejo_errores(self, "ERROR: Debes elegir distintas monedas", "orange")
        return
    
    resultado_conversion, error = conversor(float(valor), moneda, moneda_convertir)
    if error:
        manejo_errores(self, "ERROR: Se acaba de producir un error al convertir", "red")
    else:
        manejo_errores(self, "{0} {1} se acaban de convertir en {2} {3}".format(valor, moneda, moneda_convertir, resultado_conversion), "green")
        manejo_valido(self, "Guardar en TXT", "yellow", valor, moneda, moneda_convertir, resultado_conversion)
        if hasattr(self, "boton_guardar"): 
            self.boton_guardar.configure(state=tk.NORMAL)

def conversor(monto, moneda, moneda_convertir):
    api_url = f"https://open.er-api.com/v6/latest/{moneda}"
    respuesta = requests.get(api_url)
    data = respuesta.json()
    if 'error' in data:
        return None, data['error']
    if moneda_convertir not in data['rates']:
        return None, f"La moneda {moneda_convertir} no esta registrada."
    excambio = data['rates'][moneda_convertir]
    monto_convertido = monto * excambio
    return monto_convertido, None

def guardar_excel(self, moneda, valor, moneda_convertida, conversion):
    if hasattr(self, "boton_guardar") and self.boton_guardar.cget('state') == tk.NORMAL:
        manejo_errores(self, "Guardado en el Excel", "green")
        resultados = [moneda, valor, moneda_convertida, conversion]
        valores = [
            ["Moneda", "Monto", "Moneda Convertida", "Resultado"],
            [moneda, valor, moneda_convertida, conversion]
        ]
        df = pd.DataFrame(valores[1:], columns=valores[0])

        try:
            existing_df = pd.read_excel("resultados.xlsx")
            updated_df = pd.concat([existing_df, df], ignore_index=True)
        except FileNotFoundError: 
            updated_df = df

        with ExcelWriter("resultados.xlsx") as writer:
            updated_df.to_excel(writer, index=False)
        self.boton_guardar.configure(state=tk.DISABLED) 
