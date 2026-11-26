import tkinter as tk
from menu import Menu
from niveles.nivel1 import Nivel1
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
        self.nivel1 = Nivel1(self)

        self.menu = Menu(self)
        self.menu.mostrar()

        root.bind("<KeyPress>", self.tecla_abajo)
        root.bind("<KeyRelease>", self.tecla_arriba)

        self._after_id = None
        self.bucle()

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
        if self.nivel1 is not None:
            self.nivel1.ocultar()
        self.menu.mostrar()

    def ir_a_seleccion_niveles(self):
        self.menu.ocultar()
        if self.nivel1 is not None:
            self.nivel1.ocultar()
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

        btn_nivel1 = tk.Button(
            self.canvas,
            text="Nivel 1",
            command=self.ir_a_nivel1,
            **estilo_boton,
        )
        btn_volver = tk.Button(
            self.canvas,
            text="Volver",
            command=self.ir_a_menu,
            **estilo_boton,
        )

        win_nivel1 = self.canvas.create_window(w // 2, h // 2 - 20, window=btn_nivel1)
        win_volver = self.canvas.create_window(w // 2, h - 100, window=btn_volver)
        self.elementos_seleccion = [texto, btn_nivel1, btn_volver, win_nivel1, win_volver]

    def ir_a_nivel1(self):
        self.menu.ocultar()
        self.limpiar_seleccion_niveles()
        self.modo = "nivel1"
        if self.nivel1 is not None:
            self.nivel1.mostrar()

    def salir_juego(self):
        if self._after_id is not None:
            self.root.after_cancel(self._after_id)
            self._after_id = None
        self.root.destroy()
        self.root.quit()

    def tecla_abajo(self, evento):
        tecla = evento.keysym.lower()
        self.teclas.add(tecla)
        if tecla == "escape":
            if self.modo == "seleccion_niveles":
                self.ir_a_menu()
            elif self.modo != "menu":
                self.ir_a_seleccion_niveles()
        elif tecla == "e" and self.modo == "nivel1" and self.nivel1 is not None:
            self.nivel1.jugadores.alternar_division(self.canvas)

    def tecla_arriba(self, evento):
        self.teclas.discard(evento.keysym.lower())

    def bucle(self):
        if self.modo == "menu":
            self.menu.actualizar()
        elif self.modo == "nivel1" and self.nivel1 is not None:
            self.nivel1.actualizar()

        self._after_id = self.root.after(16, self.bucle)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()