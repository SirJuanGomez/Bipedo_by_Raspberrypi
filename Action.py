import math
from Control import *
from Servo import *
class Action:
    def __init__(self):
        self.servo = Servo()
        self.control = Control()
        self.servo.setServoAngle(15, 90)

    def step_forward(self):
        # Utiliza la función forWard del Control
        self.control.forWard()

    def wave_hand(self):
        # Eleva primero el hombro y el codo antes de saludar
        for i in range(90, 130):
            self.servo.setServoAngle(11, i)  # Hombro
            time.sleep(0.02)
        for i in range(90, 130):
            self.servo.setServoAngle(12, i)  # Codo
            time.sleep(0.02)
        for i in range(90, 130):
            self.servo.setServoAngle(13, i)  # Muñeca
            time.sleep(0.02)
        # Vuelve primero la muñeca, luego el codo y finalmente el hombro
        for i in range(130, 90, -1):
            self.servo.setServoAngle(13, i)  # Muñeca
            time.sleep(0.02)
        for i in range(130, 90, -1):
            self.servo.setServoAngle(12, i)  # Codo
            time.sleep(0.02)
        for i in range(130, 90, -1):
            self.servo.setServoAngle(11, i)  # Hombro
            time.sleep(0.02)
    def squat(self):
        # Agacharse y levantarse usando setpLeft y setpRight para simular equilibrio
        for _ in range(5):
            self.control.setpLeft()
            self.control.setpRight()

if __name__ == '__main__':
    action = Action()
    time.sleep(2)
    while True:
        action.step_forward()
        action.wave_hand()
        action.squat()
        time.sleep(3)
