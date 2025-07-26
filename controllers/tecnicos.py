import os
from datetime import datetime
from utils.helpers import cargar_datos, guardar_datos, obtener_ultimo_id
from utils.validators import validar_entero_positivo

ARCHIVO_TECNICOS = "data/tecnicos.json"
ARCHIVO_EQUIPOS = "data/equipos.json"

def listar_tecnicos():
    """Lista todos los miembros del cuerpo técnico"""
    tecnicos = cargar_datos(ARCHIVO_TECNICOS)
    equipos = cargar_datos(ARCHIVO_EQUIPOS)
    
    if not tecnicos:
        print("\nNo hay miembros del cuerpo técnico registrados")
        return []
    
    print("\n=== CUERPO TÉCNICO ===")
    print(f"{'ID':<5} {'Nombre':<25} {'Rol':<20} {'Equipo':<20} {'Nacionalidad':<15}")
    print("-" * 90)
    
    for tecnico in tecnicos:
        equipo_nombre = next((e['nombre'] for e in equipos if e['id'] == tecnico['equipo_id']), "Desconocido")
        print(f"{tecnico['id']:<5} {tecnico['nombre']:<25} {tecnico['rol']:<20} {equipo_nombre:<20} {tecnico['nacionalidad']:<15}")
    
    print(f"\nTotal: {len(tecnicos)} miembros")
    return tecnicos

def crear_tecnico():
    """Registra un nuevo miembro del cuerpo técnico"""
    tecnicos = cargar_datos(ARCHIVO_TECNICOS)
    equipos = cargar_datos(ARCHIVO_EQUIPOS)
    
    if not equipos:
        print("\nPrimero debe registrar equipos")
        return
    
    print("\n=== REGISTRAR NUEVO MIEMBRO ===")
    
    # Validación de nombre
    nombre = input("Nombre completo: ").strip()
    if not nombre:
        print("\nError: El nombre no puede estar vacío")
        return
    
    # Selección de rol
    roles = ["Entrenador", "Asistente", "Preparador físico", "Médico", "Utilero"]
    print("\nRoles disponibles:")
    for i, rol in enumerate(roles, 1):
        print(f"{i}. {rol}")
    
    while True:
        opcion = input("\nSeleccione el rol (1-5): ").strip()
        if not validar_entero_positivo(opcion) or int(opcion) < 1 or int(opcion) > 5:
            print("Error: Seleccione una opción válida (1-5)")
            continue
        rol = roles[int(opcion)-1]
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
        
        break
    
    # Nacionalidad
    nacionalidad = input("Nacionalidad: ").strip()
    if not nacionalidad:
        nacionalidad = "Desconocida"
    
    # Generar ID
    nuevo_id = obtener_ultimo_id(tecnicos) + 1
    
    nuevo_tecnico = {
        "id": nuevo_id,
        "nombre": nombre,
        "rol": rol,
        "equipo_id": equipo_id,
        "nacionalidad": nacionalidad,
        "fecha_ingreso": datetime.now().strftime("%Y-%m-%d")
    }
    
    tecnicos.append(nuevo_tecnico)
    
    if guardar_datos(ARCHIVO_TECNICOS, tecnicos):
        print(f"\n✅ {rol} '{nombre}' registrado con ID {nuevo_id}")
    else:
        print("\n❌ Error al guardar el miembro")

def editar_tecnico():
    """Edita un miembro del cuerpo técnico existente"""
    tecnicos = cargar_datos(ARCHIVO_TECNICOS)
    equipos = cargar_datos(ARCHIVO_EQUIPOS)
    
    if not tecnicos:
        print("\nNo hay miembros registrados para editar")
        return
    
    # Mostrar lista de técnicos
    print("\n=== EDITAR MIEMBRO DEL CUERPO TÉCNICO ===")
    listar_tecnicos()
    
    try:
        tecnico_id = int(input("\nIngrese el ID del miembro a editar: "))
    except ValueError:
        print("\nError: Debe ingresar un número válido")
        return
    
    # Buscar técnico
    tecnico = next((t for t in tecnicos if t['id'] == tecnico_id), None)
    if not tecnico:
        print("\nError: No se encontró miembro con ese ID")
        return
    
    print("\nDatos actuales del miembro:")
    print(f"1. Nombre: {tecnico['nombre']}")
    print(f"2. Rol: {tecnico['rol']}")
    print(f"3. Equipo ID: {tecnico['equipo_id']}")
    print(f"4. Nacionalidad: {tecnico['nacionalidad']}")
    
    # Procesar cambios
    cambios = {}
    
    # Editar nombre
    nuevo_nombre = input("\nNuevo nombre (dejar vacío para mantener actual): ").strip()
    if nuevo_nombre:
        cambios['nombre'] = nuevo_nombre
    
    # Editar rol
    roles = ["Entrenador", "Asistente", "Preparador físico", "Médico", "Utilero"]
    print("\nRoles disponibles:")
    for i, rol in enumerate(roles, 1):
        print(f"{i}. {rol}")
    
    nuevo_rol = input("\nNuevo rol (número 1-5, dejar vacío para mantener actual): ").strip()
    if nuevo_rol:
        try:
            opcion = int(nuevo_rol)
            if 1 <= opcion <= 5:
                cambios['rol'] = roles[opcion-1]
            else:
                print("Error: Opción fuera de rango")
        except ValueError:
            print("Error: Debe ingresar un número entre 1 y 5")
    
    # Editar equipo
    print("\nEquipos disponibles:")
    for equipo in equipos:
        print(f"{equipo['id']}: {equipo['nombre']}")
    
    nuevo_equipo = input("\nNuevo ID de equipo (dejar vacío para mantener actual): ").strip()
    if nuevo_equipo:
        try:
            equipo_id = int(nuevo_equipo)
            if equipo_id in [e['id'] for e in equipos]:
                cambios['equipo_id'] = equipo_id
            else:
                print("Error: ID de equipo no válido")
        except ValueError:
            print("Error: Debe ingresar un número válido")
    
    # Editar nacionalidad
    nueva_nacionalidad = input("Nueva nacionalidad (dejar vacío para mantener actual): ").strip()
    if nueva_nacionalidad:
        cambios['nacionalidad'] = nueva_nacionalidad
    
    # Aplicar cambios
    if cambios:
        confirmar = input("\n¿Confirmar cambios? (s/n): ").lower()
        if confirmar == 's':
            tecnico.update(cambios)
            if guardar_datos(ARCHIVO_TECNICOS, tecnicos):
                print("\n✅ Miembro actualizado correctamente")
            else:
                print("\n❌ Error al guardar cambios")
        else:
            print("\n⚠️ Cambios cancelados")
    else:
        print("\n⚠️ No se realizaron cambios")

def eliminar_tecnico():
    """Elimina un miembro del cuerpo técnico con confirmación"""
    tecnicos = cargar_datos(ARCHIVO_TECNICOS)
    
    if not tecnicos:
        print("\nNo hay miembros registrados para eliminar")
        return
    
    # Mostrar lista de técnicos
    print("\n=== ELIMINAR MIEMBRO DEL CUERPO TÉCNICO ===")
    listar_tecnicos()
    
    try:
        tecnico_id = int(input("\nIngrese el ID del miembro a eliminar: "))
    except ValueError:
        print("\nError: Debe ingresar un número válido")
        return
    
    # Buscar técnico
    tecnico = next((t for t in tecnicos if t['id'] == tecnico_id), None)
    if not tecnico:
        print("\nError: No se encontró miembro con ese ID")
        return
    
    # Confirmar eliminación
    print(f"\nDatos del miembro a eliminar:")
    print(f"Nombre: {tecnico['nombre']}")
    print(f"Rol: {tecnico['rol']}")
    print(f"Equipo ID: {tecnico['equipo_id']}")
    print(f"Nacionalidad: {tecnico['nacionalidad']}")
    
    confirmar = input("\n¿Está seguro que desea eliminar este miembro? (s/n): ").lower()
    if confirmar == 's':
        tecnicos = [t for t in tecnicos if t['id'] != tecnico_id]
        if guardar_datos(ARCHIVO_TECNICOS, tecnicos):
            print("\n✅ Miembro eliminado correctamente")
        else:
            print("\n❌ Error al eliminar miembro")
    else:
        print("\n⚠️ Eliminación cancelada")