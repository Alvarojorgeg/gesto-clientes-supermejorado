import os
import platform
import re

def limpiar_pantalla():
    os.system('cls') if platform.system() == "Windows" else os.system('clear')

def leer_texto(min_len=0, max_len=100, mensaje=None):
    if mensaje:
        print(mensaje)
    while True:
        texto = input("> ")
        if min_len <= len(texto) <= max_len:
            return texto

def dni_valido(dni, lista):
    if not re.match('[0-9]{2}[A-Z]$', dni):
        print("DNI incorrecto, debe cumplir el formato.")
        return False
    if any(cliente.dni == dni for cliente in lista):
        print("DNI utilizado por otro cliente.")
        return False
    return True
