from utils.screenControllers import limpiar_pantalla, pausar_pantalla
from controllers.equipo import (
    listar_equipos,
    crear_equipo,
    editar_equipo,
    eliminar_equipo
)
from controllers.jugadores import (
    listar_jugadores,
    crear_jugador,
    editar_jugador,
    eliminar_jugador
)
from controllers.transferencias import (
    ver_estadisticas,
    registrar_transferencia,
    editar_transferencia,
    eliminar_transferencia
)
from controllers.tecnicos import (
    listar_tecnicos,
    crear_tecnico,
    editar_tecnico,
    eliminar_tecnico
)
from controllers.torneos import (
    listar_torneos,
    crear_torneo,
    programar_partido,
    listar_partidos
)
from controllers.estadisticas import (
    mostrar_estadisticas_equipos_completas,
    mostrar_estadisticas_jugadores_detalladas,
    mostrar_maximos_goleadores,
    mostrar_resumen_torneos,
    mostrar_comparativa_equipos

)
from utils.menus import (
    menu_principal,
    menu_equipos,
    menu_jugadores,
    menu_transferencias,
    menu_tecnicos,
    menu_torneos,
    menu_estadisticas

)

def main():
    while True:
        limpiar_pantalla()
        print(menu_principal)
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":  # Menú equipos
            while True:
                limpiar_pantalla()
                print(menu_equipos)
                opcion = input("Seleccione una opción: ").strip()

                if opcion == "1":
                    listar_equipos()
                elif opcion == "2":
                    crear_equipo()
                elif opcion == "3":
                    editar_equipo()
                elif opcion == "4":
                    eliminar_equipo()
                elif opcion == "5":
                    break
                else:
                    print("Opción inválida. Intente de nuevo.")
                
                pausar_pantalla()

        elif opcion == "2":  # Menú jugadores
            while True:
                limpiar_pantalla()
                print(menu_jugadores)
                opcion = input("Seleccione una opción: ").strip()

                if opcion == "1":
                    listar_jugadores()
                elif opcion == "2":
                    crear_jugador()
                elif opcion == "3":
                    editar_jugador()
                elif opcion == "4":
                    eliminar_jugador()
                elif opcion == "5":
                    break
                else:
                    print("Opción inválida. Intente de nuevo.")
                
                pausar_pantalla()

        elif opcion == "3":  # Menú técnicos
            while True:
                limpiar_pantalla()
                print(menu_tecnicos)
                opcion = input("Seleccione una opción: ").strip()

                if opcion == "1":
                    listar_tecnicos()
                elif opcion == "2":
                    crear_tecnico()
                elif opcion == "3":
                    editar_tecnico()
                elif opcion == "4":
                    eliminar_tecnico()
                elif opcion == "5":
                    break
                else:
                    print("Opción inválida. Intente de nuevo.")
                
                pausar_pantalla()
        
        elif opcion == "4":  # Menú transferencias
            while True:
                limpiar_pantalla()
                print(menu_transferencias)
                opcion = input("Seleccione una opción: ").strip()

                if opcion == "1":
                    registrar_transferencia()
                elif opcion == "2":
                    editar_transferencia()
                elif opcion == "3":
                    eliminar_transferencia()
                elif opcion == "4":
                    break
                else:
                    print("Opción inválida. Intente de nuevo.")
                
                pausar_pantalla()

        elif opcion == "5":  # Menú transferencias
            while True:
                limpiar_pantalla()
                print(menu_torneos)
                opcion = input("Seleccione una opción: ").strip()

                if opcion == "1":
                    listar_torneos()
                elif opcion == "2":
                    crear_torneo()
                elif opcion == "3":
                    programar_partido()
                elif opcion == "4":
                    listar_partidos()
                elif opcion == "5":
                    break
                else:
                    print("Opción inválida. Intente de nuevo.")
                
                pausar_pantalla()

        elif opcion == "6":  # Menú transferencias
            while True:
                limpiar_pantalla()
                print(menu_estadisticas)
                opcion = input("Seleccione una opción: ").strip()

                if opcion == "1":
                    mostrar_estadisticas_equipos_completas()
                elif opcion == "2":
                    mostrar_estadisticas_jugadores_detalladas()
                elif opcion == "3":
                    mostrar_maximos_goleadores()
                elif opcion == "4":
                    mostrar_resumen_torneos()
                elif opcion == "5":
                    mostrar_comparativa_equipos()
                elif opcion == "6":
                    break
                else:
                    print("Opción inválida. Intente de nuevo.")
                
                pausar_pantalla()

        elif opcion == "7":
            print("Saliendo del programa...")
            break

        else:
            print("Opción inválida. Intente de nuevo.")
            pausar_pantalla()

if __name__ == "__main__":
    main()