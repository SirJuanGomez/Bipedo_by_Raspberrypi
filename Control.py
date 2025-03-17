from Servo import Servo
from PID import PID
import math

class RobotControl:
    def __init__(self, update_frequency=50):
        # Inicialización de Servo y PIDs
        self.servo = Servo()
        self.pids = [PID(0.8, 0.01, 0.05) for _ in range(16)]
        self.setpoints = [90] * 16  # Setpoints iniciales en 90 grados
        self.update_period = 1.0 / update_frequency
        # Longitudes de los segmentos desde la cadera hasta el pie
        self.leg_lengths = [40, 62.9, 60, 43.9, 46.96]

    def set_setpoint(self, servo_id, value):
        """Actualizar el setpoint de un servo específico."""
        if 0 <= servo_id <= 15 and 5 <= value <= 175:
            self.setpoints[servo_id] = value
            self.pids[servo_id].setSetpoint(value)
        else:
            print(f"Error: Setpoint {value} fuera de rango para el servo {servo_id}")

    def inverse_kinematics(self, x, y, z, hip_angle=0):
        """Calcula los ángulos de la pierna usando cinemática inversa, con control de cadera."""
        try:
            # Ángulo de la cadera para apertura lateral
            hip_angle_rad = math.radians(hip_angle)
            y_adjusted = y - self.leg_lengths[0] * math.cos(hip_angle_rad)
            z_adjusted = z - self.leg_lengths[0] * math.sin(hip_angle_rad)

            # Cálculos para los demás segmentos
            l_total = math.sqrt(x**2 + y_adjusted**2 + z_adjusted**2)
            w = x / l_total
            v = (self.leg_lengths[1]**2 + l_total**2 - sum(self.leg_lengths[1:])**2) / (2 * self.leg_lengths[1] * l_total)
            b = math.asin(w) - math.acos(v)
            c = math.pi - math.acos((self.leg_lengths[1]**2 + sum(self.leg_lengths[1:])**2 - l_total**2) / (2 * sum(self.leg_lengths[1:]) * self.leg_lengths[1]))

            return hip_angle, math.degrees(b), math.degrees(c)
        except ValueError as e:
            print(f"Error en la cinemática inversa: {e}")
            return None, None, None

    def calculate_step_trajectory(self, step_height, step_length, steps=10):
        """Genera una trayectoria para un paso."""
        trajectory = []
        for i in range(steps + 1):
            t = i / steps
            x = step_length * t
            y = 0
            z = step_height * math.sin(math.pi * t)
            trajectory.append((x, y, z))
        return trajectory

    def validate_movement(self, angles):
        """Verifica que los ángulos estén dentro de los límites."""
        for angle in angles:
            if angle is None or not (5 <= angle <= 175):
                return False
        return True

if __name__ == "__main__":
    robot = RobotControl(update_frequency=50)
    trajectory = robot.calculate_step_trajectory(step_height=30, step_length=50)
    for point in trajectory:
        angles = robot.inverse_kinematics(*point, hip_angle=15)  # Prueba con la cadera a 15°
        if robot.validate_movement(angles):
            print(f"Ángulos calculados: {angles}")
        else:
            print("Movimiento no válido.")
