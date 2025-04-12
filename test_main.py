import tkinter as tk
from IR_Data import IRHandler  # Importa la clase IRHandler para manejar el receptor IR
import time
from Moves import Moves  # Importa la clase Moves desde moves.py

# Instancia de la clase Moves
moves = Moves()

# Diccionario de callbacks con los métodos de la clase Moves
callbacks = {
    "pose_saludo": moves.pose_saludo,
    "saludo_hands": moves.saludo_hands,
    "saludo_up": moves.saludo_up,
    "head_cicle": moves.head_cicle
}

# Clase que crea la interfaz gráfica en Tkinter
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Control IR con Tkinter")
        
        # Crear los botones en la ventana
        self.btn_pose_saludo = tk.Button(root, text="Pose Saludo", command=self.pose_saludo)
        self.btn_pose_saludo.pack(padx=10, pady=10)

        self.btn_saludo_hands = tk.Button(root, text="Saludo Hands", command=self.saludo_hands)
        self.btn_saludo_hands.pack(padx=10, pady=10)

        self.btn_saludo_up = tk.Button(root, text="Saludo Up", command=self.saludo_up)
        self.btn_saludo_up.pack(padx=10, pady=10)

        self.btn_head_cicle = tk.Button(root, text="Head Cicle", command=self.head_cicle)
        self.btn_head_cicle.pack(padx=10, pady=10)

        # Inicializa el receptor IR en el GPIO 17
        self.ir_handler = IRHandler(gpio_pin=17, callbacks=callbacks)

    def pose_saludo(self):
        moves.pose_saludo()

    def saludo_hands(self):
        moves.saludo_hands()

    def saludo_up(self):
        moves.saludo_up()

    def head_cicle(self):
        moves.head_cicle()

    def detener(self):
        self.ir_handler.detener()


# Función para iniciar la aplicación Tkinter
def main():
    root = tk.Tk()
    app = App(root)
    
    try:
        # Mantener la ventana de Tkinter abierta
        root.mainloop()
    except KeyboardInterrupt:
        app.detener()
        print("Programa terminado.")

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
