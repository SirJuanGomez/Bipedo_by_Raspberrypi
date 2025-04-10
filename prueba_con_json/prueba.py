import json

ARTICULACIONES_A_SERVO = {
    "pie_derecho": 0,
    "rodilla_derecha": 1,
    "muslo_derecho": 2,
    "muslo_superior_derecho": 3,
    "cadera_derecha": 4,
    "hombro_derecho": 5,
    "codo_derecho": 6,
    "mano_derecha": 7,
    "mano_izquierda": 8,
    "codo_izquierdo": 9,
    "hombro_izquierdo": 10,
    "cadera_izquierda": 11,
    "muslo_superior_izquierdo": 12,
    "muslo_izquierdo": 13,
    "rodilla_izquierda": 14,
    "pie_izquierdo": 15
}

class PID:
    def __init__(self, kp=0.5, ki=0.0, kd=0.1):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = {}
        self.last_error = {}

    def update(self, joint, target, current, dt):
        error = target - current
        self.integral[joint] = self.integral.get(joint, 0) + error * dt
        last_e = self.last_error.get(joint, 0)
        derivative = (error - last_e) / dt if dt > 0 else 0
        self.last_error[joint] = error

        output = (
            self.kp * error +
            self.ki * self.integral[joint] +
            self.kd * derivative
        )
        return output

def pedir_angulo(articulacion):
    while True:
        val = input(f"🦿 Ángulo para '{articulacion}' (0-180 o 'n' para no mover): ").strip().lower()
        if val == 'n':
            return None
        try:
            angulo = int(val)
            if 0 <= angulo <= 180:
                return angulo
            else:
                print("❌ El ángulo debe estar entre 0 y 180.")
        except:
            print("❌ Entrada no válida.")

def crear_keyframe(tiempo):
    print(f"\n🕒 Keyframe en t = {tiempo}s")
    angulos = {}
    for art in ARTICULACIONES_VALIDAS:
        angulo = pedir_angulo(art)
        if angulo is not None:
            angulos[art] = angulo
    return {
        "time": tiempo,
        "angles": angulos
    }

def interpolar_keyframes(pid, inicio, fin, steps, dt):
    frames = []
    actuales = inicio["angles"].copy()

    # Asegurar que todas las articulaciones tengan valor inicial
    for art in ARTICULACIONES_VALIDAS:
        if art not in actuales:
            actuales[art] = fin["angles"].get(art, 90)  # Valor por defecto 90

    for step in range(1, steps + 1):
        t = inicio["time"] + step * dt
        nuevo = {"time": round(t, 3), "servos": []}
        for art in ARTICULACIONES_VALIDAS:
            ang_deseado = fin["angles"].get(art, actuales[art])
            ang_actual = actuales[art]
            output = pid.update(art, ang_deseado, ang_actual, dt)
            ang_nuevo = max(0, min(180, ang_actual + output))
            actuales[art] = ang_nuevo
            nuevo["servos"].append({
                "id": ARTICULACIONES_A_SERVO[art],
                "angle": round(ang_nuevo, 2)
            })
        frames.append(nuevo)
    return frames

def crear_movimiento_con_pid():
    nombre = input("📛 Nombre del movimiento: ")
    fps = int(input("🎞️ FPS para la animación (ej: 30): "))
    base_keyframes = []
    tiempo = 0

    while True:
        base_keyframes.append(crear_keyframe(tiempo))
        continuar = input("➕ ¿Agregar otro keyframe? (s/n): ").strip().lower()
        if continuar != 's':
            break
        tiempo += float(input("⏱️ ¿Cuántos segundos hasta el próximo keyframe?: "))

    pid = PID(kp=0.8, ki=0.0, kd=0.05)
    all_frames = []
    dt = 1.0 / fps

    for i in range(len(base_keyframes) - 1):
        kf1 = base_keyframes[i]
        kf2 = base_keyframes[i + 1]
        duration = kf2["time"] - kf1["time"]
        steps = int(duration / dt)
        inter_frames = interpolar_keyframes(pid, kf1, kf2, steps, dt)
        all_frames.extend(inter_frames)

    motion = {
        "name": nombre,
        "fps": fps,
        "frames": all_frames
    }

    archivo = input("💾 Nombre del archivo para guardar (ej: saludo.json): ").strip()
    with open(archivo, "w") as f:
        json.dump(motion, f, indent=2)
    print(f"✅ Movimiento guardado en '{archivo}' con {len(all_frames)} frames generados.")

# === MAIN ===
if __name__ == "__main__":
    crear_movimiento_con_pid()
