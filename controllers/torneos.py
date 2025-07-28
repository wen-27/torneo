import os
import json
from datetime import datetime
from utils.helpers import cargar_datos, guardar_datos, obtener_ultimo_id
from utils.validators import validar_fecha, validar_hora, validar_entero_positivo

ARCHIVO_TORNEOS = "data/torneos.json"
ARCHIVO_PARTIDOS = "data/partidos.json"
ARCHIVO_EQUIPOS = "data/equipos.json"

def listar_torneos():
    """Muestra todos los torneos registrados"""
    torneos = cargar_datos(ARCHIVO_TORNEOS)
    
    if not torneos:
        print("\nNo hay torneos registrados")
        return []
    
    print("\n=== LISTADO DE TORNEOS ===")
    encabezados = ["ID", "Nombre", "Tipo", "Fecha Inicio", "Fecha Fin", "Equipos"]
    print(f"{encabezados[0]:<5} {encabezados[1]:<25} {encabezados[2]:<15} {encabezados[3]:<12} {encabezados[4]:<12} {encabezados[5]:<5}")
    print("-" * 80)
    
    for torneo in torneos:
        print(f"{torneo['id']:<5} {torneo['nombre']:<25} {torneo['tipo']:<15} "
              f"{torneo['fecha_inicio']:<12} {torneo['fecha_fin']:<12} {len(torneo['equipos']):<5}")
    
    print(f"\nTotal de torneos: {len(torneos)}")
    return torneos

def crear_torneo():
    """Registra un nuevo torneo con validación"""
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
    
    # Selección de tipo
    tipo = seleccionar_tipo_torneo()
    if not tipo:
        return
    
    # Validación de fechas
    fecha_inicio, fecha_fin = obtener_fechas_validas()
    if not fecha_inicio or not fecha_fin:
        return
    
    # Selección de equipos
    equipos_ids = seleccionar_equipos_torneo(equipos)
    if not equipos_ids:
        return
    
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

def seleccionar_tipo_torneo():
    """Maneja la selección del tipo de torneo"""
    print("\nSeleccione el tipo de torneo:")
    print("1. Liga Local")
    print("2. Liga Internacional")
    
    while True:
        opcion = input("Opción (1-2): ").strip()
        if opcion == "1":
            return "Liga Local"
        elif opcion == "2":
            return "Liga Internacional"
        else:
            print("Error: Seleccione 1 o 2")

def obtener_fechas_validas():
    """Valida y obtiene las fechas de inicio y fin"""
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
        
        return fecha_inicio, fecha_fin

def seleccionar_equipos_torneo(equipos):
    """Maneja la selección de equipos participantes"""
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
    
    return equipos_ids

def programar_partido():
    """Gestiona la programación de un nuevo partido"""
    torneos = cargar_datos(ARCHIVO_TORNEOS)
    equipos = cargar_datos(ARCHIVO_EQUIPOS)
    
    if not torneos:
        print("\nNo hay torneos registrados")
        return
    
    # Selección de torneo
    torneo = seleccionar_torneo(torneos)
    if not torneo:
        return
    
    # Verificar equipos en el torneo
    if len(torneo['equipos']) < 2:
        print("\nError: El torneo no tiene suficientes equipos")
        return
    
    # Selección de equipos
    local_id, visitante_id = seleccionar_equipos_partido(torneo, equipos)
    if not local_id or not visitante_id:
        return
    
    # Fecha y hora del partido
    fecha, hora = obtener_fecha_hora_valida(local_id, visitante_id)
    if not fecha or not hora:
        return
    
    # Estadio (opcional)
    estadio = input("\nEstadio (opcional, presione Enter para omitir): ").strip()
    
    # Crear partido
    partidos = cargar_partidos()
    partido_id = obtener_ultimo_id(partidos) + 1 if partidos else 1
    
    nuevo_partido = {
        "id": partido_id,
        "torneo_id": torneo['id'],
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

def seleccionar_torneo(torneos):
    """Selecciona un torneo válido"""
    listar_torneos()
    try:
        torneo_id = int(input("\nID del torneo: ").strip())
        return next((t for t in torneos if t['id'] == torneo_id), None)
    except ValueError:
        print("\nError: Debe ingresar un número")
        return None

def seleccionar_equipos_partido(torneo, equipos):
    """Selecciona los equipos para el partido"""
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
            
            return local_id, visitante_id
        except ValueError:
            print("\nError: Debe ingresar números válidos")

def obtener_fecha_hora_valida(local_id, visitante_id):
    """Valida y obtiene fecha y hora sin conflictos"""
    while True:
        fecha = input("\nFecha del partido (YYYY-MM-DD): ").strip()
        hora = input("Hora del partido (HH:MM): ").strip()
        
        if not validar_fecha(fecha) or not validar_hora(hora):
            print("\nError: Formato de fecha u hora inválido")
            continue
        
        if verificar_conflicto_horario(fecha, hora, local_id, visitante_id):
            continue
        
        return fecha, hora

def verificar_conflicto_horario(fecha, hora, local_id, visitante_id):
    """Verifica conflictos de horario para los equipos"""
    partidos = cargar_partidos()
    
    for p in partidos:
        if p['fecha'] == fecha and p['hora'] == hora:
            equipos_conflicto = {p['local_id'], p['visitante_id']}
            if {local_id, visitante_id} & equipos_conflicto:
                print(f"\nError: Conflicto con partido {p['id']}")
                print(f"Equipos: {p['local_id']} vs {p['visitante_id']}")
                return True
    return False

def listar_partidos():
    """Muestra todos los partidos programados"""
    partidos = cargar_partidos()
    equipos = cargar_datos(ARCHIVO_EQUIPOS)
    torneos = cargar_datos(ARCHIVO_TORNEOS)
    
    if not partidos:
        print("\nNo hay partidos programados")
        return []
    
    print("\n=== LISTADO DE PARTIDOS ===")
    encabezados = ["ID", "Torneo", "Local", "vs", "Visitante", "Fecha", "Hora", "Estadio"]
    print(f"{encabezados[0]:<5} {encabezados[1]:<20} {encabezados[2]:<20} {encabezados[3]:<5} "
          f"{encabezados[4]:<20} {encabezados[5]:<12} {encabezados[6]:<8} {encabezados[7]:<20}")
    print("-" * 110)
    
    for partido in partidos:
        torneo_nombre = next((t['nombre'] for t in torneos if t['id'] == partido['torneo_id']), "Desconocido")
        local = next((e['nombre'] for e in equipos if e['id'] == partido['local_id']), "Desconocido")
        visitante = next((e['nombre'] for e in equipos if e['id'] == partido['visitante_id']), "Desconocido")
        
        print(f"{partido['id']:<5} {torneo_nombre:<20} {local:<20} {'vs':<5} {visitante:<20} "
              f"{partido['fecha']:<12} {partido['hora']:<8} {partido['estadio']:<20}")
    
    print(f"\nTotal de partidos: {len(partidos)}")
    return partidos

def cargar_partidos():
    """Carga los partidos desde el archivo"""
    if not os.path.exists(ARCHIVO_PARTIDOS):
        return []
    
    try:
        with open(ARCHIVO_PARTIDOS, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            return json.loads(contenido) if contenido.strip() else []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al cargar partidos: {str(e)}")
        return []

def guardar_partidos(partidos):
    """Guarda los partidos en el archivo"""
    try:
        with open(ARCHIVO_PARTIDOS, "w", encoding="utf-8") as archivo:
            json.dump(partidos, archivo, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error al guardar partidos: {str(e)}")
        return False