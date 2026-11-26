from entorno import Pinchos, PlacaPresion
from personajes import SistemaJugadores


class Nivel2:
    def __init__(self, app):
        self.app = app
        self.suelo_y = self.app.alto - 60
        self.elementos = []

        self.inicio_x = 180
        self.inicio_y = self.suelo_y - 40
        self.jugadores = SistemaJugadores(
            x=self.inicio_x,
            y=self.inicio_y,
            controles_fu=self.app.controles_fu,
            controles_fi=self.app.controles_fi,
        )

        alto_placa = 30
        ancho_placa = 20
        y_placa = self.suelo_y - alto_placa
        espacio = self.app.ancho // 4

        self.placas = [
            PlacaPresion(
                espacio * 1 - ancho_placa // 2,
                y_placa,
                espacio * 1 + ancho_placa // 2,
                self.suelo_y,
                nombre_requerido="fi",
                color_base="#cd2f2f",
                color_activa="red",
            ),
            PlacaPresion(
                espacio * 2 - ancho_placa // 2,
                y_placa,
                espacio * 2 + ancho_placa // 2,
                self.suelo_y,
                nombre_requerido="fu",
                color_base="#d6c84c",
                color_activa="yellow",
            ),
            PlacaPresion(
                espacio * 3 - ancho_placa // 2,
                y_placa,
                espacio * 3 + ancho_placa // 2,
                self.suelo_y,
                nombre_requerido="fusion",
                color_base="#d38b4f",
                color_activa="orange",
            ),
        ]

        alto_pinchos = 15
        ancho_pinchos = 100

        centro_pinchos = (espacio * 1 + espacio * 2) // 2
        self.pinchos = [
            Pinchos(
                centro_pinchos - ancho_pinchos // 2,
                self.suelo_y - alto_pinchos,
                centro_pinchos + ancho_pinchos // 2,
                self.suelo_y,
                cantidad=4,
            )
        ]

    def mostrar(self):
        self.ocultar()
        c = self.app.canvas
        w = self.app.ancho
        h = self.app.alto

        plataforma = c.create_rectangle(0, self.suelo_y, w, h, fill="#475569", outline="")
        ayuda = c.create_text(
            20,
            25,
            anchor="w",
            text="NIVEL 1 | Placas: Roja = fi | Amarilla = fu | Naranja = fusion | Dividir: E | ESC: Volver",
            fill="white",
            font=("Arial", 11, "bold"),
        )
        self.elementos = [plataforma, ayuda]

        for placa in self.placas:
            placa.dibujar(c)
        for pincho in self.pinchos:
            pincho.dibujar(c)
        self.jugadores.dibujar(c)

    def ocultar(self):
        for item in self.elementos:
            self.app.canvas.delete(item)
        self.elementos = []

        for placa in self.placas:
            placa.borrar(self.app.canvas)
        for pincho in self.pinchos:
            pincho.borrar(self.app.canvas)
        self.jugadores.borrar(self.app.canvas)

    def actualizar(self):
        self.jugadores.actualizar(self.app.teclas, self.suelo_y, self.app.canvas)
        activas = self.jugadores.bolas_activas()

        for pincho in self.pinchos:
            if pincho.colisiona_con_bolas(activas):
                self.jugadores.borrar(self.app.canvas)
                self.jugadores.reiniciar(self.inicio_x, self.inicio_y)
                self.jugadores.dibujar(self.app.canvas)
                return

        for placa in self.placas:
            placa.comprobar(activas)
            placa.dibujar(self.app.canvas)

        self.jugadores.dibujar(self.app.canvas)