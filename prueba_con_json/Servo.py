#coding:utf-8
from PCA9685 import PCA9685
import time 

class Servo:
    def __init__(self, pwm_freq=50):
        self.angleMin = 18
        self.angleMax = 162
        self.pwm = PCA9685(address=0x40, debug=True)   
        self.pwm.setPWMFreq(pwm_freq)  # Set the cycle frequency of PWM

    # Clamp value to ensure it's within the min and max range
    def clamp(self, value, min_value, max_value):
        return max(min(value, max_value), min_value)

    # Convert the input angle to the value of pca9685
    def map(self, value, fromLow, fromHigh, toLow, toHigh):
        return (toHigh - toLow) * (value - fromLow) / (fromHigh - fromLow) + toLow

    def setServoAngle(self, channel, angle):
        # Validate channel range
        if not (0 <= channel <= 15):
            raise ValueError(f"Canal {channel} fuera de rango (0-15)")

        # Clamp the angle to prevent physical damage
        angle = self.clamp(angle, self.angleMin, self.angleMax)
        date = self.map(angle, 0, 180, 102, 512)
        self.pwm.setPWM(channel, 0, int(date))
        print(f"Servo {channel} movido a ángulo {angle}°")

# Main program logic follows:
if __name__ == '__main__':
    print("Now servos will rotate to 90°.") 
    print("If they have already been at 90°, nothing will be observed.")
    print("Please keep the program running when installing the servos.")
    print("After that, you can press ctrl-C to end the program.")
    S = Servo()
    while True:
        try:
            for i in range(16):
                S.setServoAngle(i, 90)
        except KeyboardInterrupt:
            print("\nEnd of program")
            break
