# Sistema de Gestión de Torneos Deportivos ⚽🏆
### Proyecto desarrollado por Wendy Angélica Vega Sánchez  
### Grupo J3 | Correo: wendyangelicavegasanchez@gmail.com

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Status](https://img.shields.io/badge/Estado-Activo-brightgreen.svg)
![License](https://img.shields.io/badge/Licencia-Academica-yellow.svg)

## Tabla de Contenidos 📑
1. [Descripción](#descripción-)
2. [Características](#características-principales-)
3. [Tecnologías](#tecnologías-)
4. [Instalación](#instalación-)
6. [Estructura](#estructura-del-proyecto-)
7. [Validaciones](#validaciones-implementadas-)
8. [Contacto](#contacto-)

## Descripción 📝
Sistema completo para la administración de torneos deportivos desarrollado como proyecto académico para el Grupo J3. Permite gestionar equipos, jugadores, cuerpo técnico, partidos y estadísticas.

## Características Principales ✨
| Módulo | Funcionalidades |
|--------|----------------|
| Equipos | Registro, edición, eliminación y listado |
| Jugadores | Gestión completa con validación de dorsales |
| Técnicos | Administración de roles y equipos |
| Torneos | Creación, programación de partidos y seguimiento |
| Estadísticas | Reportes detallados y análisis |

## Tecnologías 💻
- Python 3.12.1
- Estructura modular
- Almacenamiento en JSON
- Interfaz de consola interactiva

## Instalación 🛠️
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/torneo-j3.git

# Navegar al directorio
cd torneo-j3

# Ejecutar el sistema
python main.py
Uso 🖥️
python
=== MENÚ PRINCIPAL ===
1. Gestión de Equipos
2. Gestión de Jugadores
3. Cuerpo Técnico
4. Torneos y Partidos
5. Estadísticas
6. Salir
# # Estructura del Proyecto 🌐
text
torneo-j3/
├── data/
│   ├── equipos.json       # Datos de equipos
│   ├── jugadores.json     # Registro de jugadores
│   └── torneos.json       # Información de torneos
├── src/
│   ├── core/              # Módulos principales
│   │   ├── equipos.py
│   │   ├── jugadores.py
│   │   └── torneos.py
│   └── utils/             # Utilidades
│       ├── file_manager.py
│       └── validators.py
└── main.py                # Punto de entrada
# # Validaciones Implementadas ✅
Datos obligatorios: Campos requeridos en todos los formularios

Formatos específicos:

Fechas (YYYY-MM-DD)

Horas (HH:MM)

Lógica de negocio:

Dorsales únicos por equipo

No conflictos en horarios de partidos

Mínimo 2 equipos por torneo


# # Contacto 📧
Wendy Angélica Vega Sánchez
📧 wendyangelicavegasanchez@gmail.com
📚 Grupo J3
📅 Julio 2023

