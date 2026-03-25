"""
nodo.py
Clase Nodo para el Árbol Binario de Búsqueda (ABB)
Equivalente a Nodo.java
"""

class Nodo:
    def __init__(self, dato: int):
        self.dato = dato
        self.izquierdo = None   # hijo izquierdo
        self.derecho = None     # hijo derecho
