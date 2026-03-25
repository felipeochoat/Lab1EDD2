"""
arbol.py
Árbol Binario de Búsqueda (ABB) - versión Python
Equivalente a Arbol.java, sin balanceo AVL.
"""

from nodo import Nodo


class Arbol:
    def __init__(self):
        self.raiz = None

    # ------------------------------------------------------------------ #
    #  INSERTAR                                                            #
    # ------------------------------------------------------------------ #
    def insertar(self, dato: int):
        """Inserta un valor en el ABB (sin balanceo)."""
        self.raiz = self._insertar_rec(self.raiz, dato)

    def _insertar_rec(self, nodo: Nodo, dato: int) -> Nodo:
        if nodo is None:
            return Nodo(dato)
        if dato < nodo.dato:
            nodo.izquierdo = self._insertar_rec(nodo.izquierdo, dato)
        elif dato > nodo.dato:
            nodo.derecho = self._insertar_rec(nodo.derecho, dato)
        # si dato == nodo.dato, no se insertan duplicados
        return nodo

    # ------------------------------------------------------------------ #
    #  ELIMINAR                                                            #
    # ------------------------------------------------------------------ #
    def eliminar(self, dato: int):
        """Elimina un valor del ABB."""
        self.raiz = self._eliminar_rec(self.raiz, dato)

    def _eliminar_rec(self, nodo: Nodo, dato: int) -> Nodo:
        if nodo is None:
            return None
        if dato < nodo.dato:
            nodo.izquierdo = self._eliminar_rec(nodo.izquierdo, dato)
        elif dato > nodo.dato:
            nodo.derecho = self._eliminar_rec(nodo.derecho, dato)
        else:
            # Nodo encontrado
            if nodo.izquierdo is None:
                return nodo.derecho
            elif nodo.derecho is None:
                return nodo.izquierdo
            # Nodo con dos hijos: reemplazar con el sucesor (mínimo del subárbol derecho)
            sucesor = self._min_valor(nodo.derecho)
            nodo.dato = sucesor
            nodo.derecho = self._eliminar_rec(nodo.derecho, sucesor)
        return nodo

    def _min_valor(self, nodo: Nodo) -> int:
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual.dato

    # ------------------------------------------------------------------ #
    #  BUSCAR                                                              #
    # ------------------------------------------------------------------ #
    def buscar(self, dato: int) -> bool:
        """Retorna True si el valor existe en el árbol."""
        return self._buscar_rec(self.raiz, dato)

    def _buscar_rec(self, nodo: Nodo, dato: int) -> bool:
        if nodo is None:
            return False
        if dato == nodo.dato:
            return True
        if dato < nodo.dato:
            return self._buscar_rec(nodo.izquierdo, dato)
        return self._buscar_rec(nodo.derecho, dato)

    # ------------------------------------------------------------------ #
    #  RECORRIDOS (devuelven listas, útil para pygame)                    #
    # ------------------------------------------------------------------ #
    def inorden(self) -> list:
        resultado = []
        self._inorden_rec(self.raiz, resultado)
        return resultado

    def _inorden_rec(self, nodo: Nodo, resultado: list):
        if nodo:
            self._inorden_rec(nodo.izquierdo, resultado)
            resultado.append(nodo.dato)
            self._inorden_rec(nodo.derecho, resultado)

    def preorden(self) -> list:
        resultado = []
        self._preorden_rec(self.raiz, resultado)
        return resultado

    def _preorden_rec(self, nodo: Nodo, resultado: list):
        if nodo:
            resultado.append(nodo.dato)
            self._preorden_rec(nodo.izquierdo, resultado)
            self._preorden_rec(nodo.derecho, resultado)

    def postorden(self) -> list:
        resultado = []
        self._postorden_rec(self.raiz, resultado)
        return resultado

    def _postorden_rec(self, nodo: Nodo, resultado: list):
        if nodo:
            self._postorden_rec(nodo.izquierdo, resultado)
            self._postorden_rec(nodo.derecho, resultado)
            resultado.append(nodo.dato)

    # ------------------------------------------------------------------ #
    #  ALTURA                                                              #
    # ------------------------------------------------------------------ #
    def altura(self) -> int:
        return self._altura_rec(self.raiz)

    def _altura_rec(self, nodo: Nodo) -> int:
        if nodo is None:
            return 0
        return 1 + max(self._altura_rec(nodo.izquierdo),
                       self._altura_rec(nodo.derecho))

    # ------------------------------------------------------------------ #
    #  POSICIONES PARA DIBUJAR (pygame)                                   #
    # ------------------------------------------------------------------ #
    def obtener_posiciones(self, ancho_pantalla: int, altura_pantalla: int) -> dict:
        """
        Calcula las coordenadas (x, y) de cada nodo para dibujarlos en pygame.
        Retorna un dict: { id(nodo): (x, y, nodo) }
        """
        posiciones = {}
        if self.raiz is None:
            return posiciones
        radio_nodo = 25
        margen_y = 70
        self._calcular_pos(self.raiz, ancho_pantalla // 2, 60,
                           ancho_pantalla // 4, margen_y,
                           posiciones, radio_nodo)
        return posiciones

    def _calcular_pos(self, nodo, x, y, offset_x, offset_y, posiciones, radio):
        if nodo is None:
            return
        posiciones[id(nodo)] = (x, y, nodo)
        if nodo.izquierdo:
            self._calcular_pos(nodo.izquierdo,
                               x - offset_x, y + offset_y,
                               max(offset_x // 2, radio + 5), offset_y,
                               posiciones, radio)
        if nodo.derecho:
            self._calcular_pos(nodo.derecho,
                               x + offset_x, y + offset_y,
                               max(offset_x // 2, radio + 5), offset_y,
                               posiciones, radio)
