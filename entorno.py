#PLACA
class PlacaPresion:
    def __init__(
        self,
        x1,
        y1,
        x2,
        y2,
        nombre_requerido,
        color_base,
        color_activa,
        barrera_objetivo=None,
        un_solo_uso=False,
        color_usada="#334155",
    ):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.nombre_requerido = nombre_requerido
        self.color_base = color_base
        self.color_activa = color_activa
        self.barrera_objetivo = barrera_objetivo
        self.un_solo_uso = un_solo_uso
        self.color_usada = color_usada
        self.activada = False
        self.usada = False
        self.item = None
        self.texto_item = None

    def comprobar(self, bolas, canvas=None):
        if self.un_solo_uso and self.usada:
            self.activada = True
            return

        if not self.un_solo_uso:
            self.activada = False

        for bola in bolas:
            cerca_x = bola.x + bola.radio >= self.x1 and bola.x - bola.radio <= self.x2
            cerca_y = bola.y + bola.radio >= self.y1 - 6 and bola.y - bola.radio <= self.y2
            if cerca_x and cerca_y and bola.nombre == self.nombre_requerido:
                self.activada = True
                if self.un_solo_uso:
                    self.usada = True
                    if self.barrera_objetivo is not None and canvas is not None:
                        self.barrera_objetivo.destruir(canvas)
                break

    def dibujar(self, canvas):
        if self.un_solo_uso and self.usada:
            color = self.color_usada
        else:
            color = self.color_activa if self.activada else self.color_base

        if self.item is None:
            self.item = canvas.create_rectangle(
                self.x1,
                self.y1,
                self.x2,
                self.y2,
                fill=color,
                outline="white",
                width=1,
            )
        else:
            canvas.itemconfig(self.item, fill=color)

        if self.un_solo_uso and self.usada:
            etiqueta = "USADA"
        elif self.activada:
            etiqueta = self.nombre_requerido
        else:
            etiqueta = ""

        centro_x = (self.x1 + self.x2) // 2
        arriba_y = self.y1 - 18

        if self.texto_item is None:
            self.texto_item = canvas.create_text(
                centro_x,
                arriba_y,
                text=etiqueta,
                fill="white",
                font=("Arial", 11, "bold"),
            )
        else:
            canvas.itemconfig(self.texto_item, text=etiqueta)

    def borrar(self, canvas):
        if self.item is not None:
            canvas.delete(self.item)
            self.item = None
        if self.texto_item is not None:
            canvas.delete(self.texto_item)
            self.texto_item = None

    def reiniciar(self, canvas):
        self.activada = False
        self.usada = False
        self.borrar(canvas)
        self.dibujar(canvas)

#PINCHOS
class Pinchos:
    def __init__(self, x1, y1, x2, y2, cantidad=5, color="#dc2626"):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.cantidad = max(1, cantidad)
        self.color = color
        self.items = []

    def colisiona_con_bolas(self, bolas):
        for bola in bolas:
            toca_x = bola.x + bola.radio >= self.x1 and bola.x - bola.radio <= self.x2
            toca_y = bola.y + bola.radio >= self.y1 and bola.y - bola.radio <= self.y2
            if toca_x and toca_y:
                return True
        return False

    def dibujar(self, canvas):
        if self.items:
            return

        ancho_total = self.x2 - self.x1
        ancho_pincho = ancho_total / self.cantidad

        for i in range(self.cantidad):
            px1 = self.x1 + i * ancho_pincho
            px2 = px1 + ancho_pincho
            punta_x = (px1 + px2) / 2
            triangulo = canvas.create_polygon(
                px1,
                self.y2,
                punta_x,
                self.y1,
                px2,
                self.y2,
                fill=self.color,
                outline="#fca5a5",
                width=1,
            )
            self.items.append(triangulo)

    def borrar(self, canvas):
        for item in self.items:
            canvas.delete(item)
        self.items = []

#PISO
class PisoFragil:
    def __init__(self, x1, y1, x2, y2, nombres_que_rompen=("fu", "fusion"), color="#7dd3fc", borde="#e0f2fe"):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.nombres_que_rompen = set(nombres_que_rompen)
        self.color = color
        self.borde = borde
        self.roto = False
        self.item = None

    def comprobar_y_romper(self, bolas, canvas):
        if self.roto:
            return False

        for bola in bolas:
            encima_x = bola.x + bola.radio >= self.x1 and bola.x - bola.radio <= self.x2
            toca_y = bola.y + bola.radio >= self.y1 - 4 and bola.y - bola.radio <= self.y2
            if encima_x and toca_y and bola.nombre in self.nombres_que_rompen:
                self.roto = True
                self.borrar(canvas)
                return True
        return False

    def dibujar(self, canvas):
        if self.roto or self.item is not None:
            return
        self.item = canvas.create_rectangle(
            self.x1,
            self.y1,
            self.x2,
            self.y2,
            fill=self.color,
            outline=self.borde,
            width=2,
        )

    def borrar(self, canvas):
        if self.item is not None:
            canvas.delete(self.item)
            self.item = None

    def reiniciar(self, canvas):
        self.roto = False
        self.borrar(canvas)
        self.dibujar(canvas)

#PUERTA
class Puerta:
    def __init__(
        self,
        x1,
        y1,
        x2,
        y2,
        color_borde="#78350f",
        color_cerrada="#78350f",
        color_abierta="#ffffff",
        grosor_borde=4,
    ):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color_borde = color_borde
        self.color_cerrada = color_cerrada
        self.color_abierta = color_abierta
        self.grosor_borde = grosor_borde
        self.abierta = False
        self.item = None

    def actualizar_estado(self, abierta):
        self.abierta = bool(abierta)

    def dibujar(self, canvas):
        relleno = self.color_abierta if self.abierta else self.color_cerrada
        if self.item is None:
            self.item = canvas.create_rectangle(
                self.x1,
                self.y1,
                self.x2,
                self.y2,
                fill=relleno,
                outline=self.color_borde,
                width=self.grosor_borde,
            )
        else:
            canvas.itemconfig(self.item, fill=relleno, outline=self.color_borde)

    def borrar(self, canvas):
        if self.item is not None:
            canvas.delete(self.item)
            self.item = None

#BLOQUES_ACTIVADORES
class Barrera:
    def __init__(self, x1, y1, x2, y2, color_relleno="#eab308", color_borde="#fef08a"):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color_relleno = color_relleno
        self.color_borde = color_borde
        self.destruida = False
        self.item = None

    def destruir(self, canvas):
        if not self.destruida:
            self.destruida = True
            self.borrar(canvas)

    def dibujar(self, canvas):
        if self.destruida or self.item is not None:
            return
        self.item = canvas.create_rectangle(
            self.x1,
            self.y1,
            self.x2,
            self.y2,
            fill=self.color_relleno,
            outline=self.color_borde,
            width=2,
        )

    def borrar(self, canvas):
        if self.item is not None:
            canvas.delete(self.item)
            self.item = None

    def reiniciar(self, canvas):
        self.destruida = False
        self.borrar(canvas)
        self.dibujar(canvas)

