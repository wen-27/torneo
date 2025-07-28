import os
import json
from datetime import datetime

# Constantes
ARCHIVO_EQUIPOS = "data/equipos.json"
ARCHIVO_JUGADORES = "data/jugadores.json"
ARCHIVO_TORNEOS = "data/torneos.json"
ARCHIVO_PARTIDOS = "data/partidos.json"

def cargar_datos(archivo):
    """Carga datos desde un archivo JSON"""
    if not os.path.exists(archivo):
        return []
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def mostrar_estadisticas_equipos_completas():
    """Muestra estadísticas extendidas de equipos"""
    equipos = cargar_datos(ARCHIVO_EQUIPOS)
    partidos = cargar_datos(ARCHIVO_PARTIDOS)
    
    if not equipos or not partidos:
        print("\nNo hay suficientes datos para generar estadísticas")
        return
    
    print("\n📊 ESTADÍSTICAS COMPLETAS DE EQUIPOS")
    print("="*90)
    print(f"{'Equipo':<20} | {'PJ':<4} | {'PG':<4} | {'PE':<4} | {'PP':<4} | {'GF':<4} | {'GC':<4} | {'DG':<4} | {'Efectividad':<10}")
    print("-"*90)
    
    for equipo in equipos:
        stats = calcular_estadisticas_equipo(equipo['id'], partidos)
        efectividad = (stats['pg']*3 + stats['pe']) / (stats['pj']*3) * 100 if stats['pj'] > 0 else 0
        
        print(f"{equipo['nombre'][:19]:<20} | {stats['pj']:<4} | {stats['pg']:<4} | "
              f"{stats['pe']:<4} | {stats['pp']:<4} | {stats['gf']:<4} | {stats['gc']:<4} | "
              f"{stats['gf']-stats['gc']:<4} | {efectividad:.1f}%")

def calcular_estadisticas_equipo(equipo_id, partidos):
    """Calcula estadísticas para un equipo específico"""
    stats = {'pj':0, 'pg':0, 'pe':0, 'pp':0, 'gf':0, 'gc':0}
    
    for partido in partidos:
        if partido['resultado'] is None:
            continue
            
        if partido['local_id'] == equipo_id:
            stats['pj'] += 1
            stats['gf'] += partido['goles_local']
            stats['gc'] += partido['goles_visitante']
            
            if partido['goles_local'] > partido['goles_visitante']:
                stats['pg'] += 1
            elif partido['goles_local'] == partido['goles_visitante']:
                stats['pe'] += 1
            else:
                stats['pp'] += 1
                
        elif partido['visitante_id'] == equipo_id:
            stats['pj'] += 1
            stats['gf'] += partido['goles_visitante']
            stats['gc'] += partido['goles_local']
            
            if partido['goles_visitante'] > partido['goles_local']:
                stats['pg'] += 1
            elif partido['goles_visitante'] == partido['goles_local']:
                stats['pe'] += 1
            else:
                stats['pp'] += 1
                
    return stats

def mostrar_estadisticas_jugadores_detalladas():
    """Muestra estadísticas avanzadas de jugadores"""
    jugadores = cargar_datos(ARCHIVO_JUGADORES)
    equipos = cargar_datos(ARCHIVO_EQUIPOS)
    
    if not jugadores:
        print("\nNo hay jugadores registrados")
        return
    
    # Ordenar por goles y luego por asistencias
    jugadores_ordenados = sorted(
        jugadores,
        key=lambda x: (x.get('goles', 0), x.get('asistencias', 0)),
        reverse=True
    )
    
    print("\n⚽ ESTADÍSTICAS DETALLADAS DE JUGADORES")
    print("="*120)
    print(f"{'Nombre':<20} | {'Equipo':<20} | {'Posición':<15} | {'Goles':<6} | {'Asist.':<6} | {'TA':<3} | {'TR':<3} | {'Ratio Gol/Part.':<15}")
    print("-"*120)
    
    for jugador in jugadores_ordenados[:20]:  # Mostrar solo los 20 primeros
        equipo_nombre = next(
            (e['nombre'] for e in equipos if e['id'] == jugador['equipo_id']),
            "Desconocido"
        )
        ratio = jugador.get('goles', 0) / jugador.get('partidos_jugados', 1) if jugador.get('partidos_jugados', 0) > 0 else 0
        
        print(
            f"{jugador['nombre'][:19]:<20} | {equipo_nombre[:19]:<20} | "
            f"{jugador['posicion'][:14]:<15} | {jugador.get('goles', 0):<6} | "
            f"{jugador.get('asistencias', 0):<6} | {jugador.get('tarjetas_amarillas', 0):<3} | "
            f"{jugador.get('tarjetas_rojas', 0):<3} | {ratio:.2f}"
        )

def mostrar_maximos_goleadores():
    """Muestra ranking de goleadores y asistentes"""
    jugadores = cargar_datos(ARCHIVO_JUGADORES)
    
    if not jugadores:
        print("\nNo hay jugadores registrados")
        return
    
    goleadores = sorted(jugadores, key=lambda x: x.get('goles', 0), reverse=True)[:10]
    asistentes = sorted(jugadores, key=lambda x: x.get('asistencias', 0), reverse=True)[:10]
    
    print("\n🏆 TOP 10 GOLEADORES")
    print("="*60)
    for i, jug in enumerate(goleadores, 1):
        print(f"{i}. {jug['nombre'][:25]:<25} - {jug.get('goles', 0)} goles")
    
    print("\n🎯 TOP 10 ASISTENTES")
    print("="*60)
    for i, jug in enumerate(asistentes, 1):
        print(f"{i}. {jug['nombre'][:25]:<25} - {jug.get('asistencias', 0)} asistencias")

def mostrar_resumen_torneos():
    """Muestra resumen de todos los torneos"""
    torneos = cargar_datos(ARCHIVO_TORNEOS)
    partidos = cargar_datos(ARCHIVO_PARTIDOS)
    
    if not torneos:
        print("\nNo hay torneos registrados")
        return
    
    print("\n🏅 RESUMEN DE TORNEOS")
    print("="*90)
    print(f"{'Torneo':<25} | {'Equipos':<7} | {'Partidos':<8} | {'Completado':<10} | {'Goles Tot.':<9} | {'Prom. Gol':<9}")
    print("-"*90)
    
    for torneo in torneos:
        partidos_torneo = [p for p in partidos if p.get('torneo_id') == torneo['id']]
        partidos_jugados = [p for p in partidos_torneo if p.get('resultado') is not None]
        goles = sum(p['goles_local'] + p['goles_visitante'] for p in partidos_jugados)
        promedio = goles / len(partidos_jugados) if partidos_jugados else 0
        
        print(
            f"{torneo['nombre'][:24]:<25} | {len(torneo.get('equipos', [])):<7} | "
            f"{len(partidos_torneo):<8} | {len(partidos_jugados)/len(partidos_torneo)*100 if partidos_torneo else 0:.1f}%{'':<6} | "
            f"{goles:<9} | {promedio:.2f}"
        )

def mostrar_comparativa_equipos():
    """Muestra comparativa entre equipos"""
    equipos = cargar_datos(ARCHIVO_EQUIPOS)
    partidos = cargar_datos(ARCHIVO_PARTIDOS)
    
    if len(equipos) < 2:
        print("\nSe necesitan al menos 2 equipos para comparar")
        return
    
    print("\n🔍 COMPARATIVA ENTRE EQUIPOS")
    
    # Mostrar lista de equipos
    for i, equipo in enumerate(equipos, 1):
        print(f"{i}. {equipo['nombre']}")
    
    # Seleccionar equipos a comparar
    try:
        opciones = input("\nSeleccione 2 equipos (ej: 1 3): ").split()
        if len(opciones) != 2:
            raise ValueError
        
        idx1, idx2 = map(int, opciones)
        equipo1 = equipos[idx1-1]
        equipo2 = equipos[idx2-1]
        
        # Comparar
        print(f"\n🆚 COMPARANDO: {equipo1['nombre']} vs {equipo2['nombre']}")
        
        # Buscar partidos entre estos equipos
        enfrentamientos = [
            p for p in partidos 
            if {p['local_id'], p['visitante_id']} == {equipo1['id'], equipo2['id']}
            and p['resultado'] is not None
        ]
        
        if not enfrentamientos:
            print("No hay partidos jugados entre estos equipos")
            return
            
        print(f"\n📅 Total enfrentamientos: {len(enfrentamientos)}")
        
        # Calcular resultados
        victorias_equipo1 = 0
        victorias_equipo2 = 0
        empates = 0
        
        for p in enfrentamientos:
            if p['goles_local'] > p['goles_visitante']:
                if p['local_id'] == equipo1['id']:
                    victorias_equipo1 += 1
                else:
                    victorias_equipo2 += 1
            elif p['goles_visitante'] > p['goles_local']:
                if p['visitante_id'] == equipo1['id']:
                    victorias_equipo1 += 1
                else:
                    victorias_equipo2 += 1
            else:
                empates += 1
        
        print(f"\n🏆 Victorias: {equipo1['nombre']}: {victorias_equipo1} | {equipo2['nombre']}: {victorias_equipo2} | Empates: {empates}")
        
    except (ValueError, IndexError):
        print("\n❌ Selección inválida. Debe ingresar 2 números válidos")