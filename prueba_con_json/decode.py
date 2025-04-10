import json
import time
from prueba_con_json.Servo import Servo

FPS_POR_DEFECTO = 30

def reproducir_movimiento(nombre_archivo):
    with open(nombre_archivo, "r") as f:
        data = json.load(f)

    fps = data.get("fps", FPS_POR_DEFECTO)
    delay = 1.0 / fps
    frames = data["frames"]

    servo = Servo()

    for frame in frames:
        print(f"t = {frame['time']}s")
        for servo_data in frame["servos"]:
            servo_id = servo_data["id"]
            angle = servo_data["angle"]
            servo.setServoAngle(servo_id, angle)
        time.sleep(delay)

    print("Movimiento completado.")

# === MAIN ===
if __name__ == "__main__":
    archivo = input("Archivo de movimiento:").strip()
    reproducir_movimiento(archivo)
