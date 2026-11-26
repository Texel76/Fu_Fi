import tkinter as tk
from menu import Menu
from niveles.nivel1 import Nivel1
from niveles.nivel2 import Nivel2
from controles import controles_fu, controles_fi

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Fusión y Fisión")
        self.root.attributes("-fullscreen", True)

        self.ancho = root.winfo_screenwidth()
        self.alto = root.winfo_screenheight()

        self.canvas = tk.Canvas(
            root,
            width=self.ancho,
            height=self.alto,
            bg="black",
            highlightthickness=0,
        )

        self.canvas.pack(fill="both", expand=True)

        self.teclas = set()
        self.modo = "menu"
        self.elementos_seleccion = []
        self.controles_fu = controles_fu
        self.controles_fi = controles_fi
        self.niveles = {
            1: Nivel1(self),
            2: Nivel2(self),
        }
        self.nivel_actual = None

        self.menu = Menu(self)
        self.menu.mostrar()

        root.bind("<KeyPress>", self.tecla_abajo)
        root.bind("<KeyRelease>", self.tecla_arriba)
        self.bucle()

    def ocultar_nivel_actual(self):
        if self.nivel_actual is not None:
            self.nivel_actual.ocultar()
            self.nivel_actual = None
    
    def limpiar_seleccion_niveles(self):
        for item in self.elementos_seleccion:
            if isinstance(item, tk.Widget):
                item.destroy()
            else:
                self.canvas.delete(item)
        self.elementos_seleccion = []

    def ir_a_menu(self):
        self.modo = "menu"
        self.limpiar_seleccion_niveles()
        self.ocultar_nivel_actual()
        self.menu.mostrar()

    def ir_a_seleccion_niveles(self):
        self.menu.ocultar()
        self.ocultar_nivel_actual()
        self.limpiar_seleccion_niveles()
        self.modo = "seleccion_niveles"

        w = self.ancho
        h = self.alto
        texto = self.canvas.create_text(
            w // 2,
            h // 4,
            text="SELECCIÓN DE NIVELES",
            fill="orange",
            font=("Arial", 28, "bold"),
        )
        self.elementos_seleccion = [texto]

        estilo_boton = {
            "font": ("Arial", 16, "bold"),
            "bg": "#000000",
            "fg": "orange",
            "activebackground": "orange",
            "activeforeground": "black",
            "relief": "flat",
            "highlightthickness": 1,
            "highlightbackground": "orange",
            "padx": 24,
            "pady": 8,
            "cursor": "hand2",
        }

        # Un botón por cada nivel del diccionario
        for i, numero in enumerate(self.niveles):
            boton = tk.Button(
                self.canvas,
                text=f"Nivel {numero}",
                command=lambda n=numero: self.ir_a_nivel(n),
                **estilo_boton,
            )
            ventana = self.canvas.create_window(w // 2, h // 2 - 20 + i * 70, window=boton)
            self.elementos_seleccion += [boton, ventana]

        btn_volver = tk.Button(
            self.canvas,
            text="Volver",
            command=self.ir_a_menu,
            **estilo_boton,
        )
        win_volver = self.canvas.create_window(w // 2, h - 100, window=btn_volver)
        self.elementos_seleccion += [btn_volver, win_volver]

    def ir_a_nivel(self, numero):
        self.menu.ocultar()
        self.limpiar_seleccion_niveles()
        self.modo = "nivel"
        self.nivel_actual = self.niveles[numero]
        self.nivel_actual.mostrar()

    def salir_juego(self):
        self.root.quit()
        self.root.destroy()

    def tecla_abajo(self, evento):
        tecla = evento.keysym.lower()
        self.teclas.add(tecla)
        if tecla == "escape":
            if self.modo == "seleccion_niveles":
                self.ir_a_menu()
            elif self.modo != "menu":
                self.ir_a_seleccion_niveles()
        elif tecla == "e" and self.modo == "nivel":
            self.nivel_actual.jugadores.alternar_division(self.canvas)



    def tecla_arriba(self, evento):
        self.teclas.discard(evento.keysym.lower())

    def bucle(self):
        if self.modo == "menu":
            self.menu.actualizar()
        elif self.modo == "nivel":
            self.nivel_actual.actualizar()

        self.root.after(16, self.bucle)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()