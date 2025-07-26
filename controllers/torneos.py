import os
import json
from datetime import datetime
from utils.helpers import cargar_datos, guardar_datos, obtener_ultimo_id
from utils.validators import validar_fecha, validar_hora, validar_entero_positivo

ARCHIVO_TORNEOS = "data/torneos.json"
ARCHIVO_PARTIDOS = "data/partidos.json"
ARCHIVO_EQUIPOS = "data/equipos.json"

def listar_torneos():
    """Lista todos los torneos registrados"""
    torneos = cargar_datos(ARCHIVO_TORNEOS)
    
    if not torneos:
        print("\nNo hay torneos registrados")
        return []
    
    print("\n=== LISTADO DE TORNEOS ===")
    print(f"{'ID':<5} {'Nombre':<25} {'Tipo':<15} {'Fecha Inicio':<12} {'Fecha Fin':<12} {'Equipos':<5}")
    print("-" * 80)
    
    for torneo in torneos:
        print(f"{torneo['id']:<5} {torneo['nombre']:<25} {torneo['tipo']:<15} {torneo['fecha_inicio']:<12} {torneo['fecha_fin']:<12} {len(torneo['equipos']):<5}")
    
    print(f"\nTotal de torneos: {len(torneos)}")
    return torneos

def crear_torneo():
    """Crea un nuevo torneo con validación de datos"""
    equipos = cargar_datos(ARCHIVO_EQUIPOS)
    if not equipos:
        print("\nPrimero debe registrar equipos")
        return
    
    print("\n=== CREAR NUEVO TORNEO ===")
    
    # Validación de nombre
    nombre = input("Nombre del torneo: ").strip()
    if not nombre:
        print("\nError: El nombre no puede estar vacío")
        return
    
    # Tipo de torneo
    print("\nSeleccione el tipo de torneo:")
    print("1. Liga Local")
    print("2. Liga Internacional")
    
    while True:
        tipo_opcion = input("Opción (1-2): ").strip()
        if tipo_opcion == "1":
            tipo = "Liga Local"
            break
        elif tipo_opcion == "2":
            tipo = "Liga Internacional"
            break
        else:
            print("Error: Seleccione 1 o 2")
    
    # Validación de fechas
    while True:
        fecha_inicio = input("\nFecha de inicio (YYYY-MM-DD): ").strip()
        if not validar_fecha(fecha_inicio):
            print("Error: Formato de fecha inválido")
            continue
        
        fecha_fin = input("Fecha de fin (YYYY-MM-DD): ").strip()
        if not validar_fecha(fecha_fin):
            print("Error: Formato de fecha inválido")
            continue
        
        if fecha_fin < fecha_inicio:
            print("Error: La fecha de fin debe ser posterior a la de inicio")
            continue
        
        break
    
    # Selección de equipos
    print("\nEquipos disponibles:")
    for equipo in equipos:
        print(f"{equipo['id']}: {equipo['nombre']}")
    
    equipos_ids = []
    while True:
        equipo_id = input("\nID del equipo a añadir (0 para terminar): ").strip()
        if equipo_id == "0":
            if len(equipos_ids) < 2:
                print("Error: Debe haber al menos 2 equipos")
                continue
            break
        
        if not validar_entero_positivo(equipo_id):
            print("Error: ID debe ser un número positivo")
            continue
        
        equipo_id = int(equipo_id)
        if equipo_id not in [e['id'] for e in equipos]:
            print("Error: No existe un equipo con ese ID")
            continue
        
        if equipo_id in equipos_ids:
            print("Error: Equipo ya añadido")
            continue
        
        equipos_ids.append(equipo_id)
        print(f"Equipos añadidos: {len(equipos_ids)}")
    
    # Crear torneo
    torneos = cargar_datos(ARCHIVO_TORNEOS)
    nuevo_id = obtener_ultimo_id(torneos) + 1 if torneos else 1
    
    nuevo_torneo = {
        "id": nuevo_id,
        "nombre": nombre,
        "tipo": tipo,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "equipos": equipos_ids,
        "partidos": []
    }
    
    torneos.append(nuevo_torneo)
    
    if guardar_datos(ARCHIVO_TORNEOS, torneos):
        print(f"\n✅ Torneo '{nombre}' creado con ID {nuevo_id}")
    else:
        print("\n❌ Error al crear torneo")

def programar_partido():
    """Programa un nuevo partido en un torneo existente"""
    torneos = cargar_datos(ARCHIVO_TORNEOS)
    equipos = cargar_datos(ARCHIVO_EQUIPOS)
    
    if not torneos:
        print("\nNo hay torneos registrados")
        return
    
    # Seleccionar torneo
    listar_torneos()
    try:
        torneo_id = int(input("\nID del torneo: ").strip())
        torneo = next((t for t in torneos if t['id'] == torneo_id), None)
        if not torneo:
            print("\nError: Torneo no encontrado")
            return
    except ValueError:
        print("\nError: Debe ingresar un número")
        return
    
    # Verificar equipos en el torneo
    if len(torneo['equipos']) < 2:
        print("\nError: El torneo no tiene suficientes equipos")
        return
    
    # Seleccionar equipos
    print("\nEquipos participantes:")
    for equipo_id in torneo['equipos']:
        equipo = next((e for e in equipos if e['id'] == equipo_id), None)
        if equipo:
            print(f"{equipo['id']}: {equipo['nombre']}")
    
    while True:
        try:
            local_id = int(input("\nID del equipo local: ").strip())
            if local_id not in torneo['equipos']:
                print("\nError: Equipo no está en este torneo")
                continue
            
            visitante_id = int(input("ID del equipo visitante: ").strip())
            if visitante_id not in torneo['equipos']:
                print("\nError: Equipo no está en este torneo")
                continue
            
            if local_id == visitante_id:
                print("\nError: No puede ser el mismo equipo")
                continue
            
            break
        except ValueError:
            print("\nError: Debe ingresar números válidos")
    
    # Fecha y hora del partido
    while True:
        fecha = input("\nFecha del partido (YYYY-MM-DD): ").strip()
        hora = input("Hora del partido (HH:MM): ").strip()
        
        if not validar_fecha(fecha) or not validar_hora(hora):
            print("\nError: Formato de fecha u hora inválido")
            continue
        
        # Verificar conflictos de horario
        partidos = cargar_partidos()
        conflicto = False
        
        for p in partidos:
            if p['fecha'] == fecha and p['hora'] == hora:
                if p['local_id'] == local_id or p['visitante_id'] == local_id or p['local_id'] == visitante_id or p['visitante_id'] == visitante_id:
                    print(f"\nError: Conflicto con partido {p['id']}")
                    print(f"Equipos: {p['local_id']} vs {p['visitante_id']}")
                    conflicto = True
                    break
        
        if not conflicto:
            break
    
    # Estadio (opcional)
    estadio = input("\nEstadio (opcional, presione Enter para omitir): ").strip()
    
    # Crear partido
    partidos = cargar_partidos()
    partido_id = obtener_ultimo_id(partidos) + 1 if partidos else 1
    
    nuevo_partido = {
        "id": partido_id,
        "torneo_id": torneo_id,
        "local_id": local_id,
        "visitante_id": visitante_id,
        "fecha": fecha,
        "hora": hora,
        "estadio": estadio if estadio else "Por definir",
        "resultado": None,
        "goles_local": 0,
        "goles_visitante": 0,
        "tarjetas_amarillas": 0,
        "tarjetas_rojas": 0
    }
    
    partidos.append(nuevo_partido)
    torneo['partidos'].append(partido_id)
    
    if guardar_partidos(partidos) and guardar_datos(ARCHIVO_TORNEOS, torneos):
        print(f"\n✅ Partido programado con ID {partido_id}")
    else:
        print("\n❌ Error al programar partido")

def listar_partidos():
    """Lista todos los partidos programados"""
    partidos = cargar_partidos()
    equipos = cargar_datos(ARCHIVO_EQUIPOS)
    torneos = cargar_datos(ARCHIVO_TORNEOS)
    
    if not partidos:
        print("\nNo hay partidos programados")
        return []
    
    print("\n=== LISTADO DE PARTIDOS ===")
    print(f"{'ID':<5} {'Torneo':<20} {'Local':<20} {'vs':<5} {'Visitante':<20} {'Fecha':<12} {'Hora':<8} {'Estadio':<20}")
    print("-" * 110)
    
    for partido in partidos:
        torneo_nombre = next((t['nombre'] for t in torneos if t['id'] == partido['torneo_id']), "Desconocido")
        local = next((e['nombre'] for e in equipos if e['id'] == partido['local_id']), "Desconocido")
        visitante = next((e['nombre'] for e in equipos if e['id'] == partido['visitante_id']), "Desconocido")
        
        print(f"{partido['id']:<5} {torneo_nombre:<20} {local:<20} {'vs':<5} {visitante:<20} {partido['fecha']:<12} {partido['hora']:<8} {partido['estadio']:<20}")
    
    print(f"\nTotal de partidos: {len(partidos)}")
    return partidos

# Funciones auxiliares para manejo de archivos
def cargar_partidos():
    """Carga los partidos desde el archivo JSON"""
    if not os.path.exists(ARCHIVO_PARTIDOS):
        return []
    
    try:
        with open(ARCHIVO_PARTIDOS, "r", encoding="utf-8") as file:
            content = file.read()
            return json.loads(content) if content.strip() else []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al cargar partidos: {str(e)}")
        return []

def guardar_partidos(partidos):
    """Guarda los partidos en el archivo JSON"""
    try:
        with open(ARCHIVO_PARTIDOS, "w", encoding="utf-8") as file:
            json.dump(partidos, file, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error al guardar partidos: {str(e)}")
        return False