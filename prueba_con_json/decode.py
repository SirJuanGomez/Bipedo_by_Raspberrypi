import json
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

LIMB_LENGTH = 30

# Mapeo de nombres a estructura física
JOINT_MAP = {
    "cadera_derecha": ("cadera_derecha", "rodilla_derecha"),
    "rodilla_derecha": ("rodilla_derecha", "pie_derecho"),
    "cadera_izquierda": ("cadera_izquierda", "rodilla_izquierda"),
    "rodilla_izquierda": ("rodilla_izquierda", "pie_izquierdo"),
    "hombro_derecho": ("hombro_derecho", "codo_derecho"),
    "codo_derecho": ("codo_derecho", "mano_derecha"),
    "hombro_izquierdo": ("hombro_izquierdo", "codo_izquierdo"),
    "codo_izquierdo": ("codo_izquierdo", "mano_izquierda")
}

# Posiciones iniciales de articulaciones
def get_default_skeleton():
    torso = np.array([0, 0])
    return {
        "torso": torso,
        "cadera_derecha": torso + np.array([15, -10]),
        "rodilla_derecha": torso + np.array([15, -40]),
        "pie_derecho": torso + np.array([15, -70]),
        "cadera_izquierda": torso + np.array([-15, -10]),
        "rodilla_izquierda": torso + np.array([-15, -40]),
        "pie_izquierdo": torso + np.array([-15, -70]),
        "hombro_derecho": torso + np.array([25, 20]),
        "codo_derecho": torso + np.array([25, 50]),
        "mano_derecha": torso + np.array([25, 80]),
        "hombro_izquierdo": torso + np.array([-25, 20]),
        "codo_izquierdo": torso + np.array([-25, 50]),
        "mano_izquierda": torso + np.array([-25, 80]),
    }

def rotate(v, angle_deg):
    rad = np.radians(angle_deg - 90)
    rot = np.array([[np.cos(rad), -np.sin(rad)], [np.sin(rad), np.cos(rad)]])
    return np.dot(rot, v)

def apply_angles(skeleton, angles):
    skeleton = skeleton.copy()
    for joint, angle in angles.items():
        if joint in JOINT_MAP:
            start, end = JOINT_MAP[joint]
            direction = rotate([0, LIMB_LENGTH], angle)
            skeleton[end] = skeleton[start] + direction
    return skeleton

def load_motion(path):
    with open(path) as f:
        return json.load(f)

def simulate_stickman(motion):
    frames = motion["keyframes"]
    fps = motion["fps"]
    name = motion["name"]

    fig, ax = plt.subplots(figsize=(6, 8))
    line, = ax.plot([], [], 'o-', lw=3, color='black')
    ax.set_xlim(-100, 100)
    ax.set_ylim(-150, 150)
    ax.set_title(f"🧍 Simulación: {name}")
    ax.set_aspect('equal')
    ax.grid(True)

    joints_order = [
        ("torso", "hombro_izquierdo"),
        ("hombro_izquierdo", "codo_izquierdo"),
        ("codo_izquierdo", "mano_izquierda"),
        ("torso", "hombro_derecho"),
        ("hombro_derecho", "codo_derecho"),
        ("codo_derecho", "mano_derecha"),
        ("torso", "cadera_izquierda"),
        ("cadera_izquierda", "rodilla_izquierda"),
        ("rodilla_izquierda", "pie_izquierdo"),
        ("torso", "cadera_derecha"),
        ("cadera_derecha", "rodilla_derecha"),
        ("rodilla_derecha", "pie_derecho")
    ]

    def init():
        line.set_data([], [])
        return line,

    def update(frame_idx):
        frame = frames[frame_idx]
        base_skeleton = get_default_skeleton()
        posed = apply_angles(base_skeleton, frame["angles"])

        xs = []
        ys = []
        for a, b in joints_order:
            xs += [posed[a][0], posed[b][0], None]
            ys += [posed[a][1], posed[b][1], None]
        line.set_data(xs, ys)
        return line,

    ani = animation.FuncAnimation(fig, update, init_func=init,
                                  frames=len(frames), interval=1000 // fps,
                                  blit=True, repeat=False)
    plt.tight_layout()
    plt.show()

# === MAIN ===
if __name__ == "__main__":
    path = input("📂 Ruta al archivo JSON del movimiento: ").strip().strip('"')
    if not os.path.isfile(path):
        print("❌ Archivo no encontrado.")
    else:
        data = load_motion(path)
        simulate_stickman(data)
