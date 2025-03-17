#coding:utf-8
import time

class PID:
    def __init__(self, Kp=0.8, Ki=0.01, Kd=0.05, output_min=5, output_max=175, update_frequency=50):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = 0.0
        self.integral = 0.0
        self.last_error = 0.0
        self.output = 0.0
        self.output_min = output_min
        self.output_max = output_max
        self.update_period = 1.0 / update_frequency  # Período de actualización
        self.last_update_time = time.time()

    def compute(self, current_value):
        current_time = time.time()
        if current_time - self.last_update_time >= self.update_period:
            error = self.setpoint - current_value
            self.integral += error
            derivative = error - self.last_error
            self.output = (self.Kp * error) + (self.Ki * self.integral) + (self.Kd * derivative)
            self.last_error = error
            # Limitar la salida
            self.output = max(min(self.output, self.output_max), self.output_min)
            self.last_update_time = current_time
        return self.output

    def setSetpoint(self, setpoint):
        print(f"Setpoint actualizado a: {setpoint}")
        self.setpoint = setpoint

    def getSetpoint(self):
        return self.setpoint

    def tune(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

# Main program logic follows:
if __name__ == "__main__":
    pid = PID(0.8, 0.01, 0.05, update_frequency=50)  # 50 Hz
    pid.setSetpoint(90)

    current_value = 85
    while True:
        control_output = pid.compute(current_value)
        print(f"Setpoint: {pid.getSetpoint()} | Control Output: {control_output}")
        time.sleep(0.01)  # Simulación de lectura de sensores
