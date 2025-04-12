from Servo import Servo
import time
class Moves:
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

    def __init__(self):
        self.robot = Servo()

    def mover_articulaciones(self,movimientos, pausa=0.01):
        for articulacion, angulo in movimientos.items():
            canal = self.ARTICULACIONES_A_SERVO.get(articulacion)
            if canal is not None:
                self.robot.setServoAngle(canal, angulo)
            else:
                print(f"⚠️ Articulación '{articulacion}' no encontrada.")
        time.sleep(pausa)

    def pose_saludo(self):
        self.mover_articulaciones({
            ##################Superior############################
            "hombro_derecho": 150,
            "codo_derecho": 90,
            "mano_derecha": 90,    
            "hombro_izquierdo": 120,
            "codo_izquierdo": 90,
            "mano_izquierda": 90,
            ####################Inferior##########################
            "cadera_derecha": 105,
            "muslo_derecho": 100,
            "rodilla_derecha": 90,
            "pie_derecho": 90,
            "cadera_izquierda": 105,
            "muslo_izquierdo": 90,
            "rodilla_izquierda": 80,
            "pie_izquierdo": 85
        }, pausa=0.9)

    def saludo_hands(self):
        self.mover_articulaciones({
            ##################Superior############################
            "hombro_derecho": 170,
            "codo_derecho": 100,
            "mano_derecha": 95,    
            "hombro_izquierdo": 120,
            "codo_izquierdo": 90,
            "mano_izquierda": 90,
        },pausa=0.5)
        
        self.mover_articulaciones({
            ##################Superior############################
            "hombro_derecho": 150,
            "codo_derecho": 90,
            "mano_derecha": 90,    
            "hombro_izquierdo": 120,
            "codo_izquierdo": 90,
            "mano_izquierda": 90,
        },pausa=0.5)

    def pose_inicial(self):
        for i in range(16):
            self.robot.setServoAngle(i,90)


    def saludo_up(self):
        self.mover_articulaciones({
            ##################Superior############################
            "hombro_derecho": 150,
            "codo_derecho": 90,
            "mano_derecha": 90,    
            "hombro_izquierdo": 120,
            "codo_izquierdo": 90,
            "mano_izquierda": 90,
        },pausa=0.5)
        
        self.mover_articulaciones({
            ##################Superior############################
            "hombro_derecho": 170,
            "codo_derecho": 100,
            "mano_derecha": 90,    
            "hombro_izquierdo": 120,
            "codo_izquierdo": 90,
            "mano_izquierda": 90,
        },pausa=0.5)
        
    def head_cicle(self):
        self.mover_articulaciones({"cabeza":130},pausa=1)
        self.mover_articulaciones({"cabeza":35},pausa=1)


