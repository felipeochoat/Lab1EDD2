"""
ui.py
Componentes de interfaz gráfica para CyberDetective.
Estilo pixel-art: colores planos, bordes duros, fuentes monoespaciadas.
"""

import pygame

# ──────────────────────────────────────────────────────────
#  PALETA DE COLORES
# ──────────────────────────────────────────────────────────
C = {
    "fondo":          (10,  14,  26),
    "panel":          (18,  24,  42),
    "panel_borde":    (40,  60, 100),
    "acento":         (80, 200, 255),
    "acento2":        (255, 200,  60),
    "verde":          (80, 220, 120),
    "rojo":           (220,  60,  80),
    "lila":           (160,  80, 255),
    "texto":          (210, 230, 255),
    "texto_dim":      (100, 130, 170),
    "blanco":         (255, 255, 255),
    "negro":          (0,   0,   0),
    "nodo_normal":    (40,  90, 160),
    "nodo_nuevo":     (80, 220, 120),
    "nodo_raiz":      (255, 200,  60),
    "linea":          (50,  80, 130),
    "boton_normal":   (30,  50,  90),
    "boton_hover":    (50,  90, 150),
    "boton_activo":   (80, 200, 255),
    "boton_correcto": (40, 160,  80),
    "boton_incorrecto":(160, 40,  60),
    "evidencia_bg":   (20,  35,  60),
    "evidencia_hover":(35,  60, 100),
    "evidencia_col":  (80, 220, 120),
}

RADIO_NODO = 28


def _fuente(nombre, size, bold=False):
    try:
        return pygame.font.SysFont(nombre, size, bold=bold)
    except Exception:
        return pygame.font.SysFont("consolas", size, bold=bold)


# Fuentes globales (se inicializan en init_fuentes)
F = {}


def init_fuentes():
    global F
    F = {
        "titulo":   _fuente("consolas", 28, bold=True),
        "subtitulo":_fuente("consolas", 20, bold=True),
        "normal":   _fuente("consolas", 16),
        "pequeña":  _fuente("consolas", 13),
        "nodo":     _fuente("consolas", 12, bold=True),
        "grande":   _fuente("consolas", 36, bold=True),
    }


# ──────────────────────────────────────────────────────────
#  UTILIDADES DE DIBUJO
# ──────────────────────────────────────────────────────────

def rect_pixel(surf, color, rect, borde_color=None, grosor_borde=2):
    """Rectángulo estilo pixel-art (sin border-radius)."""
    pygame.draw.rect(surf, color, rect)
    if borde_color:
        pygame.draw.rect(surf, borde_color, rect, grosor_borde)


def texto_centrado(surf, texto, fuente_key, color, cx, cy):
    t = F[fuente_key].render(texto, False, color)
    r = t.get_rect(center=(cx, cy))
    surf.blit(t, r)


def texto_izq(surf, texto, fuente_key, color, x, y):
    t = F[fuente_key].render(texto, False, color)
    surf.blit(t, (x, y))
    return t.get_height()


def wrap_texto(texto, fuente_key, max_ancho):
    """Divide texto en líneas que caben en max_ancho px."""
    palabras = texto.split(" ")
    lineas = []
    actual = ""
    fuente = F[fuente_key]
    for p in palabras:
        prueba = actual + (" " if actual else "") + p
        if fuente.size(prueba)[0] <= max_ancho:
            actual = prueba
        else:
            if actual:
                lineas.append(actual)
            actual = p
    if actual:
        lineas.append(actual)
    return lineas


def dibujar_texto_multilinea(surf, texto, fuente_key, color, x, y, max_ancho, interlinea=4):
    lineas = []
    for parrafo in texto.split("\n"):
        lineas.extend(wrap_texto(parrafo, fuente_key, max_ancho))
    h = F[fuente_key].get_height() + interlinea
    for i, l in enumerate(lineas):
        texto_izq(surf, l, fuente_key, color, x, y + i * h)
    return len(lineas) * h


# ──────────────────────────────────────────────────────────
#  COMPONENTE: BOTÓN
# ──────────────────────────────────────────────────────────

class Boton:
    def __init__(self, rect, texto, fuente_key="normal",
                 color=None, color_hover=None, color_texto=None):
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.fuente_key = fuente_key
        self.color = color or C["boton_normal"]
        self.color_hover = color_hover or C["boton_hover"]
        self.color_texto = color_texto or C["texto"]
        self.hover = False
        self.activo = False
        self.color_override = None  # para estados correcto/incorrecto

    def actualizar(self, pos_mouse):
        self.hover = self.rect.collidepoint(pos_mouse)

    def dibujar(self, surf):
        if self.color_override:
            col = self.color_override
        elif self.activo:
            col = C["boton_activo"]
        elif self.hover:
            col = self.color_hover
        else:
            col = self.color
        rect_pixel(surf, col, self.rect, C["panel_borde"])
        # Sombra pixel-art (2px abajo-derecha)
        sombra = pygame.Rect(self.rect.x + 2, self.rect.y + 2,
                             self.rect.w, self.rect.h)
        pygame.draw.rect(surf, (0, 0, 0, 80), sombra)
        rect_pixel(surf, col, self.rect, C["panel_borde"])
        texto_centrado(surf, self.texto, self.fuente_key,
                       self.color_texto, self.rect.centerx, self.rect.centery)

    def fue_clickeado(self, evento):
        return (evento.type == pygame.MOUSEBUTTONDOWN and
                evento.button == 1 and
                self.rect.collidepoint(evento.pos))


# ──────────────────────────────────────────────────────────
#  COMPONENTE: TARJETA DE EVIDENCIA
# ──────────────────────────────────────────────────────────

class TarjetaEvidencia:
    ANCHO = 180
    ALTO = 100

    def __init__(self, evidencia: dict, x, y, sprites: dict):
        self.ev = evidencia
        self.rect = pygame.Rect(x, y, self.ANCHO, self.ALTO)
        self.sprites = sprites
        self.recolectada = False
        self.hover = False

    def actualizar(self, pos_mouse):
        if not self.recolectada:
            self.hover = self.rect.collidepoint(pos_mouse)

    def dibujar(self, surf):
        alpha = 80 if self.recolectada else 255
        col_bg = C["evidencia_col"] if self.recolectada else (
            C["evidencia_hover"] if self.hover else C["evidencia_bg"]
        )
        col_borde = C["verde"] if self.recolectada else C["panel_borde"]

        s = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        s.fill((*col_bg, alpha))
        surf.blit(s, self.rect.topleft)
        pygame.draw.rect(surf, col_borde, self.rect, 2)

        # Sprite / ícono
        sprite_key = self.ev.get("sprite", "")
        icono = self.sprites.get(sprite_key)
        if icono:
            surf.blit(icono, (self.rect.x + 8, self.rect.y + 8))

        # Nombre
        col_txt = C["negro"] if self.recolectada else C["acento"]
        texto_izq(surf, self.ev["nombre"], "pequeña", col_txt,
                  self.rect.x + 8, self.rect.y + 52)

        if self.recolectada:
            texto_izq(surf, "✔ RECOLECTADA", "pequeña", C["negro"],
                      self.rect.x + 8, self.rect.y + 70)
        elif self.hover:
            texto_izq(surf, "Clic para recoger", "pequeña", C["acento2"],
                      self.rect.x + 8, self.rect.y + 70)

    def fue_clickeado(self, evento):
        return (not self.recolectada and
                evento.type == pygame.MOUSEBUTTONDOWN and
                evento.button == 1 and
                self.rect.collidepoint(evento.pos))


# ──────────────────────────────────────────────────────────
#  COMPONENTE: PANEL DE INFORMACIÓN DE NODO
# ──────────────────────────────────────────────────────────

class PanelNodo:
    """Panel lateral que muestra los datos del nodo seleccionado."""

    def __init__(self, x, y, ancho, alto):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.nodo = None

    def set_nodo(self, nodo):
        self.nodo = nodo

    def dibujar(self, surf):
        rect_pixel(surf, C["panel"], self.rect, C["panel_borde"])
        if self.nodo is None:
            texto_centrado(surf, "Selecciona un nodo", "pequeña",
                           C["texto_dim"], self.rect.centerx, self.rect.centery)
            return

        n = self.nodo
        x, y = self.rect.x + 12, self.rect.y + 12
        mw = self.rect.w - 24

        y += texto_izq(surf, f"CASO: {n.id_caso}", "pequeña", C["acento2"], x, y) + 4
        y += texto_izq(surf, f"Tipo: {n.tipo_acoso}", "pequeña", C["texto"], x, y) + 4
        y += texto_izq(surf, f"Gravedad: {n.gravedad}/10", "pequeña",
                       _color_gravedad(n.gravedad), x, y) + 4

        pygame.draw.line(surf, C["panel_borde"],
                         (x, y), (x + mw, y), 1)
        y += 6

        y += texto_izq(surf, "Ley:", "pequeña", C["texto_dim"], x, y) + 2
        y += dibujar_texto_multilinea(surf, n.ley, "pequeña", C["texto"], x, y, mw) + 4

        y += texto_izq(surf, "Pena:", "pequeña", C["texto_dim"], x, y) + 2
        y += dibujar_texto_multilinea(surf, n.pena, "pequeña", C["rojo"], x, y, mw) + 4

        pygame.draw.line(surf, C["panel_borde"],
                         (x, y), (x + mw, y), 1)
        y += 6

        y += texto_izq(surf, "Evidencias:", "pequeña", C["texto_dim"], x, y) + 2
        for ev in n.evidencias:
            y += dibujar_texto_multilinea(surf, f"• {ev}", "pequeña",
                                          C["verde"], x, y, mw) + 2


def _color_gravedad(g):
    if g <= 3:
        return C["verde"]
    if g <= 6:
        return C["acento2"]
    return C["rojo"]


# ──────────────────────────────────────────────────────────
#  PANTALLA: MENÚ PRINCIPAL
# ──────────────────────────────────────────────────────────

class PantallaMenu:
    def __init__(self, ancho, alto, sprites):
        self.ancho = ancho
        self.alto = alto
        self.sprites = sprites
        cx = ancho // 2
        self.btn_jugar  = Boton((cx - 140, 340, 280, 50), "▶  INICIAR INVESTIGACIÓN",
                                color=C["boton_normal"], color_hover=C["boton_hover"],
                                color_texto=C["acento"])
        self.btn_ayuda  = Boton((cx - 140, 410, 280, 50), "?  CÓMO JUGAR")
        self.btn_salir  = Boton((cx - 140, 480, 280, 50), "✕  SALIR",
                                color_texto=C["rojo"])
        self.tick = 0

    def actualizar(self, eventos, pos_mouse):
        self.tick += 1
        self.btn_jugar.actualizar(pos_mouse)
        self.btn_ayuda.actualizar(pos_mouse)
        self.btn_salir.actualizar(pos_mouse)
        for ev in eventos:
            if self.btn_jugar.fue_clickeado(ev):
                return "jugar"
            if self.btn_ayuda.fue_clickeado(ev):
                return "ayuda"
            if self.btn_salir.fue_clickeado(ev):
                return "salir"
        return None

    def dibujar(self, surf):
        surf.fill(C["fondo"])
        # Líneas de cuadrícula pixel-art
        for i in range(0, self.ancho, 40):
            pygame.draw.line(surf, (18, 26, 46), (i, 0), (i, self.alto), 1)
        for i in range(0, self.alto, 40):
            pygame.draw.line(surf, (18, 26, 46), (0, i), (self.ancho, i), 1)

        # Título
        titulo_surf = self.sprites.get("logo")
        if titulo_surf:
            r = titulo_surf.get_rect(centerx=self.ancho // 2, y=80)
            surf.blit(titulo_surf, r)
        else:
            texto_centrado(surf, "CYBER DETECTIVE", "grande", C["acento"],
                           self.ancho // 2, 120)
            texto_centrado(surf, "El Árbol de la Verdad", "subtitulo", C["acento2"],
                           self.ancho // 2, 170)

        texto_centrado(surf, "Una investigación sobre ciberacoso y sus consecuencias legales",
                       "pequeña", C["texto_dim"], self.ancho // 2, 220)

        # Parpadeo decorativo
        if (self.tick // 30) % 2 == 0:
            texto_centrado(surf, "► DETECTIVE ALEX – CASO ABIERTO ◄",
                           "pequeña", C["acento2"], self.ancho // 2, 290)

        self.btn_jugar.dibujar(surf)
        self.btn_ayuda.dibujar(surf)
        self.btn_salir.dibujar(surf)


# ──────────────────────────────────────────────────────────
#  PANTALLA: AYUDA
# ──────────────────────────────────────────────────────────

class PantallaAyuda:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.btn_volver = Boton((ancho // 2 - 100, alto - 80, 200, 44),
                                "◄ VOLVER", color_texto=C["acento"])

    def actualizar(self, eventos, pos_mouse):
        self.btn_volver.actualizar(pos_mouse)
        for ev in eventos:
            if self.btn_volver.fue_clickeado(ev):
                return "menu"
        return None

    def dibujar(self, surf):
        surf.fill(C["fondo"])
        texto_centrado(surf, "CÓMO JUGAR", "titulo", C["acento"], self.ancho // 2, 50)

        lineas = [
            ("1. RECOLECTA EVIDENCIAS", C["acento2"]),
            ("   Haz clic en los objetos que aparecen en la escena.", C["texto"]),
            ("", C["texto"]),
            ("2. CLASIFICA EL DELITO", C["acento2"]),
            ("   Elige la opción correcta según las evidencias.", C["texto"]),
            ("", C["texto"]),
            ("3. EL ÁRBOL CRECE", C["acento2"]),
            ("   Cada caso correcto agrega un nodo al árbol AVL.", C["texto"]),
            ("   Si el árbol se desbalancea, verás una rotación.", C["texto"]),
            ("", C["texto"]),
            ("4. NIVEL FINAL", C["acento2"]),
            ("   Recorre el árbol y genera el reporte del caso.", C["texto"]),
            ("", C["texto"]),
            ("ÁRBOL AVL", C["lila"]),
            ("   Los nodos se ordenan por GRAVEDAD del delito.", C["texto"]),
            ("   El árbol se auto-balancea con rotaciones.", C["texto"]),
        ]

        y = 110
        for texto, color in lineas:
            if texto:
                texto_izq(surf, texto, "normal" if texto.startswith(" ") else "normal",
                          color, 80, y)
            y += 28

        self.btn_volver.dibujar(surf)


# ──────────────────────────────────────────────────────────
#  PANTALLA: NARRATIVA DE NIVEL
# ──────────────────────────────────────────────────────────

class PantallaNarrativa:
    def __init__(self, ancho, alto, nivel_data, sprites):
        self.ancho = ancho
        self.alto = alto
        self.datos = nivel_data
        self.sprites = sprites
        self.tick = 0
        self.btn_continuar = Boton(
            (ancho // 2 - 140, alto - 100, 280, 50),
            "► INICIAR INVESTIGACIÓN",
            color=C["boton_normal"], color_hover=C["boton_hover"],
            color_texto=C["acento"]
        )

    def actualizar(self, eventos, pos_mouse):
        self.tick += 1
        self.btn_continuar.actualizar(pos_mouse)
        for ev in eventos:
            if self.btn_continuar.fue_clickeado(ev):
                return "evidencias"
        return None

    def dibujar(self, surf):
        surf.fill(C["fondo"])
        d = self.datos
        acento = d.get("color_acento", C["acento"])

        # Fondo / sprite de escena
        bg = self.sprites.get(d.get("bg_sprite", ""))
        if bg:
            surf.blit(bg, (0, 0))

        # Panel semitransparente
        panel = pygame.Surface((self.ancho - 100, 300), pygame.SRCALPHA)
        panel.fill((10, 14, 26, 210))
        surf.blit(panel, (50, 140))
        pygame.draw.rect(surf, acento, (50, 140, self.ancho - 100, 300), 2)

        texto_centrado(surf, d["titulo"], "subtitulo", acento,
                       self.ancho // 2, 100)

        dibujar_texto_multilinea(surf, d["historia"], "normal", C["texto"],
                                 80, 170, self.ancho - 160)

        dibujar_texto_multilinea(surf, f"OBJETIVO: {d['objetivo']}",
                                 "pequeña", acento, 80, 340, self.ancho - 160)

        self.btn_continuar.dibujar(surf)


# ──────────────────────────────────────────────────────────
#  PANTALLA: RECOLECCIÓN DE EVIDENCIAS
# ──────────────────────────────────────────────────────────

class PantallaEvidencias:
    def __init__(self, ancho, alto, nivel_data, sprites):
        self.ancho = ancho
        self.alto = alto
        self.datos = nivel_data
        self.sprites = sprites
        self.tarjetas = []
        self.recolectadas = set()
        self.mensaje = ""
        self.tick_msg = 0

        # Crear tarjetas
        for ev in nivel_data["evidencias_disponibles"]:
            px, py = ev["posicion"]
            t = TarjetaEvidencia(ev, px, py, sprites)
            self.tarjetas.append(t)

        self.btn_continuar = Boton(
            (ancho - 220, alto - 70, 200, 44),
            "► ANALIZAR",
            color_texto=C["acento"]
        )
        self.btn_continuar.activo = False

    def _todas_requeridas(self):
        req = self.datos["evidencias_requeridas"]
        return req.issubset(self.recolectadas)

    def actualizar(self, eventos, pos_mouse):
        self.tick_msg += 1
        for t in self.tarjetas:
            t.actualizar(pos_mouse)
        self.btn_continuar.activo = self._todas_requeridas()
        self.btn_continuar.actualizar(pos_mouse)

        for ev in eventos:
            for t in self.tarjetas:
                if t.fue_clickeado(ev):
                    t.recolectada = True
                    self.recolectadas.add(t.ev["id"])
                    self.mensaje = f"✔ {t.ev['nombre']} recolectada"
                    self.tick_msg = 0
            if self.btn_continuar.fue_clickeado(ev):
                if self._todas_requeridas():
                    return "pregunta"
                else:
                    self.mensaje = "⚠ Faltan evidencias clave"
                    self.tick_msg = 0
        return None

    def dibujar(self, surf):
        surf.fill(C["fondo"])
        d = self.datos
        acento = d.get("color_acento", C["acento"])

        bg = self.sprites.get(d.get("bg_sprite", ""))
        if bg:
            surf.blit(bg, (0, 0))
            oscuro = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
            oscuro.fill((10, 14, 26, 140))
            surf.blit(oscuro, (0, 0))

        texto_centrado(surf, "RECOLECTA LAS EVIDENCIAS", "subtitulo", acento,
                       self.ancho // 2, 30)

        recolectadas_n = len(self.recolectadas & self.datos["evidencias_requeridas"])
        total = len(self.datos["evidencias_requeridas"])
        texto_centrado(surf, f"Evidencias clave: {recolectadas_n}/{total}",
                       "normal", C["texto_dim"], self.ancho // 2, 65)

        for t in self.tarjetas:
            t.dibujar(surf)

        # Mensaje flotante
        if self.tick_msg < 120:
            alpha = min(255, (120 - self.tick_msg) * 4)
            col = (*C["verde"], alpha)
            msg_s = F["normal"].render(self.mensaje, False, C["verde"])
            surf.blit(msg_s, (20, self.alto - 110))

        self.btn_continuar.dibujar(surf)


# ──────────────────────────────────────────────────────────
#  PANTALLA: PREGUNTA DE CLASIFICACIÓN
# ──────────────────────────────────────────────────────────

class PantallaPregunta:
    def __init__(self, ancho, alto, nivel_data):
        self.ancho = ancho
        self.alto = alto
        self.datos = nivel_data
        self.pregunta = nivel_data["pregunta"]
        self.seleccion = None
        self.resultado = None  # True/False
        self.tick_resultado = 0
        self.btn_continuar = None

        cx = ancho // 2
        self.botones_opciones = []
        opciones = self.pregunta["opciones"]
        for i, op in enumerate(opciones):
            y = 260 + i * 70
            b = Boton((cx - 280, y, 560, 54), op, fuente_key="normal")
            self.botones_opciones.append(b)

    def actualizar(self, eventos, pos_mouse):
        self.tick_resultado += 1
        for i, b in enumerate(self.botones_opciones):
            b.actualizar(pos_mouse)

        if self.btn_continuar:
            self.btn_continuar.actualizar(pos_mouse)

        for ev in eventos:
            if self.resultado is None:
                for i, b in enumerate(self.botones_opciones):
                    if b.fue_clickeado(ev):
                        self.seleccion = i
                        self.resultado = (i == self.pregunta["correcta"])
                        self.tick_resultado = 0
                        # Colorear botones
                        for j, bb in enumerate(self.botones_opciones):
                            if j == self.pregunta["correcta"]:
                                bb.color_override = C["boton_correcto"]
                            elif j == i and not self.resultado:
                                bb.color_override = C["boton_incorrecto"]
                        self.btn_continuar = Boton(
                            (self.ancho // 2 - 120, self.alto - 90, 240, 48),
                            "► INSERTAR EN EL ÁRBOL",
                            color_texto=C["acento"] if self.resultado else C["acento2"]
                        )
            else:
                if self.btn_continuar and self.btn_continuar.fue_clickeado(ev):
                    return "arbol"
        return None

    def dibujar(self, surf):
        surf.fill(C["fondo"])
        d = self.datos
        acento = d.get("color_acento", C["acento"])

        texto_centrado(surf, "CLASIFICA EL DELITO", "subtitulo", acento,
                       self.ancho // 2, 40)

        dibujar_texto_multilinea(surf, self.pregunta["texto"], "normal",
                                 C["texto"], 80, 100, self.ancho - 160)

        for b in self.botones_opciones:
            b.dibujar(surf)

        if self.resultado is not None and self.tick_resultado > 10:
            col = C["verde"] if self.resultado else C["rojo"]
            msg = "✔ ¡CORRECTO!" if self.resultado else "✘ INCORRECTO"
            texto_centrado(surf, msg, "subtitulo", col, self.ancho // 2, 570)
            dibujar_texto_multilinea(surf, self.pregunta["explicacion"],
                                     "pequeña", C["texto_dim"],
                                     80, 610, self.ancho - 160)

        if self.btn_continuar:
            self.btn_continuar.dibujar(surf)


# ──────────────────────────────────────────────────────────
#  PANTALLA: VISUALIZACIÓN DEL ÁRBOL
# ──────────────────────────────────────────────────────────

class PantallaArbol:
    PANEL_INFO_W = 280

    def __init__(self, ancho, alto, arbol, nuevo_nodo, sprites):
        self.ancho = ancho
        self.alto = alto
        self.arbol = arbol
        self.nuevo_nodo = nuevo_nodo
        self.sprites = sprites
        self.nodo_seleccionado = None
        self.panel_info = PanelNodo(
            ancho - self.PANEL_INFO_W - 10, 60,
            self.PANEL_INFO_W, alto - 130
        )
        self.btn_continuar = Boton(
            (ancho // 2 - 120, alto - 65, 240, 48),
            "► SIGUIENTE NIVEL",
            color_texto=C["acento"]
        )
        self.tick = 0
        self.animacion_nueva = 0  # frames desde inserción

    def actualizar(self, eventos, pos_mouse):
        self.tick += 1
        self.animacion_nueva += 1
        self.btn_continuar.actualizar(pos_mouse)

        area_arbol_w = self.ancho - self.PANEL_INFO_W - 30
        posiciones = self.arbol.obtener_posiciones(0, 60, area_arbol_w, self.alto - 130)

        for ev in eventos:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                for nid, (x, y, nodo) in posiciones.items():
                    if (ev.pos[0] - x) ** 2 + (ev.pos[1] - y) ** 2 <= RADIO_NODO ** 2:
                        self.nodo_seleccionado = nodo
                        self.panel_info.set_nodo(nodo)
                        break
            if self.btn_continuar.fue_clickeado(ev):
                return "siguiente"
        return None

    def dibujar(self, surf):
        surf.fill(C["fondo"])
        acento = C["acento"]

        texto_centrado(surf, "ÁRBOL DE INVESTIGACIÓN", "subtitulo", acento,
                       (self.ancho - self.PANEL_INFO_W) // 2, 30)

        area_arbol_w = self.ancho - self.PANEL_INFO_W - 30
        posiciones = self.arbol.obtener_posiciones(0, 60, area_arbol_w, self.alto - 130)

        # Aristas
        for nid, (x, y, nodo) in posiciones.items():
            if nodo.izquierdo and id(nodo.izquierdo) in posiciones:
                xi, yi, _ = posiciones[id(nodo.izquierdo)]
                pygame.draw.line(surf, C["linea"], (x, y), (xi, yi), 2)
            if nodo.derecho and id(nodo.derecho) in posiciones:
                xd, yd, _ = posiciones[id(nodo.derecho)]
                pygame.draw.line(surf, C["linea"], (x, y), (xd, yd), 2)

        # Nodos
        for nid, (x, y, nodo) in posiciones.items():
            es_nuevo = (nodo is self.nuevo_nodo and self.animacion_nueva < 60)
            es_raiz = (nodo is self.arbol.raiz)
            es_sel = (nodo is self.nodo_seleccionado)

            if es_nuevo:
                pulso = abs((self.animacion_nueva % 20) - 10) + RADIO_NODO
                pygame.draw.circle(surf, C["verde"], (x, y), pulso + 4)
                col = C["nodo_nuevo"]
            elif es_raiz:
                col = C["nodo_raiz"]
            elif es_sel:
                col = C["acento"]
            else:
                col = C["nodo_normal"]

            pygame.draw.circle(surf, C["panel_borde"], (x, y), RADIO_NODO + 2)
            pygame.draw.circle(surf, col, (x, y), RADIO_NODO)

            # Texto: gravedad
            t = F["nodo"].render(str(nodo.gravedad), False, C["blanco"])
            r = t.get_rect(center=(x, y - 5))
            surf.blit(t, r)
            t2 = F["pequeña"].render(nodo.id_caso[-3:], False, C["texto_dim"])
            r2 = t2.get_rect(center=(x, y + 9))
            surf.blit(t2, r2)

        # Etiqueta de rotación
        if self.arbol.rotaciones and self.animacion_nueva < 90:
            for rot_tipo, rot_val in self.arbol.rotaciones:
                msg = f"↻ ROTACIÓN {rot_tipo.upper()} (nodo {rot_val})"
                texto_centrado(surf, msg, "pequeña", C["acento2"],
                               area_arbol_w // 2, self.alto - 100)

        self.panel_info.dibujar(surf)
        self.btn_continuar.dibujar(surf)


# ──────────────────────────────────────────────────────────
#  PANTALLA: REPORTE FINAL
# ──────────────────────────────────────────────────────────

class PantallaReporte:
    def __init__(self, ancho, alto, arbol):
        self.ancho = ancho
        self.alto = alto
        self.arbol = arbol
        self.scroll = 0
        self.btn_menu = Boton((ancho // 2 - 120, alto - 65, 240, 48),
                              "◄ MENÚ PRINCIPAL", color_texto=C["acento"])
        self.nodos = arbol.inorden()

    def actualizar(self, eventos, pos_mouse):
        self.btn_menu.actualizar(pos_mouse)
        for ev in eventos:
            if ev.type == pygame.MOUSEWHEEL:
                self.scroll = max(0, self.scroll - ev.y * 20)
            if self.btn_menu.fue_clickeado(ev):
                return "menu"
        return None

    def dibujar(self, surf):
        surf.fill(C["fondo"])
        texto_centrado(surf, "REPORTE FINAL DEL CASO", "titulo", C["acento2"],
                       self.ancho // 2, 35)
        texto_centrado(surf, "Recorrido inorden del árbol (gravedad ascendente)",
                       "pequeña", C["texto_dim"], self.ancho // 2, 70)

        clip = pygame.Rect(40, 95, self.ancho - 80, self.alto - 160)
        surf.set_clip(clip)

        y = 100 - self.scroll
        for i, nodo in enumerate(self.nodos):
            if y + 140 < 95 or y > self.alto:
                y += 150
                continue
            col_borde = _color_gravedad(nodo.gravedad)
            panel_r = pygame.Rect(40, y, self.ancho - 80, 135)
            rect_pixel(surf, C["panel"], panel_r, col_borde)

            texto_izq(surf, f"#{i+1}  {nodo.id_caso} – {nodo.tipo_acoso}",
                      "normal", col_borde, 60, y + 10)
            texto_izq(surf, f"Gravedad: {nodo.gravedad}/10  |  Ley: {nodo.ley}",
                      "pequeña", C["texto"], 60, y + 38)
            texto_izq(surf, f"Pena: {nodo.pena}", "pequeña", C["rojo"], 60, y + 58)
            evs = " | ".join(nodo.evidencias[:3])
            dibujar_texto_multilinea(surf, f"Evidencias: {evs}",
                                     "pequeña", C["texto_dim"], 60, y + 78, self.ancho - 120)
            y += 150

        surf.set_clip(None)
        self.btn_menu.dibujar(surf)
