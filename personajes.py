GRAVEDAD = 0.6
SALTO_BASE = -14.0


class Bola:
    def __init__(self, nombre, x, y, radio, color, multiplicador_salto=1.0, velocidad=5):
        self.nombre = nombre
        self.x = x
        self.y = y
        self.radio = radio
        self.color = color
        self.multiplicador_salto = multiplicador_salto
        self.velocidad = velocidad
        self.vy = 0.0
        self.en_suelo = False
        self.item = None

    def mover_horizontal(self, teclas, tecla_izq, tecla_der):
        dx = 0
        if tecla_izq in teclas:
            dx -= 1
        if tecla_der in teclas:
            dx += 1
        self.x += dx * self.velocidad

    def intentar_saltar(self, teclas, teclas_salto):
        salta = any(t in teclas for t in teclas_salto)
        if salta and self.en_suelo:
            self.vy = SALTO_BASE * self.multiplicador_salto
            self.en_suelo = False

    def aplicar_gravedad(self, suelo_y):
        self.vy += GRAVEDAD
        self.y += self.vy

        if self.y + self.radio >= suelo_y:
            self.y = suelo_y - self.radio
            self.vy = 0.0
            self.en_suelo = True
        else:
            self.en_suelo = False

    def dibujar(self, canvas):
        x1 = self.x - self.radio
        y1 = self.y - self.radio
        x2 = self.x + self.radio
        y2 = self.y + self.radio

        if self.item is None:
            self.item = canvas.create_oval(x1, y1, x2, y2, fill=self.color, outline="")
        else:
            canvas.coords(self.item, x1, y1, x2, y2)

    def borrar(self, canvas):
        if self.item is not None:
            canvas.delete(self.item)
            self.item = None


class SistemaJugadores:
    def __init__(self, x, y, controles_fu, controles_fi):
        self.controles_fu = controles_fu
        self.controles_fi = controles_fi
        self.dividido = False

        self.fusion = Bola("fusion", x, y, radio=32, color="orange", multiplicador_salto=0.0, velocidad=3)
        self.fu = Bola("fu", x - 35, y, radio=28, color="yellow", multiplicador_salto=0.5, velocidad=4)
        self.fi = Bola("fi", x + 35, y, radio=15, color="red", multiplicador_salto=1.0, velocidad=6)

    def bolas_activas(self):
        if not self.dividido:
            return [self.fusion]
        return [self.fu, self.fi]

    def reiniciar(self, x, y):
        self.dividido = False
        self.fusion.x = x
        self.fusion.y = y
        self.fusion.vy = 0.0
        self.fusion.en_suelo = False

        self.fu.x = x - 35
        self.fu.y = y
        self.fu.vy = 0.0
        self.fu.en_suelo = False

        self.fi.x = x + 35
        self.fi.y = y
        self.fi.vy = 0.0
        self.fi.en_suelo = False

    def alternar_division(self, canvas):
        # Solo permite dividir cuando están juntos (fusionados)
        if not self.dividido:
            self.fusion.borrar(canvas)
            self.fu.x = self.fusion.x - 35
            self.fu.y = self.fusion.y
            self.fu.vy = self.fusion.vy
            self.fu.en_suelo = self.fusion.en_suelo

            self.fi.x = self.fusion.x + 35
            self.fi.y = self.fusion.y
            self.fi.vy = self.fusion.vy
            self.fi.en_suelo = self.fusion.en_suelo
            self.dividido = True

    def _comprobar_fusion_automatica(self, canvas):
        if not self.dividido:
            return

        dx = self.fi.x - self.fu.x
        dy = self.fi.y - self.fu.y
        distancia = (dx ** 2 + dy ** 2) ** 0.5
        distancia_contacto = self.fu.radio + self.fi.radio

        if distancia <= distancia_contacto:
            self.fu.borrar(canvas)
            self.fi.borrar(canvas)
            self.fusion.x = (self.fu.x + self.fi.x) / 2
            self.fusion.y = min(self.fu.y, self.fi.y)
            self.fusion.vy = min(self.fu.vy, self.fi.vy)
            self.fusion.en_suelo = False
            self.dividido = False

    def actualizar(self, teclas, suelo_y, canvas=None):
        if not self.dividido:
            izq = self.controles_fu.izq if self.controles_fu.izq in teclas else self.controles_fi.izq
            der = self.controles_fu.der if self.controles_fu.der in teclas else self.controles_fi.der
            self.fusion.mover_horizontal(teclas, izq, der)
            self.fusion.intentar_saltar(teclas, (self.controles_fu.arr, self.controles_fi.arr))
            self.fusion.aplicar_gravedad(suelo_y)
        else:
            self.fu.mover_horizontal(teclas, self.controles_fu.izq, self.controles_fu.der)
            self.fu.intentar_saltar(teclas, (self.controles_fu.arr,))
            self.fu.aplicar_gravedad(suelo_y)

            self.fi.mover_horizontal(teclas, self.controles_fi.izq, self.controles_fi.der)
            self.fi.intentar_saltar(teclas, (self.controles_fi.arr,))
            self.fi.aplicar_gravedad(suelo_y)

            if canvas is not None:
                self._comprobar_fusion_automatica(canvas)

    def dibujar(self, canvas):
        if not self.dividido:
            self.fusion.dibujar(canvas)
        else:
            self.fu.dibujar(canvas)
            self.fi.dibujar(canvas)

    def borrar(self, canvas):
        self.fusion.borrar(canvas)
        self.fu.borrar(canvas)
        self.fi.borrar(canvas)