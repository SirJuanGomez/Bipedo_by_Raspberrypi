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
    }, pausa=0.4)

def paso_derecho_adelante():
    # Etapa 1: levantar pierna derecha
    mover_articulaciones({
        "muslo_derecho": 80,
        "muslo_superior_derecho": 85,
        "rodilla_derecha": 100,   # menos flexión al levantar
        "pie_derecho": 100,       # inclinado

        "muslo_izquierdo": 100,
        "muslo_superior_izquierdo": 95,
        "rodilla_izquierda": 95,
        "pie_izquierdo": 90,

        "cadera_derecha": 95,
        "cadera_izquierda": 95,
        "hombro_derecho": 85,
        "hombro_izquierdo": 95,
    }, pausa=0.3)

    # Etapa 2: bajar pierna, flexionando un poco la rodilla
    mover_articulaciones({
        "rodilla_derecha": 110,  # más flexión
        "pie_derecho": 90        # pie plano
    }, pausa=0.15)

def paso_izquierdo_adelante():
    # Etapa 1: levantar pierna izquierda
    mover_articulaciones({
        "muslo_izquierdo": 80,
        "muslo_superior_izquierdo": 85,
        "rodilla_izquierda": 100,
        "pie_izquierdo": 100,

        "muslo_derecho": 100,
        "muslo_superior_derecho": 95,
        "rodilla_derecha": 95,
        "pie_derecho": 90,

        "cadera_derecha": 85,
        "cadera_izquierda": 85,
        "hombro_derecho": 95,
        "hombro_izquierdo": 85,
    }, pausa=0.3)

    # Etapa 2: bajar pierna izquierda con flexión
    mover_articulaciones({
        "rodilla_izquierda": 110,
        "pie_izquierdo": 90
    }, pausa=0.15)

# 🦿 Bucle principal de caminata
if __name__ == '__main__':
    print("Iniciando caminata fluida y balanceada...")
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
