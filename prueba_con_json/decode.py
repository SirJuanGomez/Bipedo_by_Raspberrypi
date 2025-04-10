from servo_control import Servo
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

def paso_derecha_adelante():
    mover_articulaciones({
        # Pierna derecha adelante
        "muslo_derecho": 110,
        "muslo_superior_derecho": 100,
        "rodilla_derecha": 100,
        "pie_derecho": 95,

        # Pierna izquierda atrás (soporte)
        "muslo_izquierdo": 70,
        "muslo_superior_izquierdo": 80,
        "rodilla_izquierda": 85,
        "pie_izquierdo": 90,
    }, pausa=0.4)

def paso_izquierda_adelante():
    mover_articulaciones({
        # Pierna izquierda adelante
        "muslo_izquierdo": 110,
        "muslo_superior_izquierdo": 100,
        "rodilla_izquierda": 100,
        "pie_izquierdo": 95,

        # Pierna derecha atrás (soporte)
        "muslo_derecho": 70,
        "muslo_superior_derecho": 80,
        "rodilla_derecha": 85,
        "pie_derecho": 90,
    }, pausa=0.4)

def centrar_piernas():
    mover_articulaciones({
        "muslo_derecho": 90,
        "muslo_superior_derecho": 90,
        "rodilla_derecha": 90,
        "pie_derecho": 90,
        "muslo_izquierdo": 90,
        "muslo_superior_izquierdo": 90,
        "rodilla_izquierda": 90,
        "pie_izquierdo": 90,
    }, pausa=0.2)

# Loop de caminata
if __name__ == '__main__':
    print("Iniciando caminata alternada...")
    try:
        centrar_piernas()
        while True:
            paso_derecha_adelante()
            centrar_piernas()
            paso_izquierda_adelante()
            centrar_piernas()
    except KeyboardInterrupt:
        print("\nCaminata detenida.")
        centrar_piernas()
