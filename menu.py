import tkinter as tk


class Menu:
    def __init__(self, app):
        self.app = app
        self.elementos = []

    def mostrar(self):
        self.ocultar()
        c = self.app.canvas
        w = self.app.ancho
        h = self.app.alto

        titulo = c.create_text(
            w // 2,
            h // 3,
            text="FUSIÓN Y FISIÓN",
            fill="orange",
            font=("Arial", 32, "bold"),
        )

        estilo_boton = {
            "font": ("Arial", 16, "bold"),
            "bg": "#1e1e1e",
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

        btn_jugar = tk.Button(c, text="Jugar", command=self.app.ir_a_seleccion_niveles, **estilo_boton)
        btn_salir = tk.Button(c, text="Salir", command=self.app.salir_juego, **estilo_boton)

        win_jugar = c.create_window(w // 2, h // 2 - 20, window=btn_jugar)
        win_salir = c.create_window(w // 2, h // 2 + 50, window=btn_salir)

        self.elementos = [titulo, btn_jugar, btn_salir, win_jugar, win_salir]

    def ocultar(self):
        for item in self.elementos:
            if isinstance(item, tk.Widget):
                item.destroy()
            else:
                self.app.canvas.delete(item)
        self.elementos = []

    def actualizar(self):
        pass