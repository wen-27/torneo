import os
from datetime import datetime
from utils.helpers import cargar_datos, guardar_datos, obtener_ultimo_id
from utils.validators import validar_fecha

ARCHIVO_EQUIPOS = "data/equipos.json"

def listar_equipos():
    """Muestra todos los equipos en formato de tabla"""
    equipos = cargar_datos(ARCHIVO_EQUIPOS)
    
    if not equipos:
        print("\nNo hay equipos registrados.")
        return []
    
    print("\n=== LISTADO DE EQUIPOS ===")
    print(f"{'ID':<5} {'Nombre':<25} {'Fundación':<12} {'País':<20} {'Liga ID':<10}")
    print("-" * 80)
    
    for equipo in equipos:
        print(f"{equipo['id']:<5} {equipo['nombre']:<25} {equipo['fundacion']:<12} {equipo['pais']:<20} {equipo['liga_id']:<10}")
    
    print(f"\nTotal de equipos: {len(equipos)}")
    return equipos

def crear_equipo():
    """Registra nuevos equipos con validación"""
    equipos = cargar_datos(ARCHIVO_EQUIPOS)
    
    print("\n=== REGISTRAR NUEVO EQUIPO ===")
    
    # Validación de nombre
    while True:
        nombre = input("Nombre del equipo: ").strip()
        if not nombre:
            print("Error: El nombre no puede estar vacío")
            continue
        
        if any(e['nombre'].lower() == nombre.lower() for e in equipos):
            print("Error: Ya existe un equipo con ese nombre")
            continue
        
        break
    
    # Validación de fundación
    while True:
        fundacion = input("Año de fundación (YYYY): ").strip()
        if not validar_fecha(fundacion + "-01-01") or int(fundacion) <= 1800 or int(fundacion) > datetime.now().year:
            print("Error: Año inválido (debe ser entre 1800 y el año actual)")
            continue
        break
    
    # Validación de país
    pais = input("País: ").strip()
    if not pais:
        pais = "Desconocido"
    
    # Generar nuevo ID
    nuevo_id = obtener_ultimo_id(equipos) + 1
    
    nuevo_equipo = {
        "id": nuevo_id,
        "nombre": nombre,
        "fundacion": fundacion,
        "pais": pais,
        "liga_id": nuevo_id  # Por defecto, usamos el mismo ID para liga
    }
    
    equipos.append(nuevo_equipo)
    
    if guardar_datos(ARCHIVO_EQUIPOS, equipos):
        print(f"\n✅ Equipo '{nombre}' registrado con ID {nuevo_id}")
    else:
        print("\n❌ Error al guardar el equipo")

def editar_equipo():
    """Edita un equipo existente con confirmación"""
    equipos = cargar_datos(ARCHIVO_EQUIPOS)
    
    if not equipos:
        print("\nNo hay equipos registrados para editar")
        return
    
    listar_equipos()
    
    try:
        equipo_id = int(input("\nID del equipo a editar: "))
    except ValueError:
        print("\nError: ID debe ser un número entero")
        return
    
    equipo = next((e for e in equipos if e['id'] == equipo_id), None)
    if not equipo:
        print("\nError: No se encontró el equipo con ese ID")
        return
    
    print("\n=== EDITANDO EQUIPO ===")
    print(f"1. Nombre: {equipo['nombre']}")
    print(f"2. Fundación: {equipo['fundacion']}")
    print(f"3. País: {equipo['pais']}")
    print(f"4. Liga ID: {equipo['liga_id']}")
    
    cambios = {}
    
    # Editar nombre
    nuevo_nombre = input("\nNuevo nombre (dejar vacío para mantener): ").strip()
    if nuevo_nombre:
        if any(e['nombre'].lower() == nuevo_nombre.lower() and e['id'] != equipo_id for e in equipos):
            print("Error: Ya existe un equipo con ese nombre")
        else:
            cambios['nombre'] = nuevo_nombre
    
    # Editar fundación
    nueva_fundacion = input("Nuevo año de fundación (dejar vacío para mantener): ").strip()
    if nueva_fundacion:
        if validar_fecha(nueva_fundacion + "-01-01") and 1800 < int(nueva_fundacion) <= datetime.now().year:
            cambios['fundacion'] = nueva_fundacion
        else:
            print("Error: Año de fundación inválido")
    
    # Editar país
    nuevo_pais = input("Nuevo país (dejar vacío para mantener): ").strip()
    if nuevo_pais:
        cambios['pais'] = nuevo_pais
    
    # Editar liga ID
    nueva_liga = input("Nuevo ID de liga (dejar vacío para mantener): ").strip()
    if nueva_liga:
        try:
            cambios['liga_id'] = int(nueva_liga)
        except ValueError:
            print("Error: ID de liga debe ser un número")
    
    if cambios:
        confirmacion = input("\n¿Confirmar cambios? (s/n): ").lower()
        if confirmacion == 's':
            equipo.update(cambios)
            if guardar_datos(ARCHIVO_EQUIPOS, equipos):
                print("\n✅ Equipo actualizado correctamente")
            else:
                print("\n❌ Error al guardar los cambios")
        else:
            print("\n⚠️ Cambios cancelados")
    else:
        print("\n⚠️ No se realizaron cambios")

def eliminar_equipo():
    """Elimina un equipo con confirmación"""
    equipos = cargar_datos(ARCHIVO_EQUIPOS)
    
    if not equipos:
        print("\nNo hay equipos registrados para eliminar")
        return
    
    listar_equipos()
    
    try:
        equipo_id = int(input("\nID del equipo a eliminar: "))
    except ValueError:
        print("\nError: ID debe ser un número entero")
        return
    
    equipo = next((e for e in equipos if e['id'] == equipo_id), None)
    if not equipo:
        print("\nError: No se encontró el equipo con ese ID")
        return
    
    print(f"\nEquipo a eliminar: {equipo['nombre']} (ID: {equipo['id']})")
    confirmacion = input("¿Está seguro que desea eliminar este equipo? (s/n): ").lower()
    
    if confirmacion == 's':
        equipos = [e for e in equipos if e['id'] != equipo_id]
        if guardar_datos(ARCHIVO_EQUIPOS, equipos):
            print("\n✅ Equipo eliminado correctamente")
        else:
            print("\n❌ Error al eliminar el equipo")