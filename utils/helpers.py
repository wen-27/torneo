import json
import os

def cargar_datos(archivo):
    """Carga datos desde un archivo JSON"""
    if not os.path.exists(archivo):
        return []
    
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            content = file.read()
            return json.loads(content) if content.strip() else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_datos(archivo, datos):
    """Guarda datos en un archivo JSON"""
    try:
        with open(archivo, "w", encoding="utf-8") as file:
            json.dump(datos, file, indent=4, ensure_ascii=False)
        return True
    except IOError:
        return False

def obtener_ultimo_id(datos):
    """Obtiene el último ID de una lista de diccionarios con clave 'id'"""
    return max(item['id'] for item in datos) if datos else 0