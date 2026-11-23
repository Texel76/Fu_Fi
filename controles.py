class Controles:
    def __init__(self, izq, der, arr, aba, accion=None):
        self.izq = izq
        self.der = der
        self.arr = arr
        self.aba = aba
        self.accion = accion

    def mover_x(self, teclas):
        dx = 0
        if self.izq in teclas:
            dx -= 1
        if self.der in teclas:
            dx += 1
        return dx

    def mover_y(self, teclas):
        dy = 0
        if self.arr in teclas:
            dy -= 1
        if self.aba in teclas:
            dy += 1
        return dy


controles_fu = Controles("a", "d", "w", "s", accion="e")
controles_fi = Controles("left", "right", "up", "down", accion="e")