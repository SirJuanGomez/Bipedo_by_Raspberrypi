import json
import time
from Servo import *

servo_contrl = Servo()
# Mapeo entre nombres del JSON y objetos servo que vos ya creaste
servo_map = {
    "rodilla_izquierda": 3 ,
    "pie_izquierdo": 4,
    "rodilla_derecha": 13 ,
    "pie_derecho": 14 
}

# Cargar el archivo JSON
with open("movimiento.json", "r") as f:
    data = json.load(f)

fps = data["fps"]
frame_duration = 1 / fps
keyframes = data["keyframes"]

# Reproducir la animación
for i, keyframe in enumerate(keyframes):
    angles = keyframe["angles"]

    for name, angle in angles.items():
        if name in servo_map:
            servo_map[name].set_angle(angle)  # Usá tu propia función aquí

    # Calcular el tiempo de espera
    if i < len(keyframes) - 1:
        t_actual = keyframe["time"]
        t_siguiente = keyframes[i + 1]["time"]
        sleep_time = (t_siguiente - t_actual) * frame_duration
        time.sleep(sleep_time)
