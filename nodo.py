# ──────────────────────────────────────────────────────────
#  CLASE NODO
# ──────────────────────────────────────────────────────────

class NodoCaso:
    """Nodo individual del árbol AVL. Representa un caso de ciberacoso."""

    def __init__(self, id_caso, tipo_acoso, gravedad, evidencias, ley, pena, descripcion=""):
        # Datos del caso
        self.id_caso     = id_caso
        self.tipo_acoso  = tipo_acoso
        self.gravedad    = gravedad        # clave del árbol
        self.evidencias  = evidencias      # lista de strings
        self.ley         = ley
        self.pena        = pena
        self.descripcion = descripcion

        # Punteros del árbol
        self.izquierdo = None
        self.derecho   = None
        self.altura    = 1

    def __repr__(self):
        return f"Caso({self.id_caso}, grav={self.gravedad})"
