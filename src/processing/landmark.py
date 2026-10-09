class Landmark:

    def __init__(self, nombre, indice, x, y, z, tipo, lateralidad=None, visibilidad=None):
        self.nombre = nombre
        self.indice = indice
        self.x = x
        self.y = y
        self.z = z
        self.tipo = tipo
        self.lateralidad = lateralidad
        self.visibilidad = visibilidad