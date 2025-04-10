from prueba_con_json.Servo import Servo
from simple_pid import PID
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

    def clamp(self, value, min_value, max_value):
        """Limita un valor dentro de un rango."""
        return max(min(value, max_value), min_value)

    def inverse_kinematics(self, x, y, z, hip_angle=0):
        """Calcula los ángulos de la pierna usando cinemática inversa, con control de cadera."""
        try:
            # Ángulo de la cadera para apertura lateral
            hip_angle_rad = math.radians(hip_angle)
            y_adjusted = y - self.leg_lengths[0] * math.cos(hip_angle_rad)
            z_adjusted = z - self.leg_lengths[0] * math.sin(hip_angle_rad)

            # Cálculos para los demás segmentos
            l_total = math.sqrt(x**2 + y_adjusted**2 + z_adjusted**2)
            w = self.clamp(x / l_total, -1, 1)
            v = self.clamp((self.leg_lengths[1]**2 + l_total**2 - sum(self.leg_lengths[1:])**2) / (2 * self.leg_lengths[1] * l_total), -1, 1)
            b = math.asin(w) - math.acos(v)
            c = math.pi - math.acos(self.clamp((self.leg_lengths[1]**2 + sum(self.leg_lengths[1:])**2 - l_total**2) / (2 * sum(self.leg_lengths[1:]) * self.leg_lengths[1]), -1, 1))

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
    
    def aplly_pid_control(self,angles):
        pid_outputs = []
        for i, angle in enumerate(angles):
            if angles is not None:
                pid_outputs = self.pids[i](angles)
                pid_outputs = self.clamp(pid_outputs,5,175)
                pid_outputs.append(pid_outputs)
            else :
                pid_outputs.append(None)
        return pid_outputs
    
    def convert_trajectory_to_angles(self, trajectory, hip_angle=0):
        """Convierte una trayectoria (x, y, z) en ángulos aplicando control PID."""
        angles_list = []
        for point in trajectory:
            angles = self.inverse_kinematics(*point, hip_angle)
            if self.validate_movement(angles):
                # Aplicar PID a los ángulos calculados
                corrected_angles = self.apply_pid_control(angles)
                angles_list.append(corrected_angles)
            else:
                print("Movimiento no válido.")
                angles_list.append((None, None, None))
        return angles_list
    def validate_movement(self, angles):
        """Verifica que los ángulos estén dentro de los límites."""
        for angle in angles:
            if angle is None or not (5 <= angle <= 175):
                return False
        return True

    
if __name__ == "__main__":
    robot = RobotControl(update_frequency=50)
    trajectory = robot.calculate_step_trajectory(step_height=30, step_length=50)
    angles_list = robot.convert_trajectory_to_angles(trajectory, hip_angle=15)
    for angles in angles_list:
        print(f"Ángulos calculados con PID: {angles}")

