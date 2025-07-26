# controllers/transferencias.py
import json
import os
from datetime import datetime
from controllers.equipo import listar_equipos
from controllers.jugadores import crear_jugador, listar_jugadores

archivo_transferencias = "transferencias.json"

def cargar_transferencias():
    """Carga todas las transferencias desde el archivo"""
    if not os.path.exists(archivo_transferencias):
        return []
    
    try:
        with open(archivo_transferencias, "r", encoding="utf-8") as file:
            content = file.read()
            return json.loads(content) if content.strip() else []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al cargar transferencias: {str(e)}")
        return []

def guardar_transferencias(transferencias):
    """Guarda las transferencias en el archivo JSON"""
    try:
        with open(archivo_transferencias, "w", encoding="utf-8") as file:
            json.dump(transferencias, file, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error al guardar transferencias: {str(e)}")
        return False

def ver_estadisticas():
    """Muestra estadísticas generales del sistema"""
    equipos = listar_equipos()
    jugadores = crear_jugador()
    transferencias = cargar_transferencias()
    
    print("\n" + "="*50)
    print("        ESTADÍSTICAS DEL TORNEO")
    print("="*50)
    
    print(f"📊 Total de equipos registrados: {len(equipos)}")
    print(f"👤 Total de jugadores registrados: {len(jugadores)}")
    print(f"🔄 Total de transferencias realizadas: {len(transferencias)}")
    
    if equipos:
        # Estadísticas por país
        paises = {}
        for equipo in equipos:
            pais = equipo['pais']
            paises[pais] = paises.get(pais, 0) + 1
        
        print(f"\n🌍 Equipos por país:")
        for pais, cantidad in sorted(paises.items()):
            print(f"   • {pais}: {cantidad} equipo(s)")
    
    if jugadores:
        # Estadísticas por posición
        posiciones = {}
        for jugador in jugadores:
            pos = jugador['posicion']
            posiciones[pos] = posiciones.get(pos, 0) + 1
        
        print(f"\n⚽ Jugadores por posición:")
        for posicion, cantidad in sorted(posiciones.items()):
            print(f"   • {posicion}: {cantidad} jugador(es)")
    
    if transferencias:
        # Transferencias por tipo
        tipos = {}
        for transfer in transferencias:
            tipo = transfer['tipo_transferencia']
            tipos[tipo] = tipos.get(tipo, 0) + 1
        
        print(f"\n🔄 Transferencias por tipo:")
        for tipo, cantidad in sorted(tipos.items()):
            print(f"   • {tipo}: {cantidad} transferencia(s)")
    
    print("="*50)

def registrar_transferencia():
    """Registra una nueva transferencia de jugador"""
    jugadores = crear_jugador()
    equipos = listar_equipos()
    transferencias = cargar_transferencias()
    
    if not jugadores:
        print("❌ No hay jugadores registrados")
        return
    
    if not equipos:
        print("❌ No hay equipos registrados")
        return
    
    print("\n--- REGISTRAR TRANSFERENCIA ---")
    
    # Mostrar jugadores disponibles
    print("\nJugadores disponibles:")
    print(f"{'ID':<5} {'Nombre':<25} {'Posición':<15} {'Equipo ID':<10}")
    print("-" * 60)
    for jugador in jugadores:
        print(f"{jugador['id']:<5} {jugador['nombre']:<25} {jugador['posicion']:<15} {jugador['equipo_id']:<10}")
    
    # Seleccionar jugador
    while True:
        try:
            jugador_id = int(input("\nID del jugador a transferir: "))
            jugador = next((j for j in jugadores if j['id'] == jugador_id), None)
            if jugador:
                break
            print("❌ Jugador no encontrado")
        except ValueError:
            print("❌ Debe ingresar un número válido")
    
    # Mostrar equipos disponibles
    print(f"\nEquipo actual: {jugador['equipo_id']}")
    print("\nEquipos disponibles para transferencia:")
    equipos_disponibles = [e for e in equipos if e['id'] != jugador['equipo_id']]
    
    if not equipos_disponibles:
        print("❌ No hay otros equipos disponibles")
        return
    
    for equipo in equipos_disponibles:
        print(f"{equipo['id']}: {equipo['nombre']} ({equipo['pais']})")
    
    # Seleccionar equipo destino
    while True:
        try:
            equipo_destino_id = int(input("\nID del equipo destino: "))
            equipo_destino = next((e for e in equipos if e['id'] == equipo_destino_id), None)
            if equipo_destino and equipo_destino['id'] != jugador['equipo_id']:
                break
            print("❌ Equipo no válido o es el mismo equipo actual")
        except ValueError:
            print("❌ Debe ingresar un número válido")
    
    # Seleccionar tipo de transferencia
    tipos_validos = ["Venta", "Préstamo", "Intercambio", "Traspaso libre"]
    print(f"\nTipos de transferencia disponibles:")
    for i, tipo in enumerate(tipos_validos, 1):
        print(f"{i}. {tipo}")
    
    while True:
        try:
            tipo_idx = int(input("\nSeleccione tipo de transferencia (1-4): ")) - 1
            if 0 <= tipo_idx < len(tipos_validos):
                tipo_transferencia = tipos_validos[tipo_idx]
                break
            print("❌ Opción no válida")
        except ValueError:
            print("❌ Debe ingresar un número válido")
    
    # Confirmar transferencia
    print(f"\n--- CONFIRMACIÓN DE TRANSFERENCIA ---")
    print(f"Jugador: {jugador['nombre']}")
    print(f"Equipo origen: {jugador['equipo_id']}")
    print(f"Equipo destino: {equipo_destino['id']} - {equipo_destino['nombre']}")
    print(f"Tipo: {tipo_transferencia}")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d')}")
    
    confirmar = input("\n¿Confirmar transferencia? (s/n): ").lower()
    if confirmar == 's':
        # Crear registro de transferencia
        nuevo_id = max([t['id'] for t in transferencias], default=0) + 1
        
        nueva_transferencia = {
            "id": nuevo_id,
            "jugador_id": jugador['id'],
            "jugador_nombre": jugador['nombre'],
            "equipo_origen": jugador['equipo_id'],
            "equipo_destino": equipo_destino['id'],
            "tipo_transferencia": tipo_transferencia,
            "fecha": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Actualizar equipo del jugador
        jugador['equipo_id'] = equipo_destino['id']
        
        # Guardar cambios
        transferencias.append(nueva_transferencia)
        
        if guardar_transferencias(transferencias) and listar_jugadores(jugadores):
            print("✅ Transferencia registrada exitosamente")
        else:
            print("❌ Error al registrar la transferencia")
    else:
        print("⚠️ Transferencia cancelada")

def editar_transferencia():
    """Edita una transferencia existente"""
    transferencias = cargar_transferencias()
    
    if not transferencias:
        print("❌ No hay transferencias registradas")
        return
    
    print("\n--- TRANSFERENCIAS REGISTRADAS ---")
    print(f"{'ID':<5} {'Jugador':<20} {'Origen':<8} {'Destino':<8} {'Tipo':<15} {'Fecha':<12}")
    print("-" * 75)
    
    for transfer in transferencias:
        print(f"{transfer['id']:<5} {transfer['jugador_nombre']:<20} {transfer['equipo_origen']:<8} {transfer['equipo_destino']:<8} {transfer['tipo_transferencia']:<15} {transfer['fecha'][:10]:<12}")
    
    try:
        transfer_id = int(input("\nID de transferencia a editar: "))
    except ValueError:
        print("❌ Debe ingresar un número válido")
        return
    
    transfer = next((t for t in transferencias if t['id'] == transfer_id), None)
    if not transfer:
        print("❌ Transferencia no encontrada")
        return
    
    print(f"\nEditando transferencia:")
    print(f"1. Tipo actual: {transfer['tipo_transferencia']}")
    
    tipos_validos = ["Venta", "Préstamo", "Intercambio", "Traspaso libre"]
    print(f"\nTipos disponibles:")
    for i, tipo in enumerate(tipos_validos, 1):
        print(f"{i}. {tipo}")
    
    nuevo_tipo = input("\nNuevo tipo (dejar vacío para mantener): ").strip()
    if nuevo_tipo:
        try:
            tipo_idx = int(nuevo_tipo) - 1
            if 0 <= tipo_idx < len(tipos_validos):
                transfer['tipo_transferencia'] = tipos_validos[tipo_idx]
                
                if guardar_transferencias(transferencias):
                    print("✅ Transferencia actualizada")
                else:
                    print("❌ Error al actualizar")
            else:
                print("❌ Opción no válida")
        except ValueError:
            print("❌ Debe ingresar un número válido")

def eliminar_transferencia():
    """Elimina una transferencia del registro"""
    transferencias = cargar_transferencias()
    
    if not transferencias:
        print("❌ No hay transferencias registradas")
        return
    
    print("\n--- TRANSFERENCIAS REGISTRADAS ---")
    print(f"{'ID':<5} {'Jugador':<20} {'Origen':<8} {'Destino':<8} {'Tipo':<15} {'Fecha':<12}")
    print("-" * 75)
    
    for transfer in transferencias:
        print(f"{transfer['id']:<5} {transfer['jugador_nombre']:<20} {transfer['equipo_origen']:<8} {transfer['equipo_destino']:<8} {transfer['tipo_transferencia']:<15} {transfer['fecha'][:10]:<12}")
    
    try:
        transfer_id = int(input("\nID de transferencia a eliminar: "))
    except ValueError:
        print("❌ Debe ingresar un número válido")
        return
    
    transfer = next((t for t in transferencias if t['id'] == transfer_id), None)
    if not transfer:
        print("❌ Transferencia no encontrada")
        return
    
    print(f"\nTransferencia a eliminar:")
    print(f"Jugador: {transfer['jugador_nombre']}")
    print(f"Tipo: {transfer['tipo_transferencia']}")
    print(f"Fecha: {transfer['fecha']}")
    
    confirmar = input("\n¿Confirmar eliminación? (s/n): ").lower()
    if confirmar == 's':
        transferencias = [t for t in transferencias if t['id'] != transfer_id]
        
        if guardar_transferencias(transferencias):
            print("✅ Transferencia eliminada")
        else:
            print("❌ Error al eliminar")
    else:
        print("⚠️ Eliminación cancelada")
