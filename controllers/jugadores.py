import os
from datetime import datetime
from utils.helpers import cargar_datos, guardar_datos, obtener_ultimo_id
from utils.validators import validar_entero_positivo

ARCHIVO_JUGADORES = "data/jugadores.json"
ARCHIVO_EQUIPOS = "data/equipos.json"

def listar_jugadores():
    """Lista todos los jugadores registrados"""
    jugadores = cargar_datos(ARCHIVO_JUGADORES)
    equipos = cargar_datos(ARCHIVO_EQUIPOS)
    
    if not jugadores:
        print("\nNo hay jugadores registrados")
        return []
    
    print("\n=== LISTA DE JUGADORES ===")
    print(f"{'ID':<5} {'Nombre':<25} {'Posición':<15} {'Dorsal':<8} {'Equipo':<20}")
    print("-" * 80)
    
    for jugador in jugadores:
        equipo_nombre = next((e['nombre'] for e in equipos if e['id'] == jugador['equipo_id']), "Desconocido")
        print(f"{jugador['id']:<5} {jugador['nombre']:<25} {jugador['posicion']:<15} {jugador['dorsal']:<8} {equipo_nombre:<20}")
    
    print(f"\nTotal: {len(jugadores)} jugadores")
    return jugadores

def crear_jugador():
    """Registra un nuevo jugador con validaciones"""
    jugadores = cargar_datos(ARCHIVO_JUGADORES)
    equipos = cargar_datos(ARCHIVO_EQUIPOS)
    
    if not equipos:
        print("\nPrimero debe registrar equipos")
        return
    
    print("\n=== REGISTRAR NUEVO JUGADOR ===")
    
    # Validación de nombre
    nombre = input("Nombre completo: ").strip()
    if not nombre:
        print("\nError: El nombre no puede estar vacío")
        return
    
    # Validación de posición
    posicion = input("Posición (ej. Delantero, Defensa): ").strip()
    if not posicion:
        print("\nError: La posición no puede estar vacía")
        return
    
    # Validación de dorsal
    while True:
        dorsal = input("Número de dorsal: ").strip()
        if not validar_entero_positivo(dorsal):
            print("Error: El dorsal debe ser un número positivo")
            continue
        dorsal = int(dorsal)
        break
    
    # Selección de equipo
    print("\nEquipos disponibles:")
    for equipo in equipos:
        print(f"{equipo['id']}: {equipo['nombre']}")
    
    while True:
        equipo_id = input("\nID del equipo: ").strip()
        if not validar_entero_positivo(equipo_id):
            print("Error: ID de equipo inválido")
            continue
        
        equipo_id = int(equipo_id)
        if equipo_id not in [e['id'] for e in equipos]:
            print("Error: No existe un equipo con ese ID")
            continue
        
        # Verificar dorsal único en equipo
        if any(j['equipo_id'] == equipo_id and j['dorsal'] == dorsal for j in jugadores):
            print("Error: Ya existe un jugador con ese dorsal en este equipo")
            continue
        
        break
    
    # Generar ID
    nuevo_id = obtener_ultimo_id(jugadores) + 1
    
    nuevo_jugador = {
        "id": nuevo_id,
        "nombre": nombre,
        "posicion": posicion,
        "dorsal": dorsal,
        "equipo_id": equipo_id,
        "goles": 0,
        "asistencias": 0,
        "tarjetas_amarillas": 0,
        "tarjetas_rojas": 0
    }
    
    jugadores.append(nuevo_jugador)
    
    if guardar_datos(ARCHIVO_JUGADORES, jugadores):
        print(f"\n✅ Jugador '{nombre}' registrado con ID {nuevo_id}")
    else:
        print("\n❌ Error al guardar el jugador")

def editar_jugador():
    """Edita la información de un jugador existente"""
    jugadores = cargar_datos(ARCHIVO_JUGADORES)
    equipos = cargar_datos(ARCHIVO_EQUIPOS)
    
    if not jugadores:
        print("\nNo hay jugadores registrados para editar")
        return
    
    # Mostrar lista de jugadores
    print("\n=== EDITAR JUGADOR ===")
    listado = listar_jugadores()
    
    try:
        jugador_id = int(input("\nIngrese el ID del jugador a editar: "))
    except ValueError:
        print("\nError: Debe ingresar un número válido")
        return
    
    # Buscar jugador
    jugador = next((j for j in jugadores if j['id'] == jugador_id), None)
    if not jugador:
        print("\nError: No se encontró jugador con ese ID")
        return
    
    print("\nDatos actuales del jugador:")
    print(f"1. Nombre: {jugador['nombre']}")
    print(f"2. Posición: {jugador['posicion']}")
    print(f"3. Dorsal: {jugador['dorsal']}")
    print(f"4. Equipo ID: {jugador['equipo_id']}")
    
    # Procesar cambios
    cambios = {}
    
    # Editar nombre
    nuevo_nombre = input("\nNuevo nombre (dejar vacío para mantener actual): ").strip()
    if nuevo_nombre:
        cambios['nombre'] = nuevo_nombre
    
    # Editar posición
    nueva_posicion = input("Nueva posición (dejar vacío para mantener actual): ").strip()
    if nueva_posicion:
        cambios['posicion'] = nueva_posicion
    
    # Editar dorsal
    while True:
        nuevo_dorsal = input("Nuevo dorsal (dejar vacío para mantener actual): ").strip()
        if not nuevo_dorsal:
            break
        try:
            nuevo_dorsal = int(nuevo_dorsal)
            if nuevo_dorsal <= 0:
                print("Error: Dorsal debe ser positivo")
                continue
            
            # Verificar dorsal único en equipo
            equipo_actual = jugador['equipo_id']
            if any(j['equipo_id'] == equipo_actual and j['dorsal'] == nuevo_dorsal and j['id'] != jugador_id for j in jugadores):
                print("Error: Dorsal ya existe en este equipo")
                continue
            
            cambios['dorsal'] = nuevo_dorsal
            break
        except ValueError:
            print("Error: Debe ser número entero")
    
    # Editar equipo
    print("\nEquipos disponibles:")
    for equipo in equipos:
        print(f"{equipo['id']}: {equipo['nombre']}")
    
    while True:
        nuevo_equipo = input("\nNuevo ID de equipo (dejar vacío para mantener actual): ").strip()
        if not nuevo_equipo:
            break
        try:
            nuevo_equipo = int(nuevo_equipo)
            if nuevo_equipo not in [e['id'] for e in equipos]:
                print("Error: ID de equipo no válido")
                continue
            
            # Si cambió el equipo, verificar dorsal en nuevo equipo
            if 'dorsal' in cambios or nuevo_equipo != jugador['equipo_id']:
                dorsal = cambios.get('dorsal', jugador['dorsal'])
                if any(j['equipo_id'] == nuevo_equipo and j['dorsal'] == dorsal and j['id'] != jugador_id for j in jugadores):
                    print("Error: Dorsal ya existe en el nuevo equipo")
                    continue
            
            cambios['equipo_id'] = nuevo_equipo
            break
        except ValueError:
            print("Error: Debe ser número entero")
    
    # Aplicar cambios
    if cambios:
        confirmar = input("\n¿Confirmar cambios? (s/n): ").lower()
        if confirmar == 's':
            jugador.update(cambios)
            if guardar_datos(ARCHIVO_JUGADORES, jugadores):
                print("\n✅ Jugador actualizado correctamente")
            else:
                print("\n❌ Error al guardar cambios")
        else:
            print("\n⚠️ Cambios cancelados")
    else:
        print("\n⚠️ No se realizaron cambios")

def eliminar_jugador():
    """Elimina un jugador del sistema con confirmación"""
    jugadores = cargar_datos(ARCHIVO_JUGADORES)
    
    if not jugadores:
        print("\nNo hay jugadores registrados para eliminar")
        return
    
    # Mostrar lista de jugadores
    print("\n=== ELIMINAR JUGADOR ===")
    listado = listar_jugadores()
    
    try:
        jugador_id = int(input("\nIngrese el ID del jugador a eliminar: "))
    except ValueError:
        print("\nError: Debe ingresar un número válido")
        return
    
    # Buscar jugador
    jugador = next((j for j in jugadores if j['id'] == jugador_id), None)
    if not jugador:
        print("\nError: No se encontró jugador con ese ID")
        return
    
    # Confirmar eliminación
    print(f"\nDatos del jugador a eliminar:")
    print(f"Nombre: {jugador['nombre']}")
    print(f"Posición: {jugador['posicion']}")
    print(f"Dorsal: {jugador['dorsal']}")
    print(f"Equipo ID: {jugador['equipo_id']}")
    
    confirmar = input("\n¿Está seguro que desea eliminar este jugador? (s/n): ").lower()
    if confirmar == 's':
        jugadores = [j for j in jugadores if j['id'] != jugador_id]
        if guardar_datos(ARCHIVO_JUGADORES, jugadores):
            print("\n✅ Jugador eliminado correctamente")
        else:
            print("\n❌ Error al eliminar jugador")
    else:
        print("\n⚠️ Eliminación cancelada")