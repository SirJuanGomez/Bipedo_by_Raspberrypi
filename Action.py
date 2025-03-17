from Control import RobotControl
import time

class RobotActions:
    def __init__(self, update_frequency=50):
        self.robot = RobotControl(update_frequency)
        self.step_height = 30  # Altura del paso
        self.step_length = 50  # Longitud del paso
        self.hip_angle = 15  # Ángulo de apertura de la cadera

    def walk_forward(self, steps=5):
        """Realiza una secuencia de pasos hacia adelante."""
        for _ in range(steps):
            trajectory = self.robot.calculate_step_trajectory(self.step_height, self.step_length)
            for point in trajectory:
                x, y, z = point
                # Corregir valores fuera del dominio
                x = max(min(x, 1), -1)
                y = max(min(y, 1), -1)
                z = max(min(z, 1), -1)
                angles = self.robot.inverse_kinematics(x, y, z, hip_angle=self.hip_angle)
                if self.robot.validate_movement(angles):
                    print(f"Ángulos calculados: {angles}")
                    time.sleep(self.robot.update_period)
                else:
                    print("Movimiento no válido.")

    def squat(self, depth=40):
        """Simula el movimiento de agacharse."""
        print("Agachándose...")
        for i in range(depth):
            # Corregir valores fuera del dominio
            i = max(min(i, 1), -1)
            angles = self.robot.inverse_kinematics(0, -i, 0, hip_angle=0)
            if self.robot.validate_movement(angles):
                print(f"Ángulos al agacharse: {angles}")
                time.sleep(self.robot.update_period)
        print("Levantándose...")
        for i in range(depth, 0, -1):
            # Corregir valores fuera del dominio
            i = max(min(i, 1), -1)
            angles = self.robot.inverse_kinematics(0, -i, 0, hip_angle=0)
            if self.robot.validate_movement(angles):
                print(f"Ángulos al levantarse: {angles}")
                time.sleep(self.robot.update_period)

if __name__ == "__main__":
    actions = RobotActions(update_frequency=50)
    actions.walk_forward(steps=3)
    actions.squat(depth=30)
