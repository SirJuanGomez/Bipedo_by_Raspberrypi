from Servo import Servo
import time
import sys
import select

ARTICULACIONES_A_SERVO = {
    "pie_derecho": 0,
    "rodilla_derecha": 1,
    "muslo_derecho": 2,
    "cadera_derecha": 3,
    "hombro_derecho": 4,
    "codo_derecho": 5,
    "mano_derecha": 6,
    "cabeza": 7,
    "sin uso": 8,
    "mano_izquierda": 9,
    "codo_izquierdo": 10,
    "hombro_izquierdo": 11,
    "cadera_izquierda": 12,
    "muslo_izquierdo": 13,
    "rodilla_izquierda": 14,
    "pie_izquierdo": 15
}

robot = Servo()

def mover_articulaciones(movimientos, pausa=0.01):
    for articulacion, angulo in movimientos.items():
        canal = ARTICULACIONES_A_SERVO.get(articulacion)
        if canal is not None:
            robot.setServoAngle(canal, angulo)
        else:
            print(f"⚠️ Articulación '{articulacion}' no encontrada.")
    time.sleep(pausa)

def centrar_todo():
    mover_articulaciones({
        "muslo_derecho": 90,
        "rodilla_derecha": 90,
        "pie_derecho": 90,
        "muslo_izquierdo": 90,
        "rodilla_izquierda": 90,
        "pie_izquierdo": 90,
        "cadera_derecha": 90,
        "cadera_izquierda": 90,
        "hombro_derecho": 90,
        "hombro_izquierdo": 90
    }, pausa=0.5)

def paso_derecho():
    mover_articulaciones({
        "muslo_derecho": 80,
        "rodilla_derecha": 100,
        "pie_derecho": 100,
        "cadera_derecha": 95,
        "hombro_derecho": 85
    }, pausa=0.3)
    mover_articulaciones({
        "rodilla_derecha": 110,
        "pie_derecho": 90
    }, pausa=0.15)

def paso_izquierdo():
    mover_articulaciones({
        "muslo_izquierdo": 80,
        "rodilla_izquierda": 100,
        "pie_izquierdo": 100,
        "cadera_izquierda": 95,
        "hombro_izquierdo": 85
    }, pausa=0.3)
    mover_articulaciones({
        "rodilla_izquierda": 110,
        "pie_izquierdo": 90
    }, pausa=0.15)

def caminar_derecha_sola():
    paso_derecho()
    centrar_todo()

def caminar_izquierda_sola():
    paso_izquierdo()
    centrar_todo()

def caminar_ambas_alternado():
    paso_derecho()
    centrar_todo()
    paso_izquierdo()
    centrar_todo()

def esperar_o_continuar(timeout=0.5):
    print("Presiona Enter para pausar, o espera para continuar...", end='', flush=True)
    i, o, e = select.select([sys.stdin], [], [], timeout)
    if i:
        input()
        return True
    return False

def menu_interactivo():
    while True:
        print("\n--- MENÚ DE CAMINATA ---")
        print("1. Solo pierna derecha")
        print("2. Solo pierna izquierda")
        print("3. Alternar ambas piernas")
        print("q. Salir")
        opcion = input("Selecciona opción (1/2/3/q): ").strip()

        if opcion == "q":
            print("Saliendo del programa...")
            break

        if opcion not in ("1", "2", "3"):
            print("Opción inválida.")
            continue

        print("\nEjecutando... Presiona Enter para pausar y volver al menú.")
        try:
            while True:
                if opcion == "1":
                    caminar_derecha_sola()
                elif opcion == "2":
                    caminar_izquierda_sola()
                elif opcion == "3":
                    caminar_ambas_alternado()

                if esperar_o_continuar():
                    print("⏸️ Pausado. Regresando al menú...")
                    centrar_todo()
                    break
        except KeyboardInterrupt:
            print("\n⚠️ Movimiento interrumpido con Ctrl+C.")
            centrar_todo()
            break

if __name__ == '__main__':
    centrar_todo()
    menu_interactivo()
