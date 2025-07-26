from datetime import datetime

def validar_fecha(fecha_str, formato="%Y-%m-%d"):
    try:
        datetime.strptime(fecha_str, formato)
        return True
    except ValueError:
        return False

def validar_hora(hora_str):
    return validar_fecha(hora_str, "%H:%M")

def validar_entero_positivo(valor):
    try:
        return int(valor) > 0
    except ValueError:
        return False