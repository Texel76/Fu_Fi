class PlacaPresion:
    def __init__(self, x1, y1, x2, y2, nombre_requerido, color_base, color_activa):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.nombre_requerido = nombre_requerido
        self.color_base = color_base
        self.color_activa = color_activa
        self.activada = False
        self.item = None
        self.texto_item = None

    def comprobar(self, bolas):
        self.activada = False
        for bola in bolas:
            cerca_x = bola.x + bola.radio >= self.x1 and bola.x - bola.radio <= self.x2
            cerca_y = bola.y + bola.radio >= self.y1 - 6 and bola.y - bola.radio <= self.y2
            if cerca_x and cerca_y and bola.nombre == self.nombre_requerido:
                self.activada = True
                break

    def dibujar(self, canvas):
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

        etiqueta = self.nombre_requerido if self.activada else ""
        centro_x = (self.x1 + self.x2) // 2
        arriba_y = self.y1 - 18

        if self.texto_item is None:
            self.texto_item = canvas.create_text(
                centro_x,
                arriba_y,
                text=etiqueta,
                fill="white",
                font=("Arial", 13, "bold"),
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