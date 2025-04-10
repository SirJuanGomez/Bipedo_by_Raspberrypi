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
        # Piernas
        "muslo_derecho": 90,
        "muslo_superior_derecho": 90,
        "rodilla_derecha": 90,
        "pie_derecho": 90,
        "muslo_izquierdo": 90,
        "muslo_superior_izquierdo": 90,
        "rodilla_izquierda": 90,
        "pie_izquierdo": 90,
        # Cadera
        "cadera_derecha": 90,
        "cadera_izquierda": 90,
        # Brazos
        "hombro_derecho": 90,
        "hombro_izquierdo": 90,
    }, pausa=0.2)

def paso_derecho_adelante():
    mover_articulaciones({
        # Pierna derecha al frente
        "muslo_derecho": 110,
        "muslo_superior_derecho": 100,
        "rodilla_derecha": 115,
        "pie_derecho": 95,
        # Pierna izquierda atrás
        "muslo_izquierdo": 70,
        "muslo_superior_izquierdo": 80,
        "rodilla_izquierda": 85,
        "pie_izquierdo": 90,
        # Cadera inclinada para empuje
        "cadera_derecha": 100,
        "cadera_izquierda": 100,
        # Brazos opuestos
        "hombro_derecho": 70,     # Atrás
        "hombro_izquierdo": 110,  # Adelante
    }, pausa=0.4)

def paso_izquierdo_adelante():
    mover_articulaciones({
        # Pierna izquierda al frente
        "muslo_izquierdo": 110,
        "muslo_superior_izquierdo": 100,
        "rodilla_izquierda": 115,
        "pie_izquierdo": 95,
        # Pierna derecha atrás
        "muslo_derecho": 70,
        "muslo_superior_derecho": 80,
        "rodilla_derecha": 85,
        "pie_derecho": 90,
        # Cadera inclinada para empuje
        "cadera_derecha": 80,
        "cadera_izquierda": 80,
        # Brazos opuestos
        "hombro_derecho": 110,  # Adelante
        "hombro_izquierdo": 70, # Atrás
    }, pausa=0.4)

# 🦿 Bucle de caminata completa
if __name__ == '__main__':
    print("Iniciando caminata humana mejorada...")
    try:
        centrar_todo()
        while True:
            paso_derecho_adelante()
            centrar_todo()
            paso_izquierdo_adelante()
            centrar_todo()
    except KeyboardInterrupt:
        print("\nCaminata detenida.")
        centrar_todo()
