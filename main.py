"""
main.py
Visualizador de Árbol Binario de Búsqueda (ABB) con Pygame
Equivalente a ArbolAVL.java (clase principal)

Requisitos:
    pip install pygame

Controles:
    - Escribe un número y presiona ENTER  → inserta el nodo
    - Escribe un número y presiona DELETE → elimina el nodo
    - Escribe un número y presiona B      → busca el nodo (lo resalta)
    - Presiona ESC                        → limpia el campo de texto
"""

import pygame
import sys
from arbol import Arbol

# ─────────────────────────────────────────────
#  CONFIGURACIÓN
# ─────────────────────────────────────────────
ANCHO, ALTO = 1100, 700
FPS = 60
RADIO_NODO = 26

# Paleta de colores
COLOR_FONDO        = (15,  20,  35)
COLOR_NODO         = (52,  152, 219)
COLOR_NODO_BORDE   = (41,  128, 185)
COLOR_NODO_BUSQ    = (46,  204, 113)   # verde: encontrado
COLOR_NODO_NOBUSQ  = (231, 76,  60)    # rojo: no encontrado
COLOR_LINEA        = (100, 130, 180)
COLOR_TEXTO_NODO   = (255, 255, 255)
COLOR_PANEL        = (25,  35,  55)
COLOR_INPUT_BG     = (35,  50,  75)
COLOR_INPUT_BORDE  = (80,  120, 180)
COLOR_ACENTO       = (255, 200, 60)
COLOR_TEXTO_UI     = (200, 220, 255)
COLOR_GRIS         = (120, 140, 170)

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Árbol Binario de Búsqueda — ABB Visualizer")
reloj = pygame.time.Clock()

fuente_nodo  = pygame.font.SysFont("consolas", 14, bold=True)
fuente_ui    = pygame.font.SysFont("consolas", 16)
fuente_titulo = pygame.font.SysFont("consolas", 22, bold=True)
fuente_info  = pygame.font.SysFont("consolas", 13)

# ─────────────────────────────────────────────
#  ESTADO
# ─────────────────────────────────────────────
arbol = Arbol()
texto_entrada = ""
mensaje = "Bienvenido. Inserta valores en el árbol."
color_mensaje = COLOR_ACENTO
nodo_resaltado = None   # id de nodo buscado
busqueda_exitosa = None # True/False/None

# Carga inicial de ejemplo
for v in [50, 30, 70, 20, 40, 60, 80]:
    arbol.insertar(v)

# ─────────────────────────────────────────────
#  FUNCIONES DE DIBUJO
# ─────────────────────────────────────────────

def dibujar_aristas(posiciones: dict):
    """Dibuja las líneas entre padre e hijo."""
    for nid, (x, y, nodo) in posiciones.items():
        if nodo.izquierdo and id(nodo.izquierdo) in posiciones:
            xi, yi, _ = posiciones[id(nodo.izquierdo)]
            pygame.draw.line(pantalla, COLOR_LINEA, (x, y), (xi, yi), 2)
        if nodo.derecho and id(nodo.derecho) in posiciones:
            xd, yd, _ = posiciones[id(nodo.derecho)]
            pygame.draw.line(pantalla, COLOR_LINEA, (x, y), (xd, yd), 2)


def dibujar_nodos(posiciones: dict):
    """Dibuja los círculos con el valor de cada nodo."""
    for nid, (x, y, nodo) in posiciones.items():
        # Color según si está resaltado
        if nid == nodo_resaltado:
            color = COLOR_NODO_BUSQ if busqueda_exitosa else COLOR_NODO_NOBUSQ
            borde = (255, 255, 255)
            ancho_borde = 3
        else:
            color = COLOR_NODO
            borde = COLOR_NODO_BORDE
            ancho_borde = 2

        pygame.draw.circle(pantalla, borde, (x, y), RADIO_NODO + ancho_borde)
        pygame.draw.circle(pantalla, color, (x, y), RADIO_NODO)

        texto = fuente_nodo.render(str(nodo.dato), True, COLOR_TEXTO_NODO)
        rect = texto.get_rect(center=(x, y))
        pantalla.blit(texto, rect)


def dibujar_panel_lateral():
    """Panel derecho con controles e información."""
    px = ANCHO - 240
    pygame.draw.rect(pantalla, COLOR_PANEL, (px, 0, 240, ALTO))
    pygame.draw.line(pantalla, COLOR_INPUT_BORDE, (px, 0), (px, ALTO), 1)

    y = 20
    titulo = fuente_titulo.render("ABB Visualizer", True, COLOR_ACENTO)
    pantalla.blit(titulo, (px + 15, y))

    y += 45
    sep = fuente_info.render("─" * 28, True, COLOR_GRIS)
    pantalla.blit(sep, (px + 10, y))

    y += 22
    instrucciones = [
        ("ENTER",  "Insertar"),
        ("DEL",    "Eliminar"),
        ("B",      "Buscar"),
        ("ESC",    "Limpiar"),
    ]
    for tecla, accion in instrucciones:
        t_tecla  = fuente_ui.render(f"[{tecla}]", True, COLOR_ACENTO)
        t_accion = fuente_ui.render(accion, True, COLOR_TEXTO_UI)
        pantalla.blit(t_tecla,  (px + 15, y))
        pantalla.blit(t_accion, (px + 80, y))
        y += 26

    y += 10
    pantalla.blit(sep, (px + 10, y))

    # Campo de entrada
    y += 22
    label = fuente_ui.render("Valor:", True, COLOR_TEXTO_UI)
    pantalla.blit(label, (px + 15, y))
    y += 24
    pygame.draw.rect(pantalla, COLOR_INPUT_BG,    (px + 15, y, 200, 34), border_radius=6)
    pygame.draw.rect(pantalla, COLOR_INPUT_BORDE, (px + 15, y, 200, 34), 2, border_radius=6)
    cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
    t_input = fuente_ui.render(texto_entrada + cursor, True, COLOR_ACENTO)
    pantalla.blit(t_input, (px + 25, y + 8))

    # Mensaje de estado
    y += 55
    pantalla.blit(sep, (px + 10, y))
    y += 22
    for linea in _wrap(mensaje, 27):
        t_msg = fuente_info.render(linea, True, color_mensaje)
        pantalla.blit(t_msg, (px + 15, y))
        y += 18

    # Recorridos
    y = ALTO - 200
    pantalla.blit(sep, (px + 10, y))
    y += 14
    recorridos = [
        ("In-orden",   arbol.inorden()),
        ("Pre-orden",  arbol.preorden()),
        ("Post-orden", arbol.postorden()),
    ]
    for nombre, lista in recorridos:
        t_n = fuente_info.render(nombre + ":", True, COLOR_GRIS)
        pantalla.blit(t_n, (px + 15, y))
        y += 16
        valores = ", ".join(str(v) for v in lista)
        for parte in _wrap(valores, 27):
            t_v = fuente_info.render(parte, True, COLOR_TEXTO_UI)
            pantalla.blit(t_v, (px + 15, y))
            y += 15
        y += 4

    # Altura del árbol
    altura_txt = fuente_info.render(f"Altura: {arbol.altura()}", True, COLOR_GRIS)
    pantalla.blit(altura_txt, (px + 15, ALTO - 30))


def _wrap(texto: str, max_chars: int) -> list:
    """Divide un string largo en líneas de max_chars."""
    palabras = texto.split()
    lineas, actual = [], ""
    for p in palabras:
        if len(actual) + len(p) + 1 <= max_chars:
            actual += (" " if actual else "") + p
        else:
            if actual:
                lineas.append(actual)
            actual = p
    if actual:
        lineas.append(actual)
    return lineas if lineas else [""]


# ─────────────────────────────────────────────
#  LOOP PRINCIPAL
# ─────────────────────────────────────────────
def main():
    global texto_entrada, mensaje, color_mensaje, nodo_resaltado, busqueda_exitosa

    corriendo = True
    while corriendo:
        reloj.tick(FPS)

        # ── Eventos ──────────────────────────────
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            elif evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    texto_entrada = ""
                    nodo_resaltado = None
                    busqueda_exitosa = None
                    mensaje = "Entrada limpiada."
                    color_mensaje = COLOR_GRIS

                elif evento.key == pygame.K_BACKSPACE:
                    texto_entrada = texto_entrada[:-1]

                elif evento.key == pygame.K_RETURN:
                    # INSERTAR
                    if texto_entrada.lstrip("-").isdigit():
                        val = int(texto_entrada)
                        arbol.insertar(val)
                        mensaje = f"✔ Nodo {val} insertado."
                        color_mensaje = COLOR_NODO_BUSQ
                        nodo_resaltado = None
                        busqueda_exitosa = None
                    else:
                        mensaje = "⚠ Ingresa un número entero."
                        color_mensaje = COLOR_NODO_NOBUSQ
                    texto_entrada = ""

                elif evento.key == pygame.K_DELETE:
                    # ELIMINAR
                    if texto_entrada.lstrip("-").isdigit():
                        val = int(texto_entrada)
                        if arbol.buscar(val):
                            arbol.eliminar(val)
                            mensaje = f"✔ Nodo {val} eliminado."
                            color_mensaje = COLOR_ACENTO
                        else:
                            mensaje = f"✘ {val} no existe en el árbol."
                            color_mensaje = COLOR_NODO_NOBUSQ
                        nodo_resaltado = None
                        busqueda_exitosa = None
                    else:
                        mensaje = "⚠ Ingresa un número entero."
                        color_mensaje = COLOR_NODO_NOBUSQ
                    texto_entrada = ""

                elif evento.key == pygame.K_b:
                    # BUSCAR
                    if texto_entrada.lstrip("-").isdigit():
                        val = int(texto_entrada)
                        encontrado = arbol.buscar(val)
                        busqueda_exitosa = encontrado
                        # Hallar el id del nodo para resaltarlo
                        posiciones = arbol.obtener_posiciones(ANCHO - 240, ALTO)
                        nodo_resaltado = None
                        for nid, (x, y, n) in posiciones.items():
                            if n.dato == val:
                                nodo_resaltado = nid
                                break
                        if encontrado:
                            mensaje = f"✔ {val} encontrado en el árbol."
                            color_mensaje = COLOR_NODO_BUSQ
                        else:
                            mensaje = f"✘ {val} NO está en el árbol."
                            color_mensaje = COLOR_NODO_NOBUSQ
                    else:
                        mensaje = "⚠ Ingresa un número entero."
                        color_mensaje = COLOR_NODO_NOBUSQ
                    texto_entrada = ""

                elif evento.unicode.isdigit() or \
                     (evento.unicode == "-" and texto_entrada == ""):
                    texto_entrada += evento.unicode

        # ── Dibujo ───────────────────────────────
        pantalla.fill(COLOR_FONDO)

        area_arbol = ANCHO - 240
        posiciones = arbol.obtener_posiciones(area_arbol, ALTO)
        dibujar_aristas(posiciones)
        dibujar_nodos(posiciones)
        dibujar_panel_lateral()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
