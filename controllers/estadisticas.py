from utils.helpers import cargar_datos
from collections import defaultdict

ARCHIVO_EQUIPOS = "data/equipos.json"
ARCHIVO_JUGADORES = "data/jugadores.json"
ARCHIVO_TORNEOS = "data/torneos.json"
ARCHIVO_PARTIDOS = "data/partidos.json"

def estadisticas_equipos():
    """
    Genera y muestra estadísticas detalladas de todos los equipos
    Retorna: Lista de diccionarios con las estadísticas de cada equipo
    """
    equipos = cargar_datos(ARCHIVO_EQUIPOS)
    partidos = cargar_datos(ARCHIVO_PARTIDOS)
    jugadores = cargar_datos(ARCHIVO_JUGADORES)
    
    if not equipos or not partidos:
        print("\nNo hay suficientes datos para generar estadísticas de equipos")
        return []
    
    # Inicializar estadísticas
    stats = {}
    for equipo in equipos:
        stats[equipo['id']] = {
            'nombre': equipo['nombre'],
            'pj': 0, 'pg': 0, 'pe': 0, 'pp': 0,
            'gf': 0, 'gc': 0, 'dg': 0,
            'jugadores': 0,
            'victorias_local': 0,
            'victorias_visitante': 0
        }
    
    # Procesar partidos
    for partido in partidos:
        if partido['resultado'] is None:
            continue
            
        local = partido['local_id']
        visitante = partido['visitante_id']
        goles_l = partido['goles_local']
        goles_v = partido['goles_visitante']
        
        # Estadísticas básicas
        stats[local]['pj'] += 1
        stats[visitante]['pj'] += 1
        stats[local]['gf'] += goles_l
        stats[local]['gc'] += goles_v
        stats[visitante]['gf'] += goles_v
        stats[visitante]['gc'] += goles_l
        
        # Resultados
        if goles_l > goles_v:
            stats[local]['pg'] += 1
            stats[local]['victorias_local'] += 1
            stats[visitante]['pp'] += 1
        elif goles_v > goles_l:
            stats[visitante]['pg'] += 1
            stats[visitante]['victorias_visitante'] += 1
            stats[local]['pp'] += 1
        else:
            stats[local]['pe'] += 1
            stats[visitante]['pe'] += 1
    
    # Calcular diferencia de goles y jugadores por equipo
    for eq_id, eq_data in stats.items():
        eq_data['dg'] = eq_data['gf'] - eq_data['gc']
        eq_data['jugadores'] = sum(1 for j in jugadores if j['equipo_id'] == eq_id) if jugadores else 0
    
    # Convertir a lista ordenada
    estadisticas_ordenadas = sorted(stats.values(), 
                                  key=lambda x: (x['pg']*3 + x['pe'], x['dg'], x['gf']), 
                                  reverse=True)
    
    return estadisticas_ordenadas

def estadisticas_jugadores():
    """
    Genera y muestra estadísticas detalladas de todos los jugadores
    Retorna: Lista de diccionarios con las estadísticas de cada jugador
    """
    jugadores = cargar_datos(ARCHIVO_JUGADORES)
    equipos = cargar_datos(ARCHIVO_EQUIPOS)
    
    if not jugadores:
        print("\nNo hay jugadores registrados")
        return []
    
    stats = []
    for jugador in jugadores:
        equipo_nombre = next((e['nombre'] for e in equipos if e['id'] == jugador['equipo_id']), "Desconocido")
        stats.append({
            'id': jugador['id'],
            'nombre': jugador['nombre'],
            'equipo': equipo_nombre,
            'posicion': jugador['posicion'],
            'dorsal': jugador['dorsal'],
            'goles': jugador.get('goles', 0),
            'asistencias': jugador.get('asistencias', 0),
            'tarjetas_amarillas': jugador.get('tarjetas_amarillas', 0),
            'tarjetas_rojas': jugador.get('tarjetas_rojas', 0),
            'ratio_gol': jugador.get('goles', 0) / jugador.get('partidos_jugados', 1) if jugador.get('partidos_jugados', 0) > 0 else 0
        })
    
    return sorted(stats, key=lambda x: x['goles'], reverse=True)

def estadisticas_torneos():
    """
    Genera y muestra estadísticas detalladas de todos los torneos
    Retorna: Lista de diccionarios con las estadísticas de cada torneo
    """
    torneos = cargar_datos(ARCHIVO_TORNEOS)
    partidos = cargar_datos(ARCHIVO_PARTIDOS)
    
    if not torneos:
        print("\nNo hay torneos registrados")
        return []
    
    stats = []
    for torneo in torneos:
        partidos_torneo = [p for p in partidos if p.get('torneo_id') == torneo['id']]
        partidos_jugados = [p for p in partidos_torneo if p.get('resultado') is not None]
        
        stats.append({
            'id': torneo['id'],
            'nombre': torneo['nombre'],
            'tipo': torneo['tipo'],
            'equipos': len(torneo.get('equipos', [])),
            'partidos_programados': len(partidos_torneo),
            'partidos_jugados': len(partidos_jugados),
            'porcentaje_completado': (len(partidos_jugados) / len(partidos_torneo)) * 100 if partidos_torneo else 0,
            'goles_totales': sum(p['goles_local'] + p['goles_visitante'] for p in partidos_jugados),
            'promedio_goles': (sum(p['goles_local'] + p['goles_visitante'] for p in partidos_jugados) / len(partidos_jugados)) if partidos_jugados else 0
        })
    
    return sorted(stats, key=lambda x: x['porcentaje_completado'], reverse=True)

def mostrar_estadisticas_equipos():
    """Muestra en consola las estadísticas de equipos formateadas"""
    stats = estadisticas_equipos()
    if not stats:
        return
    
    print("\n=== ESTADÍSTICAS DE EQUIPOS ===")
    print("{:<25} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4}".format(
        'Equipo', 'PJ', 'PG', 'PE', 'PP', 'GF', 'GC', 'DG', 'Jug', 'VL', 'VV'))
    print("-" * 85)
    
    for eq in stats:
        print("{:<25} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4} {:<4}".format(
            eq['nombre'], eq['pj'], eq['pg'], eq['pe'], eq['pp'], 
            eq['gf'], eq['gc'], eq['dg'], eq['jugadores'],
            eq['victorias_local'], eq['victorias_visitante']))

def mostrar_estadisticas_jugadores():
    """Muestra en consola las estadísticas de jugadores formateadas"""
    stats = estadisticas_jugadores()
    if not stats:
        return
    
    print("\n=== ESTADÍSTICAS DE JUGADORES ===")
    print("{:<5} {:<25} {:<20} {:<15} {:<6} {:<5} {:<5} {:<4} {:<4} {:<6}".format(
        'ID', 'Nombre', 'Equipo', 'Posición', 'Dorsal', 'Goles', 'Asis', 'TA', 'TR', 'Ratio'))
    print("-" * 105)
    
    for jug in stats:
        print("{:<5} {:<25} {:<20} {:<15} {:<6} {:<5} {:<5} {:<4} {:<4} {:<6.2f}".format(
            jug['id'], jug['nombre'], jug['equipo'], jug['posicion'], 
            jug['dorsal'], jug['goles'], jug['asistencias'], 
            jug['tarjetas_amarillas'], jug['tarjetas_rojas'], jug['ratio_gol']))

def mostrar_estadisticas_torneos():
    """Muestra en consola las estadísticas de torneos formateadas"""
    stats = estadisticas_torneos()
    if not stats:
        return
    
    print("\n=== ESTADÍSTICAS DE TORNEOS ===")
    print("{:<5} {:<25} {:<15} {:<7} {:<7} {:<7} {:<10} {:<7} {:<7}".format(
        'ID', 'Nombre', 'Tipo', 'Equipos', 'P Prog', 'P Jug', '% Compl', 'Goles', 'Prom'))
    print("-" * 105)
    
    for t in stats:
        print("{:<5} {:<25} {:<15} {:<7} {:<7} {:<7} {:<10.1f} {:<7} {:<7.2f}".format(
            t['id'], t['nombre'], t['tipo'], t['equipos'], 
            t['partidos_programados'], t['partidos_jugados'],
            t['porcentaje_completado'], t['goles_totales'],
            t['promedio_goles']))