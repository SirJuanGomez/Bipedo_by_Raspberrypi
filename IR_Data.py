# ir_handler.py
import pigpio
import time

class IRHandler:
    def __init__(self, gpio_pin, callbacks):
        """
        gpio_pin: El pin GPIO donde está conectado el receptor IR (por ejemplo GPIO 17)
        callbacks: diccionario con funciones que se llaman al recibir cada señal IR
        """
        self.callbacks = callbacks
        self.gpio_pin = gpio_pin

        # Inicialización de pigpio
        self.pi = pigpio.pi()

        if not self.pi.connected:
            raise RuntimeError("No se puede conectar con pigpio")

        self.pi.set_mode(self.gpio_pin, pigpio.INPUT)
        self.pi.set_pull_up_down(self.gpio_pin, pigpio.PUD_UP)

        # Se registra para escuchar el código IR
        self.pi.callback(self.gpio_pin, pigpio.FALLING_EDGE, self.leer_ir)

        # Decodificación de código
        self.pulsos = []
        self.timeout = 1  # Tiempo para esperar antes de considerar la secuencia como fallida

    def leer_ir(self, gpio, level, tick):
        """
        Esta función se llama cada vez que se recibe una señal IR.
        Dependiendo del código IR recibido, se llama a un callback.
        """
        # Recibe los pulsos y los procesa
        self.pulsos.append(tick)

        # Verifica si es el final de una señal IR
        if len(self.pulsos) > 0 and (time.time() - self.pulsos[0]/1e6) > self.timeout:
            ir_code = self.obtener_codigo_ir()
            if ir_code:
                print(f">> Código IR recibido: {ir_code}")
                self.ejecutar_accion(ir_code)
            # Limpiar los pulsos después de procesarlos
            self.pulsos.clear()

    def obtener_codigo_ir(self):
        """
        Esta función decodifica la secuencia de pulsos IR en un código real utilizando el protocolo NEC.
        """
        # NEC se codifica de la siguiente forma:
        # 1. Inicia con un bit de inicio largo
        # 2. Sigue con 32 bits: 16 bits de dirección, 16 bits de datos (8 bits de dirección, 8 bits de datos)
        # Este código debería ser capaz de capturar una señal IR y extraer su código

        # Decodificar los pulsos utilizando el protocolo NEC.
        if len(self.pulsos) >= 68:  # NEC tiene 68 pulsos para la transmisión
            # Extraemos los bits de la secuencia de pulsos
            bits = []

            for i in range(1, len(self.pulsos), 2):
                # Mide el tiempo entre los pulsos
                duracion = self.pulsos[i] - self.pulsos[i-1]
                if duracion > 4000:  # Pulse largo (representa un "1")
                    bits.append(1)
                elif duracion > 1000:  # Pulse corto (representa un "0")
                    bits.append(0)

            # Verifica si tenemos 32 bits para el código de datos y dirección
            if len(bits) >= 32:
                # Tomamos los 32 bits del código
                direccion = bits[:16]  # Primeros 16 bits son la dirección
                datos = bits[16:]      # Últimos 16 bits son los datos

                # Convirtiendo los bits a un número binario
                direccion_binario = ''.join(str(bit) for bit in direccion)
                datos_binario = ''.join(str(bit) for bit in datos)

                # Convertimos las secuencias binarias a valores enteros
                direccion_decimal = int(direccion_binario, 2)
                datos_decimal = int(datos_binario, 2)

                # Aquí puedes manejar el código IR decodificado
                print(f"Dirección: {direccion_decimal}, Datos: {datos_decimal}")
                
                # Ahora verificamos qué código se recibió y ejecutamos las acciones correspondientes
                if datos_decimal == 0x10:  # Código para "pose_saludo"
                    return "pose_saludo"
                elif datos_decimal == 0x11:  # Código para "saludo_hands"
                    return "saludo_hands"
                elif datos_decimal == 0x12:  # Código para "saludo_up"
                    return "saludo_up"
                elif datos_decimal == 0x13:  # Código para "head_cicle"
                    return "head_cicle"

        return None  # Si no se recibe un código válido, retorna None

    def ejecutar_accion(self, ir_code):
        """Esta función ejecuta la acción correspondiente según el código IR recibido."""
        if ir_code == "pose_saludo":
            self.callbacks["pose_saludo"]()
        elif ir_code == "saludo_hands":
            self.callbacks["saludo_hands"]()
        elif ir_code == "saludo_up":
            self.callbacks["saludo_up"]()
        elif ir_code == "head_cicle":
            self.callbacks["head_cicle"]()

    def detener(self):
        """Detiene el receptor IR y cierra la conexión con pigpio."""
        self.pi.stop()
