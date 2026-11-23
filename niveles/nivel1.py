import tkinter as tk

ANCHO, ALTO = 800, 600
FPS_MS = 16

class NivelTemplate(tk.Toplevel): # Usamos Toplevel para abrirlo desde el selector
    def __init__(self, parent, tiempo_limite_seg=30, callback_regresar=None):
        super().__init__(parent)
        self.title("Nivel del Juego - Unir Bolas")
        self.geometry(f"{ANCHO}x{ALTO}")
        self.resizable(False, False)
        
        self.callback_regresar = callback_regresar
        
        # Canvas principal (similar a tu taller)
        self.canvas = tk.Canvas(self, width=ANCHO, height=ALTO, bg="#0B1220", highlightthickness=0)
        self.canvas.pack()

        # Control de tiempo (Límite)
        self.tiempo_limite = tiempo_limite_seg * 1000 # Convertido a milisegundos
        self.tiempo_inicio = tk.IntVar(value=tiempo_limite_seg)
        
        # Textos en pantalla (Interfaz)
        self.txt_tiempo = self.canvas.create_text(
            ANCHO - 80, 30, fill="#E6EDF5", font=("Helvetica", 14, "bold"), text=f"Tiempo: {tiempo_limite_seg}s"
        )
        
        # Variables de estado
        self.en_pausa = False
        self.terminado = False
        self.bolas_unidas = False

        # --- AQUÍ LLAMAS A TUS PERSONAJES DESDE EL OTRO ARCHIVO ---
        # Ejemplo: from personajes import DobleBola
        # self.jugadores = DobleBola(self.canvas)
        
        # Controles simultáneos (ejemplo con flechas o WASD)
        self.bind("<KeyPress>", self.tecla_presionada)
        self.bind("<KeyRelease>", self.tecla_soltada)

        # Iniciar temporizadores y bucle de juego
        self.iniciar_tiempo()
        self.paso()

    def iniciar_tiempo(self):
        """Maneja la cuenta regresiva del nivel."""
        if self.terminado or self.en_pausa:
            return
        
        if self.tiempo_limite > 0:
            self.tiempo_limite -= 1000
            self.tiempo_set = self.tiempo_limite // 1000
            self.canvas.itemconfig(self.txt_tiempo, text=f"Tiempo: {self.tiempo_set}s")
            self.after(1000, self.iniciar_tiempo)
        else:
            self.fallar_nivel("¡Se acabó el tiempo!\nReiniciando nivel...")

    def tecla_presionada(self, event):
        # Controlar ambas bolas simultáneamente según la tecla
        if event.keysym in ["Left", "Right", "Up", "Down", "a", "d", "w", "s"]:
            # self.jugadores.mover(event.keysym)
            pass

    def tecla_soltada(self, event):
        # Detener movimiento si es necesario
        pass

    def actualizar(self):
        if self.en_pausa or self.terminado:
            return

        # 1. Actualizar posición de las bolas
        # self.jugadores.actualizar()

        # 2. Comprobar si ambas bolas se han unido
        # if self.jugadores.verificar_union():
        #     self.bolas_unidas = True

        # 3. Comprobar si llegaron al mecanismo final con la condición cumplida
        # if self.verificar_meta() and self.bolas_unidas:
        #     self.ganar_nivel()

    def paso(self):
        """Bucle principal idéntico al de tu taller."""
        self.actualizar()
        if not self.terminado:
            self.after(FPS_MS, self.paso)

    def fallar_nivel(self, mensaje):
        self.terminado = True
        self.canvas.create_text(
            ANCHO / 2, ALTO / 2, text=mensaje, fill="#F43F5E", font=("Helvetica", 20, "bold"), justify="center"
        )
        # Reiniciar el nivel después de 2 segundos
        self.after(2000, self.reiniciar_nivel)

    def reiniciar_nivel(self):
        self.destroy()
        # Volver a instanciar el nivel actual

    def ganar_nivel(self):
        self.terminado = True
        self.canvas.create_text(
            ANCHO / 2, ALTO / 2, text="¡Nivel Superado!", fill="#55F765", font=("Helvetica", 22, "bold")
        )
        self.after(2000, self.destroy)