Sistema de Gestión de Torneos Deportivos ⚽🏆
Proyecto desarrollado por Wendy Angélica Vega Sánchez
Grupo J3 | 📧 Correo: wendyangelicavegasanchez@gmail.com

https://img.shields.io/badge/Python-3.12+-blue.svg
https://img.shields.io/badge/Estado-Activo-brightgreen.svg
https://img.shields.io/badge/Licencia-Acad%C3%A9mica-yellow.svg

📑 Tabla de Contenidos
Descripción

Características

Tecnologías

Instalación

Uso

Estructura

Validaciones

Capturas

Contacto

📝 Descripción
Sistema completo para la administración de torneos deportivos desarrollado como proyecto académico para el Grupo J3. Permite gestionar equipos, jugadores, cuerpo técnico, partidos y estadísticas de manera integrada.

✨ Características Principales
Gestión de Equipos
Registro de nuevos equipos

Edición de información existente

Eliminación de equipos

Listado completo con filtros

Administración de Jugadores
Alta/baja de jugadores

Asignación de dorsales

Control por equipos

Estadísticas individuales

Cuerpo Técnico
Registro de entrenadores

Asignación de roles

Vinculación con equipos

Gestión de contrataciones

💻 Tecnologías
Python 3.12.1: Lenguaje principal

JSON: Almacenamiento de datos

POO: Programación Orientada a Objetos

CLI: Interfaz de línea de comandos

🛠️ Instalación
Clonar repositorio:

bash
git clone https://github.com/tu-usuario/torneo-j3.git
cd torneo-j3
Ejecutar el sistema:

bash
python main.py
🖥️ Uso
El sistema muestra un menú interactivo:

text
=== MENÚ PRINCIPAL ===
1. Gestión de Equipos
2. Jugadores
3. Cuerpo Técnico
4. Torneos
5. Partidos
6. Estadísticas
7. Salir
Seleccione opción:
🌐 Estructura del Proyecto
text
torneo-j3/
├── data/
│   ├── equipos.json
│   ├── jugadores.json
│   └── torneos.json
├── src/
│   ├── core/
│   │   ├── equipos.py
│   │   ├── jugadores.py
│   │   └── torneos.py
│   └── utils/
│       ├── file_manager.py
│       └── validators.py
└── main.py
✅ Validaciones Implementadas
Datos Obligatorios
Nombre de equipos

Fechas de nacimiento

Números de dorsal

Formatos Específicos
Campo	Formato
Fecha	YYYY-MM-DD
Hora	HH:MM
Dorsal	Número entero
Reglas de Negocio
Máximo 25 jugadores por equipo

No duplicación de dorsales

Validación de fechas (inicio < fin)

📸 Capturas de Pantalla
(Espacio para agregar imágenes del sistema en funcionamiento)

📧 Contacto
Wendy Angélica Vega Sánchez
📧 wendyangelicavegasanchez@gmail.com
📚 Grupo J3
🏫 Institución Educativa
📅 Julio 2023

