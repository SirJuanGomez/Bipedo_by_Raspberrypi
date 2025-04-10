from Servo import Servo
import time

ARTICULACIONES_A_SERVO = {
    "pie_derecho": 0,
    "rodilla_derecha": 1,
    "muslo_derecho": 2,
    "muslo_superior_derecho": 3,
    "cadera_derecha": 4,
    "hombro_derecho": 5,
    "codo_derecho": 6,
    "mano_derecha": 7,
    "mano_izquierda": 8,
    "codo_izquierdo": 9,
    "hombro_izquierdo": 10,
    "cadera_izquierda": 11,
    "muslo_superior_izquierdo": 12,
    "muslo_izquierdo": 13,
    "rodilla_izquierda": 14,
    "pie_izquierdo": 15
}

robot = Servo()

def mover_articulaciones(movimientos, pausa=0.01):
    for articulacion, angulo in movimientos.items():
        canal = ARTICULACIONES_A_SERVO[articulacion]
        robot.setServoAngle(canal, angulo)
    time.sleep(pausa)

def centrar_todo():
    mover_articulaciones({
        "muslo_derecho": 90, "muslo_superior_derecho": 90,
        "rodilla_derecha": 90, "pie_derecho": 90,
        "muslo_izquierdo": 90, "muslo_superior_izquierdo": 90,
        "rodilla_izquierda": 90, "pie_izquierdo": 90,
        "cadera_derecha": 90, "cadera_izquierda": 90,
        "hombro_derecho": 90, "hombro_izquierdo": 90
    }, pausa=0.5)

# Paso derecho solo
def paso_derecho():
    mover_articulaciones({
        "muslo_derecho": 80,
        "muslo_superior_derecho": 85,
        "rodilla_derecha": 100,
        "pie_derecho": 100,
        "cadera_derecha": 95,
        "hombro_derecho": 85
    }, pausa=0.3)
    mover_articulaciones({
        "rodilla_derecha": 110,
        "pie_derecho": 90
    }, pausa=0.15)

# Paso izquierdo solo
def paso_izquierdo():
    mover_articulaciones({
        "muslo_izquierdo": 80,
        "muslo_superior_izquierdo": 85,
        "rodilla_izquierda": 100,
        "pie_izquierdo": 100,
        "cadera_izquierda": 95,
        "hombro_izquierdo": 85
    }, pausa=0.3)
    mover_articulaciones({
        "rodilla_izquierda": 110,
        "pie_izquierdo": 90
    }, pausa=0.15)

# Secuencias de prueba
def caminar_derecha_sola(repeticiones=3):
    centrar_todo()
    for _ in range(repeticiones):
        paso_derecho()
        centrar_todo()

def caminar_izquierda_sola(repeticiones=3):
    centrar_todo()
    for _ in range(repeticiones):
        paso_izquierdo()
        centrar_todo()

def caminar_ambas_alternado(repeticiones=3):
    centrar_todo()
    for _ in range(repeticiones):
        paso_derecho()
        centrar_todo()
        paso_izquierdo()
        centrar_todo()

# Menú principal
if __name__ == '__main__':
    try:
        print("1. Solo pierna derecha")
        print("2. Solo pierna izquierda")
        print("3. Alternar ambas piernas")
        opcion = input("Selecciona opción (1/2/3): ").strip()
        if opcion == "1":
            caminar_derecha_sola()
        elif opcion == "2":
            caminar_izquierda_sola()
        elif opcion == "3":
            caminar_ambas_alternado()
        else:
            print("Opción no válida.")
    except KeyboardInterrupt:
        print("\nMovimiento detenido por usuario.")
        centrar_todo()
