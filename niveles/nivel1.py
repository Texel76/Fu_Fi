from entorno import Barrera, Pinchos, PisoFragil, PlacaPresion, Puerta
from personajes import SistemaJugadores


class Nivel1:
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

        alto_placa = 15
        ancho_placa = 20
        y_placa = self.suelo_y - alto_placa
        espacio = self.app.ancho // 4

        self.placa_fusion = PlacaPresion(
            espacio * 3 - ancho_placa // 2,
            y_placa,
            espacio * 3 + ancho_placa // 2,
            self.suelo_y,
            nombre_requerido="fusion",
            color_base="#d38b4f",
            color_activa="orange",
            un_solo_uso=True,
        )
        

        # Barreras y placas de un solo uso
        self.barreras = []
        self.placas = []

        ancho_barrera = 22
        alto_barrera = 95

        # 4 barreras amarillas de "fu"
        posiciones_fu = [
            espacio * 2 - 70,
            espacio * 2 + 40,
            espacio * 3 - 90,
            espacio * 3 + 50,
        ]
        for x_placa in posiciones_fu:
            barrera = Barrera(
                x_placa + 55,
                self.suelo_y - alto_barrera,
                x_placa + 55 + ancho_barrera,
                self.suelo_y,
                color_relleno="#eab308",
                color_borde="#fef08a",
            )
            placa = PlacaPresion(
                x_placa - ancho_placa // 2,
                y_placa,
                x_placa + ancho_placa // 2,
                self.suelo_y,
                nombre_requerido="fu",
                color_base="#d6c84c",
                color_activa="yellow",
                barrera_objetivo=barrera,
                un_solo_uso=True,
            )
            self.barreras.append(barrera)
            self.placas.append(placa)

        # 2 barreras rojas de "fi" (cada una con su propia placa de "fi")
        posiciones_fi = [
            espacio * 1 - 40,
            espacio * 1 + 65,
        ]
        for x_placa in posiciones_fi:
            barrera = Barrera(
                x_placa + 55,
                self.suelo_y - alto_barrera,
                x_placa + 55 + ancho_barrera,
                self.suelo_y,
                color_relleno="#ef4444",
                color_borde="#fecaca",
            )
            placa = PlacaPresion(
                x_placa - ancho_placa // 2,
                y_placa,
                x_placa + ancho_placa // 2,
                self.suelo_y,
                nombre_requerido="fi",
                color_base="#cd2f2f",
                color_activa="red",
                barrera_objetivo=barrera,
                un_solo_uso=True,
            )
            self.barreras.append(barrera)
            self.placas.append(placa)

        # Placa de "fusion" que abre la puerta
        self.placas.append(self.placa_fusion)

        alto_pinchos = 15
        ancho_pinchos = 0
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

        ancho_fragil = 140
        alto_fragil = 14
        x_fragil = espacio * 2
        y_fragil = self.suelo_y - 95
        self.pisos_fragiles = [
            PisoFragil(
                x_fragil - ancho_fragil // 2,
                y_fragil,
                x_fragil + ancho_fragil // 2,
                y_fragil + alto_fragil,
            )
        ]

        ancho_puerta = 65
        alto_puerta = 110
        x_puerta = self.app.ancho - 120
        self.puerta = Puerta(
            x_puerta - ancho_puerta // 2,
            self.suelo_y - alto_puerta,
            x_puerta + ancho_puerta // 2,
            self.suelo_y,
        )

    def _bloquear_barreras_activas(self):
        barreras_activas = [b for b in self.barreras if not b.destruida]
        if not barreras_activas:
            return

        for bola in self.jugadores.bolas_activas():
            for b in barreras_activas:
                cruza_y = bola.y + bola.radio > b.y1 and bola.y - bola.radio < b.y2
                if not cruza_y:
                    continue
                toca_x = bola.x + bola.radio > b.x1 and bola.x - bola.radio < b.x2
                if toca_x:
                    dist_izq = abs((bola.x + bola.radio) - b.x1)
                    dist_der = abs(b.x2 - (bola.x - bola.radio))
                    if dist_izq < dist_der:
                        bola.x = b.x1 - bola.radio
                    else:
                        bola.x = b.x2 + bola.radio

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
            text="NIVEL 1 | Placas: Roja = fi | Amarilla = fu | Naranja = fusion (abre puerta) | Cristal: solo fi | E: Dividir | ESC: Volver",
            fill="white",
            font=("Arial", 11, "bold"),
        )
        self.elementos = [plataforma, ayuda]

        for barrera in self.barreras:
            barrera.dibujar(c)
        for placa in self.placas:
            placa.dibujar(c)
        for pincho in self.pinchos:
            pincho.dibujar(c)
        for piso in self.pisos_fragiles:
            piso.dibujar(c)
        self.puerta.dibujar(c)
        self.jugadores.dibujar(c)

    def ocultar(self):
        for item in self.elementos:
            self.app.canvas.delete(item)
        self.elementos = []

        for barrera in self.barreras:
            barrera.borrar(self.app.canvas)
        for placa in self.placas:
            placa.borrar(self.app.canvas)
        for pincho in self.pinchos:
            pincho.borrar(self.app.canvas)
        for piso in self.pisos_fragiles:
            piso.borrar(self.app.canvas)
        self.puerta.borrar(self.app.canvas)
        self.jugadores.borrar(self.app.canvas)

    def actualizar(self):
        superficies = [
            (p.x1, p.y1, p.x2) for p in self.pisos_fragiles if not p.roto
        ]
        self.jugadores.actualizar(
            self.app.teclas,
            self.suelo_y,
            self.app.canvas,
            superficies=superficies,
        )
        self._bloquear_barreras_activas()
        activas = self.jugadores.bolas_activas()

        for pincho in self.pinchos:
            if pincho.colisiona_con_bolas(activas):
                self.jugadores.borrar(self.app.canvas)
                self.jugadores.reiniciar(self.inicio_x, self.inicio_y)
                for piso in self.pisos_fragiles:
                    piso.reiniciar(self.app.canvas)
                for barrera in self.barreras:
                    barrera.reiniciar(self.app.canvas)
                for placa in self.placas:
                    if placa.un_solo_uso:
                        placa.reiniciar(self.app.canvas)
                    else:
                        placa.activada = False
                self.puerta.actualizar_estado(False)
                self.puerta.dibujar(self.app.canvas)
                self.jugadores.dibujar(self.app.canvas)
                return

        for piso in self.pisos_fragiles:
            piso.comprobar_y_romper(activas, self.app.canvas)

        for placa in self.placas:
            placa.comprobar(activas, self.app.canvas)
            placa.dibujar(self.app.canvas)

        self.puerta.actualizar_estado(self.placa_fusion.activada)
        self.puerta.dibujar(self.app.canvas)

        self.jugadores.dibujar(self.app.canvas)