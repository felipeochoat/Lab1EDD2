# ──────────────────────────────────────────────────────────
#  NodoCaso vive en nodo.py (clases separadas por requerimiento)
# ──────────────────────────────────────────────────────────
from nodo import NodoCaso  # noqa: F401 – reexportado para compatibilidad


# ──────────────────────────────────────────────────────────
#  CLASE ÁRBOL AVL
# ──────────────────────────────────────────────────────────
class ArbolAVL:
    def __init__(self):
        self.raiz = None
        self.ultimo_insertado = None    # para animaciones
        self.rotaciones = []            # log de rotaciones recientes

    # ──────────────────────────────────────────
    #  ALTURA Y BALANCE
    # ──────────────────────────────────────────
    def _altura(self, nodo):
        return nodo.altura if nodo else 0

    def _actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self._altura(nodo.izquierdo),
                              self._altura(nodo.derecho))

    def _balance(self, nodo):
        return self._altura(nodo.izquierdo) - self._altura(nodo.derecho) if nodo else 0

    # ──────────────────────────────────────────
    #  ROTACIONES
    # ──────────────────────────────────────────
    def _rotar_derecha(self, z):
        y = z.izquierdo
        T3 = y.derecho
        y.derecho = z
        z.izquierdo = T3
        self._actualizar_altura(z)
        self._actualizar_altura(y)
        self.rotaciones.append(("derecha", y.gravedad))
        return y

    def _rotar_izquierda(self, z):
        y = z.derecho
        T2 = y.izquierdo
        y.izquierdo = z
        z.derecho = T2
        self._actualizar_altura(z)
        self._actualizar_altura(y)
        self.rotaciones.append(("izquierda", y.gravedad))
        return y

    def _balancear(self, nodo, gravedad):
        self._actualizar_altura(nodo)
        balance = self._balance(nodo)

        # Caso LL
        if balance > 1 and gravedad < nodo.izquierdo.gravedad:
            return self._rotar_derecha(nodo)
        # Caso RR
        if balance < -1 and gravedad > nodo.derecho.gravedad:
            return self._rotar_izquierda(nodo)
        # Caso LR
        if balance > 1 and gravedad > nodo.izquierdo.gravedad:
            nodo.izquierdo = self._rotar_izquierda(nodo.izquierdo)
            return self._rotar_derecha(nodo)
        # Caso RL
        if balance < -1 and gravedad < nodo.derecho.gravedad:
            nodo.derecho = self._rotar_derecha(nodo.derecho)
            return self._rotar_izquierda(nodo)
        return nodo

    # ──────────────────────────────────────────
    #  INSERTAR
    # ──────────────────────────────────────────
    def insertar(self, caso: NodoCaso):
        self.rotaciones = []
        self.raiz = self._insertar_rec(self.raiz, caso)
        self.ultimo_insertado = caso

    def _insertar_rec(self, nodo, caso):
        if nodo is None:
            return caso
        if caso.gravedad < nodo.gravedad:
            nodo.izquierdo = self._insertar_rec(nodo.izquierdo, caso)
        elif caso.gravedad > nodo.gravedad:
            nodo.derecho = self._insertar_rec(nodo.derecho, caso)
        else:
            # Gravedad igual → actualiza el nodo existente
            nodo.evidencias.extend(caso.evidencias)
            return nodo
        return self._balancear(nodo, caso.gravedad)

    # ──────────────────────────────────────────
    #  BUSCAR
    # ──────────────────────────────────────────
    def buscar(self, gravedad):
        return self._buscar_rec(self.raiz, gravedad)

    def _buscar_rec(self, nodo, gravedad):
        if nodo is None:
            return None
        if gravedad == nodo.gravedad:
            return nodo
        if gravedad < nodo.gravedad:
            return self._buscar_rec(nodo.izquierdo, gravedad)
        return self._buscar_rec(nodo.derecho, gravedad)

    # ──────────────────────────────────────────
    #  RECORRIDOS
    # ──────────────────────────────────────────
    def inorden(self):
        resultado = []
        self._inorden_rec(self.raiz, resultado)
        return resultado

    def _inorden_rec(self, nodo, res):
        if nodo:
            self._inorden_rec(nodo.izquierdo, res)
            res.append(nodo)
            self._inorden_rec(nodo.derecho, res)

    def todos_los_nodos(self):
        #Retorna lista de todos los nodos (inorden).
        return self.inorden()

    # ──────────────────────────────────────────
    #  POSICIONES PARA DIBUJAR
    # ──────────────────────────────────────────
    def obtener_posiciones(self, area_x, area_y, area_ancho, area_alto):
        #Calcula coordenadas (x, y) de cada nodo.
        #Retorna dict: { id(nodo): (x, y, nodo) }

        posiciones = {}
        if self.raiz is None:
            return posiciones
        offset_y = min(80, area_alto // (self._altura(self.raiz) + 1))
        self._calcular_pos(
            self.raiz,
            area_x + area_ancho // 2,
            area_y + 50,
            area_ancho // 4,
            offset_y,
            posiciones,
            30
        )
        return posiciones

    def _calcular_pos(self, nodo, x, y, offset_x, offset_y, posiciones, radio):
        if nodo is None:
            return
        posiciones[id(nodo)] = (x, y, nodo)
        if nodo.izquierdo:
            self._calcular_pos(nodo.izquierdo, x - offset_x, y + offset_y,
                               max(offset_x // 2, radio + 5), offset_y, posiciones, radio)
        if nodo.derecho:
            self._calcular_pos(nodo.derecho, x + offset_x, y + offset_y,
                               max(offset_x // 2, radio + 5), offset_y, posiciones, radio)

    def altura(self):
        return self._altura(self.raiz)
