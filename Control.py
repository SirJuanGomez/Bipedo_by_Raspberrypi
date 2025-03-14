# -*- coding: utf-8 -*-
import time
import math
import smbus
import copy
import threading
from PID import *
import numpy as np
from Servo import *
from Command import COMMAND as cmd

# Constantes
ARM_RANGE = (15, 100)  # Rango válido para los brazos
LEG_RANGE = (25, 130)  # Rango válido para las piernas

class Control:
    def __init__(self):
        self.servo = Servo()
        self.pid = Incremental_PID(0.5, 0.0, 0.0025)
        self.speed = 8
        self.height = 99
        self.timeout = 0
        self.move_flag = 0
        self.move_count = 0
        self.move_timeout = 0
        self.point = [[0, 99, 10], [0, 99, 10], [0, 99, -10], [0, 99, -10]]
        self.angle = [[90, 0, 0], [90, 0, 0], [90, 0, 0], [90, 0, 0]]
        self.calibration_angle = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.arm_lengths = [23, 55, 55]  # Longitudes de los brazos (3 segmentos)
        self.leg_lengths = [23, 55, 55, 30]  # Longitudes de las piernas (4 segmentos)
        self.order = ['', '', '', '', '']  # Comandos
        self.calibration()
        self.relax(True)
        self.Thread_condition = threading.Thread(target=self.condition)
        self.Thread_condition.start()

    def toRadians(self, degrees):
        """Convierte grados a radianes."""
        return math.radians(degrees)

    def coordinateToAngle(self, x, y, z, lengths):
        """Convierte coordenadas a ángulos."""
        if len(lengths) < 2:
            raise ValueError("Se requieren al menos dos segmentos para calcular el ángulo.")
        a = math.pi / 2 - math.atan2(z, y)
        l_total = sum(lengths)
        l_target = math.sqrt(x**2 + y**2 + z**2 - 2 * z * lengths[0] * math.cos(a))
        w = x / l_target
        v = (lengths[1]**2 + l_target**2 - l_total**2) / (2 * lengths[1] * l_target)
        b = math.asin(w) - math.acos(v)
        c = math.pi - math.acos((lengths[1]**2 + l_total**2 - l_target**2) / (2 * l_total * lengths[1]))
        return round(math.degrees(a)), round(math.degrees(b)), round(math.degrees(c))

    def angleToCoordinate(self, angles, lengths):
        """Convierte ángulos a coordenadas."""
        if len(angles) != len(lengths):
            raise ValueError("La cantidad de ángulos debe coincidir con la cantidad de segmentos.")
        angles = [self.toRadians(a) for a in angles]
        x, y, z = 0, 0, 0
        for i in range(len(lengths)):
            x += lengths[i] * math.sin(sum(angles[:i + 1]))
            y += lengths[i] * math.sin(angles[0]) * math.cos(sum(angles[1:i + 1]))
            z += lengths[i] * math.cos(angles[0]) * math.cos(sum(angles[1:i + 1]))
        return x, y, z

    def calibration(self):
        """Calibra los ángulos iniciales."""
        for i in range(4):
            lengths = self.arm_lengths if i < 2 else self.leg_lengths
            self.calibration_angle[i] = [self.coordinateToAngle(*self.point[i], lengths)[j] for j in range(3)]

    def checkPoint(self):
        """Verifica si los puntos están dentro del rango permitido."""
        for i, p in enumerate(self.point):
            distance = math.sqrt(sum(coord ** 2 for coord in p))
            if i < 2:  # Brazos
                if not (ARM_RANGE[0] <= distance <= ARM_RANGE[1]):
                    return False
            else:  # Piernas
                if not (LEG_RANGE[0] <= distance <= LEG_RANGE[1]):
                    return False
        return True

    def restriction(self, var, v_min, v_max):
        """Restringe un valor dentro de un rango."""
        return max(v_min, min(var, v_max))

    def run(self):
        """Ejecuta el movimiento basado en los puntos actuales."""
        if self.checkPoint():
            try:
                for i in range(4):
                    self.angle[i][0], self.angle[i][1], self.angle[i][2] = self.coordinateToAngle(self.point[i][0],
                                                                                                   self.point[i][1],
                                                                                                   self.point[i][2])
                for i in range(2):
                    self.angle[i][0] = self.restriction(self.angle[i][0] + self.calibration_angle[i][0], 0, 180)
                    self.angle[i][1] = self.restriction(90 - (self.angle[i][1] + self.calibration_angle[i][1]), 0, 180)
                    self.angle[i][2] = self.restriction(self.angle[i][2] + self.calibration_angle[i][2], 0, 180)
                    self.angle[i + 2][0] = self.restriction(self.angle[i + 2][0] + self.calibration_angle[i + 2][0], 0, 180)
                    self.angle[i + 2][1] = self.restriction(90 + self.angle[i + 2][1] + self.calibration_angle[i + 2][1], 0, 180)
                    self.angle[i + 2][2] = self.restriction(180 - (self.angle[i + 2][2] + self.calibration_angle[i + 2][2]), 0, 180)
                for i in range(2):
                    self.servo.setServoAngle(4 + i * 3, self.angle[i][0])
                    self.servo.setServoAngle(3 + i * 3, self.angle[i][1])
                    self.servo.setServoAngle(2 + i * 3, self.angle[i][2])
                    self.servo.setServoAngle(8 + i * 3, self.angle[i + 2][0])
                    self.servo.setServoAngle(9 + i * 3, self.angle[i + 2][1])
                    self.servo.setServoAngle(10 + i * 3, self.angle[i + 2][2])
            except ValueError as ve:
                print(f"ValueError: {ve}")
            except Exception as e:
                print(f"Unexpected error: {e}")
        else:
            print("This coordinate point is out of the active range")

    def condition(self):
        """Monitorea y ejecuta comandos según la orden recibida."""
        command_map = {
            cmd.CMD_MOVE_STOP: self.stop,
            cmd.CMD_MOVE_FORWARD: self.forWard,
            cmd.CMD_MOVE_BACKWARD: self.backWard,
            cmd.CMD_MOVE_LEFT: self.setpLeft,
            cmd.CMD_MOVE_RIGHT: self.setpRight,
            cmd.CMD_TURN_LEFT: self.turnLeft,
            cmd.CMD_TURN_RIGHT: self.turnRight,
            cmd.CMD_RELAX: lambda: self.relax(True)
        }
        while True:
            try:
                if self.order[0] in command_map:
                    self.speed = int(self.order[1]) if len(self.order) > 1 else self.speed
                    command_map[self.order[0]]()
                    self.order = ['', '', '', '', '']
            except Exception as e:
                print(f"Error in command processing: {e}")

    def changeCoordinates(self, move_order, X1=0, Y1=96, Z1=0, X2=0, Y2=96, Z2=0):
        """Cambia las coordenadas según el movimiento solicitado."""
        if move_order in ['forWard', 'backWard', 'setpRight', 'setpLeft']:
            for i in range(2):
                # Piernas
                self.point[i * 2] = [X1 + 10, Y1, Z1]
                self.point[i * 2 + 1] = [X2 + 10, Y2, Z2]
                # Brazos en dirección contraria a las piernas
                self.point[i] = [-X1 + 10, Y1, -Z1] if i == 0 else [-X2 + 10, Y2, -Z2]
        elif move_order in ['turnLeft', 'turnRight']:
            for i in range(2):
                self.point[i * 2] = [(-1)**i * X1 + 10, Y1, (-1)**(1 + i) * Z1]
                self.point[i * 2 + 1] = [(-1)**i * X2 + 10, Y2, (-1)**i * Z2]
        self.run()

    def forWard(self):
        """Ejecuta el movimiento hacia adelante."""
        for i in range(90, 451, self.speed):
            # Piernas
            X1 = 12 * math.cos(i * math.pi / 180)
            Y1 = 6 * math.sin(i * math.pi / 180) + self.height
            X2 = 12 * math.cos((i + 180) * math.pi / 180)
            Y2 = 6 * math.sin((i + 180) * math.pi / 180) + self.height
            # Ejecutar movimiento
            self.changeCoordinates('forWard', X1, Y1, 0, X2, Y2, 0)

    def backWard(self):
        """Ejecuta el movimiento hacia atrás."""
        for i in range(450, 89, -self.speed):
            # Piernas
            X1 = 12 * math.cos(i * math.pi / 180)
            Y1 = 6 * math.sin(i * math.pi / 180) + self.height
            X2 = 12 * math.cos((i + 180) * math.pi / 180)
            Y2 = 6 * math.sin((i + 180) * math.pi / 180) + self.height
            # Ejecutar movimiento
            self.changeCoordinates('backWard', X1, Y1, 0, X2, Y2, 0)

    def turnLeft(self):
        """Ejecuta el movimiento de giro a la izquierda."""
        for i in range(0, 361, self.speed):
            # Piernas
            X1 = 3 * math.cos(i * math.pi / 180)
            Y1 = 8 * math.sin(i * math.pi / 180) + self.height
            X2 = 3 * math.cos((i + 180) * math.pi / 180)
            Y2 = 8 * math.sin((i + 180) * math.pi / 180) + self.height
            Z1 = X1
            Z2 = X2
            # Ejecutar movimiento
            self.changeCoordinates('turnLeft', X1, Y1, Z1, X2, Y2, Z2)

    def turnRight(self):
        """Ejecuta el movimiento de giro a la derecha."""
        for i in range(0, 361, self.speed):
            # Piernas
            X1 = 3 * math.cos(i * math.pi / 180)
            Y1 = 8 * math.sin(i * math.pi / 180) + self.height
            X2 = 3 * math.cos((i + 180) * math.pi / 180)
            Y2 = 8 * math.sin((i + 180) * math.pi / 180) + self.height
            Z1 = X1
            Z2 = X2
            # Ejecutar movimiento
            self.changeCoordinates('turnRight', X1, Y1, Z1, X2, Y2, Z2)

    def setpLeft(self):
        """Ejecuta el movimiento de paso a la izquierda."""
        for i in range(90, 451, self.speed):
            # Piernas
            Z1 = 10 * math.cos(i * math.pi / 180)
            Y1 = 5 * math.sin(i * math.pi / 180) + self.height
            Z2 = 10 * math.cos((i + 180) * math.pi / 180)
            Y2 = 5 * math.sin((i + 180) * math.pi / 180) + self.height
            # Ejecutar movimiento
            self.changeCoordinates('setpLeft', 0, Y1, Z1, 0, Y2, Z2)

    def setpRight(self):
        """Ejecuta el movimiento de paso a la derecha."""
        for i in range(450, 89, -self.speed):
            # Piernas
            Z1 = 10 * math.cos(i * math.pi / 180)
            Y1 = 5 * math.sin(i * math.pi / 180) + self.height
            Z2 = 10 * math.cos((i + 180) * math.pi / 180)
            Y2 = 5 * math.sin((i + 180) * math.pi / 180) + self.height
            # Ejecutar movimiento
            self.changeCoordinates('setpRight', 0, Y1, Z1, 0, Y2, Z2)

    def stop(self):
        """Detiene el movimiento y regresa a la posición inicial."""
        p = [[10, self.height, 10], [10, self.height, 10], [10, self.height, -10], [10, self.height, -10]]
        for i in range(4):
            p[i][0] = (p[i][0] - self.point[i][0]) / 50
            p[i][1] = (p[i][1] - self.point[i][1]) / 50
            p[i][2] = (p[i][2] - self.point[i][2]) / 50
        for j in range(50):
            for i in range(4):
                self.point[i][0] += p[i][0]
                self.point[i][1] += p[i][1]
                self.point[i][2] += p[i][2]
            self.run()

    def relax(self, flag=False):
        """Relaja los movimientos del sistema."""
        if flag:
            p = [[55, 78, 0], [55, 78, 0], [55, 78, 0], [55, 78, 0]]
            for i in range(4):
                p[i][0] = (self.point[i][0] - p[i][0]) / 50
                p[i][1] = (self.point[i][1] - p[i][1]) / 50
                p[i][2] = (self.point[i][2] - p[i][2]) / 50
            for j in range(1, 51):
                for i in range(4):
                    self.point[i][0] -= p[i][0]
                    self.point[i][1] -= p[i][1]
                    self.point[i][2] -= p[i][2]
                self.run()
            if self.move_timeout != 0:
                self.move_count += time.time() - self.move_timeout
                self.move_timeout = time.time()
        else:
            self.stop()
            self.move_timeout = time.time()

if __name__ == '__main__':
    pass