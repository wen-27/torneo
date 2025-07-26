import os
import sys

def limpiar_pantalla():
    if sys.platform == "linux" or sys.platform == "darwin":
        os.system('clear')
    else:
        os.system('cls')

def pausar_pantalla():
    if sys.platform == 'linux' or sys.platform == 'darwin':
        input('Presione Enter para continuar...')
    else: 
        os.system('pause')