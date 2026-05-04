import pygame

# ──────────────────────────────────────────────────────────
#  AJUSTES GLOBALES (volumen, tamaño, contraste)
# ──────────────────────────────────────────────────────────
AJUSTES = {
    "volumen":   0.5,       # 0.0 – 1.0
    "tamaño":    "NORMAL",  # "GRANDE" | "NORMAL" | "PEQUEÑO"
    "contraste": False,     # True = alto contraste
}

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

# Paleta alternativa de alto contraste
C_CONTRASTE = {
    "fondo":           (0,   0,   0),
    "panel":           (20,  20,  20),
    "panel_borde":     (255, 255, 0),
    "acento":          (0,   255, 255),
    "acento2":         (255, 255, 0),
    "verde":           (0,   255, 0),
    "rojo":            (255, 60,  60),
    "lila":            (220, 100, 255),
    "texto":           (255, 255, 255),
    "texto_dim":       (200, 200, 200),
    "blanco":          (255, 255, 255),
    "negro":           (0,   0,   0),
    "nodo_normal":     (0,   80,  200),
    "nodo_nuevo":      (0,   255, 0),
    "nodo_raiz":       (255, 255, 0),
    "linea":           (180, 180, 180),
    "boton_normal":    (40,  40,  80),
    "boton_hover":     (80,  80,  160),
    "boton_activo":    (0,   255, 255),
    "boton_correcto":  (0,   180, 0),
    "boton_incorrecto":(200, 0,   0),
    "evidencia_bg":    (10,  10,  30),
    "evidencia_hover": (30,  30,  80),
    "evidencia_col":   (0,   255, 0),
}

def get_C():
    #Devuelve la paleta activa según el ajuste de contraste.
    return C_CONTRASTE if AJUSTES["contraste"] else C


def _fuente(nombre, size, bold=False):
    try:
        return pygame.font.SysFont(nombre, size, bold=bold)
    except Exception:
        return pygame.font.SysFont("consolas", size, bold=bold)


# Fuentes globales (se inicializan en init_fuentes)
F = {}


def init_fuentes():
    global F
    tam = AJUSTES["tamaño"]
    if tam == "GRANDE":
        escala = 1.35
    elif tam == "PEQUEÑO":
        escala = 0.80
    else:
        escala = 1.0

    def s(base):
        return max(8, int(base * escala))

    F = {
        "titulo":    _fuente("consolas", s(28), bold=True),
        "subtitulo": _fuente("consolas", s(20), bold=True),
        "normal":    _fuente("consolas", s(16)),
        "pequeña":   _fuente("consolas", s(13)),
        "nodo":      _fuente("consolas", s(12), bold=True),
        "grande":    _fuente("consolas", s(36), bold=True),
    }


# ──────────────────────────────────────────────────────────
#  UTILIDADES DE DIBUJO
# ──────────────────────────────────────────────────────────

def rect_pixel(surf, color, rect, borde_color=None, grosor_borde=2):
    pygame.draw.rect(surf, color, rect)
    if borde_color:
        pygame.draw.rect(surf, borde_color, rect, grosor_borde)


def cc(key):
    return get_C()[key]


def texto_centrado(surf, texto, fuente_key, color, cx, cy):
    t = F[fuente_key].render(texto, False, color)
    r = t.get_rect(center=(cx, cy))
    surf.blit(t, r)


def texto_izq(surf, texto, fuente_key, color, x, y):
    t = F[fuente_key].render(texto, False, color)
    surf.blit(t, (x, y))
    return t.get_height()


def wrap_texto(texto, fuente_key, max_ancho):
    #Divide texto en líneas que caben en max_ancho px.
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
    ANCHO = 200
    ALTO  = 120
    # Dimensiones del panel de mockup visual
    IMG_W = 330
    IMG_H = 420

    def __init__(self, evidencia: dict, x, y, sprites: dict, nivel_data: dict = None):
        self.ev          = evidencia
        self.rect        = pygame.Rect(x, y, self.ANCHO, self.ALTO)
        self.sprites     = sprites
        self.nivel_data  = nivel_data or {}
        self.recolectada = False
        self.hover       = False
        self._tick       = 0
        self._click_anim = 0   # frames de animación de click (cuenta regresiva)
        self._mockup     = None   # se genera lazy al primer hover

    def _get_mockup(self):
        """Genera la imagen de mockup la primera vez que se necesita.
        La clave incluye el nombre de la víctima para evitar mostrar
        datos de un nivel anterior si el objeto se reutiliza."""
        if self._mockup is not None:
            return self._mockup
        try:
            from evidencias_img import generar_imagen_evidencia
            sprite_key    = self.ev.get("sprite", "")
            self._mockup  = generar_imagen_evidencia(sprite_key, self.nivel_data)
        except Exception as e:
            # Fallback: panel de texto simple
            s = pygame.Surface((self.IMG_W, self.IMG_H), pygame.SRCALPHA)
            pygame.draw.rect(s, (12, 16, 26), (0, 0, self.IMG_W, self.IMG_H),
                             border_radius=10)
            self._mockup = s
        return self._mockup

    def actualizar(self, pos_mouse):
        if not self.recolectada:
            self.hover = self.rect.collidepoint(pos_mouse)
        else:
            self.hover = False
        if self.hover:
            self._tick += 1
            self._get_mockup()   # pre-calentar
        else:
            self._tick = 0

    # ------------------------------------------------------------------
    def dibujar(self, surf):
        # Animación de click: flash blanco/verde al recolectar
        if self._click_anim > 0:
            self._click_anim -= 1

        alpha  = 80 if self.recolectada else 255

        if self.recolectada:
            col_bg    = (30, 80, 45)
            col_borde = C["verde"]
        elif self._click_anim > 0:
            t = self._click_anim / 18
            col_bg    = (int(30 * (1-t) + 80 * t), int(100 * (1-t) + 220 * t), int(80 * (1-t) + 120 * t))
            col_borde = C["verde"]
        elif self.hover:
            col_bg    = C["evidencia_hover"]
            col_borde = C["acento"]
        else:
            col_bg    = C["evidencia_bg"]
            col_borde = C["panel_borde"]

        # Sombra exterior para dar profundidad
        if not self.recolectada:
            sombra = pygame.Surface((self.rect.w + 8, self.rect.h + 8), pygame.SRCALPHA)
            sombra.fill((0, 0, 0, 60))
            surf.blit(sombra, (self.rect.x + 4, self.rect.y + 4))

        # Pulso de glow en hover (más vistoso)
        if self.hover and not self.recolectada:
            pulso = abs((self._tick % 24) - 12) / 12.0
            glow_size = int(4 + 4 * pulso)
            glow_r = pygame.Rect(self.rect.x - glow_size, self.rect.y - glow_size,
                                 self.rect.w + glow_size * 2, self.rect.h + glow_size * 2)
            glow_col = (
                int(30  + 60  * pulso),
                int(100 + 120 * pulso),
                int(200 + 55  * pulso),
            )
            pygame.draw.rect(surf, glow_col, glow_r, 3, border_radius=10)

        # Fondo de la tarjeta
        s = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        s.fill((*col_bg, alpha))
        surf.blit(s, self.rect.topleft)

        # Borde
        pygame.draw.rect(surf, col_borde, self.rect, 2, border_radius=6)

        # Línea decorativa superior de acento (solo si no recolectada)
        if not self.recolectada:
            accent_col = col_borde
            pygame.draw.rect(surf, accent_col,
                             (self.rect.x, self.rect.y, self.rect.w, 3), border_radius=6)

        # Ícono de sprite (si existe) o emoji de tipo de evidencia
        sprite_key = self.ev.get("sprite", "")
        icono      = self.sprites.get(sprite_key)
        icon_y = self.rect.y + 10
        if icono:
            surf.blit(icono, (self.rect.x + 8, icon_y))
        else:
            # Emoji de fallback según tipo
            _iconos = {
                "captura": "📱", "chat": "💬", "perfil": "👤",
                "post": "📢", "perfil_falso": "🎭", "metadata": "🌐",
                "logs": "📋", "testimonio": "🗣", "analisis": "🔍",
                "historial": "📄", "ip": "🌐", "denuncia": "⚖",
            }
            ico_txt = _iconos.get(sprite_key, "📁")
            try:
                f_ico = pygame.font.SysFont("segoeuiemoji,applesymbols,noto color emoji,symbola", 22)
                s_ico = f_ico.render(ico_txt, True, (200, 220, 255))
                surf.blit(s_ico, (self.rect.x + 8, icon_y))
            except Exception:
                pass

        # Nombre de la evidencia (bold / highlight en hover)
        nombre_col = C["negro"] if self.recolectada else (C["acento"] if self.hover else C["texto"])
        texto_izq(surf, self.ev["nombre"], "pequeña", nombre_col,
                  self.rect.x + 8, self.rect.y + 70)

        # Estado / instrucción
        if self.recolectada:
            texto_izq(surf, "✔ RECOLECTADA", "pequeña", C["verde"],
                      self.rect.x + 8, self.rect.y + 90)
        elif self.hover:
            # Texto pulsante "clic para recoger"
            pulso2 = abs((self._tick % 30) - 15) / 15.0
            bright = int(200 + 55 * pulso2)
            texto_izq(surf, "► CLIC PARA RECOGER", "pequeña", (bright, bright, 60),
                      self.rect.x + 8, self.rect.y + 90)
        else:
            texto_izq(surf, self.ev.get("descripcion", "")[:26], "pequeña", C["texto_dim"],
                      self.rect.x + 8, self.rect.y + 90)

    # ------------------------------------------------------------------
    def dibujar_tooltip(self, surf, screen_w, screen_h):
        """Muestra el mockup visual real de la evidencia al hacer hover.
        Nunca se sale de la ventana: escala la imagen si es necesario.
        """
        if not self.hover or self.recolectada:
            return

        mockup = self._get_mockup()
        if mockup is None:
            return

        MARGEN   = 6    # px de margen respecto a los bordes
        FLECHA_H = 10   # altura de la flecha indicadora
        LBL_H    = 18   # espacio reservado para la etiqueta de nombre

        iw_orig, ih_orig = mockup.get_size()

        # Espacio disponible arriba y abajo de la tarjeta
        espacio_arriba = self.rect.y - MARGEN - FLECHA_H - LBL_H
        espacio_abajo  = screen_h - self.rect.bottom - MARGEN - FLECHA_H - LBL_H

        # Elegir lado con más espacio
        usar_arriba = espacio_arriba >= espacio_abajo

        espacio_h = espacio_arriba if usar_arriba else espacio_abajo
        espacio_w = screen_w - 2 * MARGEN

        # Calcular escala para que quepa sin salirse
        escala = min(1.0,
                     espacio_w / iw_orig,
                     espacio_h / ih_orig)
        escala = max(escala, 0.35)   # no encoger demasiado

        iw = int(iw_orig * escala)
        ih = int(ih_orig * escala)

        # Escalar si es necesario
        if escala < 0.999:
            imagen = pygame.transform.smoothscale(mockup, (iw, ih))
        else:
            imagen = mockup

        # Posición X: centrado sobre la tarjeta, ajustado a bordes
        tip_x = self.rect.centerx - iw // 2
        tip_x = max(MARGEN, min(tip_x, screen_w - iw - MARGEN))

        # Posición Y: arriba o abajo según el lado elegido
        if usar_arriba:
            tip_y = self.rect.y - ih - FLECHA_H
            tip_y = max(MARGEN, tip_y)
        else:
            tip_y = self.rect.bottom + FLECHA_H
            # Asegurar que no se salga por abajo
            tip_y = min(tip_y, screen_h - ih - MARGEN)

        # Sombra exterior
        sombra = pygame.Surface((iw + 8, ih + 8), pygame.SRCALPHA)
        sombra.fill((0, 0, 0, 140))
        surf.blit(sombra, (tip_x - 4, tip_y - 4))

        # Imagen del mockup
        surf.blit(imagen, (tip_x, tip_y))

        # Borde de acento
        pygame.draw.rect(surf, C["acento"], (tip_x, tip_y, iw, ih), 2,
                         border_radius=10)

        # Etiqueta de nombre encima o debajo según el lado
        label = self.ev.get("nombre", "")
        lbl_s = F["pequeña"].render(label, True, C["acento2"])
        lx = tip_x + iw // 2 - lbl_s.get_width() // 2
        lx = max(MARGEN, min(lx, screen_w - lbl_s.get_width() - MARGEN))
        if usar_arriba:
            ly = tip_y - LBL_H
            if ly >= MARGEN:
                surf.blit(lbl_s, (lx, ly))
        else:
            ly = tip_y + ih + 4
            if ly + lbl_s.get_height() <= screen_h - MARGEN:
                surf.blit(lbl_s, (lx, ly))

        # Flecha indicadora
        arrow_x = max(tip_x + 10, min(self.rect.centerx, tip_x + iw - 10))
        if usar_arriba:   # tooltip arriba → flecha apunta abajo hacia tarjeta
            pts = [(arrow_x,     tip_y + ih + FLECHA_H),
                   (arrow_x - 7, tip_y + ih),
                   (arrow_x + 7, tip_y + ih)]
        else:             # tooltip abajo → flecha apunta arriba hacia tarjeta
            pts = [(arrow_x,     tip_y - FLECHA_H),
                   (arrow_x - 7, tip_y),
                   (arrow_x + 7, tip_y)]
        pygame.draw.polygon(surf, C["acento"], pts)

    # ------------------------------------------------------------------
    def fue_clickeado(self, evento):
        if (not self.recolectada and
                evento.type == pygame.MOUSEBUTTONDOWN and
                evento.button == 1 and
                self.rect.collidepoint(evento.pos)):
            self._click_anim = 18   # arrancar animación de flash
            return True
        return False



# ──────────────────────────────────────────────────────────
#  COMPONENTE: PANEL DE INFORMACIÓN DE NODO
# ──────────────────────────────────────────────────────────

class PanelNodo:
    #Panel lateral que muestra los datos del nodo seleccionado.

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
    _NUM_PART = 40

    def __init__(self, ancho, alto, sprites):
        self.ancho   = ancho
        self.alto    = alto
        self.sprites = sprites
        cx = ancho // 2
        self.btn_jugar   = Boton((cx - 140, 340, 280, 50), "▶  INICIAR INVESTIGACIÓN",
                                 color=C["boton_normal"], color_hover=C["boton_hover"],
                                 color_texto=C["acento"])
        self.btn_ayuda   = Boton((cx - 140, 410, 280, 50), "?  CÓMO JUGAR")
        self.btn_ajustes = Boton((cx - 140, 480, 280, 50), "⚙  AJUSTES",
                                 color_texto=C["acento2"])
        self.btn_salir   = Boton((cx - 140, 550, 280, 50), "✕  SALIR",
                                 color_texto=C["rojo"])
        self.tick = 0

        # Partículas de fondo
        import random as _r
        self._particulas = [
            {
                "x":     _r.uniform(0, ancho),
                "y":     _r.uniform(0, alto),
                "vy":    _r.uniform(-0.3, -0.9),
                "vx":    _r.uniform(-0.2, 0.2),
                "radio": _r.randint(1, 2),
                "col":   _r.choice([C["acento"], C["acento2"], C["lila"]]),
                "alpha": _r.randint(30, 100),
            }
            for _ in range(self._NUM_PART)
        ]

    def actualizar(self, eventos, pos_mouse):
        self.tick += 1

        import random as _r
        for p in self._particulas:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            if p["y"] < -4:
                p["y"] = self.alto + 4
                p["x"] = _r.uniform(0, self.ancho)

        self.btn_jugar.actualizar(pos_mouse)
        self.btn_ayuda.actualizar(pos_mouse)
        self.btn_ajustes.actualizar(pos_mouse)
        self.btn_salir.actualizar(pos_mouse)
        for ev in eventos:
            if self.btn_jugar.fue_clickeado(ev):
                return "jugar"
            if self.btn_ayuda.fue_clickeado(ev):
                return "ayuda"
            if self.btn_ajustes.fue_clickeado(ev):
                return "ajustes"
            if self.btn_salir.fue_clickeado(ev):
                return "salir"
        return None

    def dibujar(self, surf):
        P = get_C()
        surf.fill(P["fondo"])

        # Cuadrícula de fondo
        for i in range(0, self.ancho, 40):
            pygame.draw.line(surf, (18, 26, 46), (i, 0), (i, self.alto), 1)
        for i in range(0, self.alto, 40):
            pygame.draw.line(surf, (18, 26, 46), (0, i), (self.ancho, i), 1)

        # Partículas
        for p in self._particulas:
            ps = pygame.Surface((p["radio"] * 2, p["radio"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(ps, (*p["col"], p["alpha"]),
                               (p["radio"], p["radio"]), p["radio"])
            surf.blit(ps, (int(p["x"]) - p["radio"], int(p["y"]) - p["radio"]))

        # Scanlines
        scan = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        for sy in range(0, self.alto, 4):
            pygame.draw.line(scan, (0, 0, 0, 30), (0, sy), (self.ancho, sy))
        surf.blit(scan, (0, 0))

        titulo_surf = self.sprites.get("logo")
        if titulo_surf:
            r = titulo_surf.get_rect(centerx=self.ancho // 2, y=80)
            surf.blit(titulo_surf, r)
        else:
            # Glitch: cada ~3 s desplaza 2 px con color diferente
            glitch = (self.tick % 180) < 4
            if glitch:
                texto_centrado(surf, "CYBER DETECTIVE", "grande", P["rojo"],
                               self.ancho // 2 + 3, 121)
            texto_centrado(surf, "CYBER DETECTIVE", "grande", P["acento"],
                           self.ancho // 2, 120)
            texto_centrado(surf, "El Árbol de la Verdad", "subtitulo", P["acento2"],
                           self.ancho // 2, 170)

        texto_centrado(surf, "Una investigación sobre ciberacoso y sus consecuencias legales",
                       "pequeña", P["texto_dim"], self.ancho // 2, 220)

        # Indicador parpadeante
        if (self.tick // 30) % 2 == 0:
            texto_centrado(surf, "► DETECTIVE ALEX – CASO ABIERTO ◄",
                           "pequeña", P["acento2"], self.ancho // 2, 290)

        self.btn_jugar.dibujar(surf)
        self.btn_ayuda.dibujar(surf)
        self.btn_ajustes.dibujar(surf)
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
#  PANTALLA: AJUSTES
# ──────────────────────────────────────────────────────────

class PantallaAjustes:
    

    TAMAÑOS = ["GRANDE", "NORMAL", "PEQUEÑO"]

    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto  = alto
        cx = ancho // 2

        # Barra de volumen
        self.barra_x     = cx - 200
        self.barra_y     = 220
        self.barra_w     = 400
        self.barra_h     = 18
        self.arrastrando = False

        # Botones de tamaño
        self.btns_tamaño = []
        for i, lbl in enumerate(self.TAMAÑOS):
            bx = cx - 210 + i * 145
            self.btns_tamaño.append(Boton((bx, 360, 130, 44), lbl))

        # Botón de contraste (toggle)
        self.btn_contraste = Boton((cx - 140, 470, 280, 50),
                                   self._label_contraste(),
                                   color_texto=C["acento2"])

        self.btn_volver = Boton((cx - 100, alto - 80, 200, 44),
                                "◄ VOLVER", color_texto=C["acento"])

    def _label_contraste(self):
        return "◉ ALTO CONTRASTE: ON" if AJUSTES["contraste"] else "○ ALTO CONTRASTE: OFF"

    def _vol_a_px(self):
        return int(self.barra_x + AJUSTES["volumen"] * self.barra_w)

    def actualizar(self, eventos, pos_mouse):
        self.btn_volver.actualizar(pos_mouse)
        self.btn_contraste.actualizar(pos_mouse)
        for b in self.btns_tamaño:
            b.actualizar(pos_mouse)

        for ev in eventos:
            # ── Barra de volumen ──────────────────────────
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                bx, by = self.barra_x, self.barra_y - 10
                if bx <= ev.pos[0] <= bx + self.barra_w and by <= ev.pos[1] <= by + self.barra_h + 20:
                    self.arrastrando = True
                    self._set_vol(ev.pos[0])

            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self.arrastrando = False

            if ev.type == pygame.MOUSEMOTION and self.arrastrando:
                self._set_vol(pos_mouse[0])

            # ── Tamaño ────────────────────────────────────
            for i, b in enumerate(self.btns_tamaño):
                if b.fue_clickeado(ev):
                    AJUSTES["tamaño"] = self.TAMAÑOS[i]
                    init_fuentes()

            # ── Contraste ─────────────────────────────────
            if self.btn_contraste.fue_clickeado(ev):
                AJUSTES["contraste"] = not AJUSTES["contraste"]
                self.btn_contraste.texto = self._label_contraste()

            # ── Volver ────────────────────────────────────
            if self.btn_volver.fue_clickeado(ev):
                return "menu"

        return None

    def _set_vol(self, mx):
        ratio = (mx - self.barra_x) / self.barra_w
        AJUSTES["volumen"] = max(0.0, min(1.0, ratio))
        try:
            pygame.mixer.music.set_volume(AJUSTES["volumen"])
        except Exception:
            pass

    def dibujar(self, surf):
        P = get_C()
        surf.fill(P["fondo"])

        # Cuadrícula
        for i in range(0, self.ancho, 40):
            pygame.draw.line(surf, (18, 26, 46), (i, 0), (i, self.alto), 1)
        for i in range(0, self.alto, 40):
            pygame.draw.line(surf, (18, 26, 46), (0, i), (self.ancho, i), 1)

        cx = self.ancho // 2
        texto_centrado(surf, "⚙  AJUSTES", "titulo", P["acento"], cx, 55)

        # ── VOLUMEN ──────────────────────────────────────
        texto_centrado(surf, "VOLUMEN DE MÚSICA", "subtitulo", P["acento2"], cx, 160)

        # Pista de la barra
        track_rect = pygame.Rect(self.barra_x, self.barra_y, self.barra_w, self.barra_h)
        rect_pixel(surf, P["panel"], track_rect, P["panel_borde"])

        # Relleno de volumen
        fill_w = int(AJUSTES["volumen"] * self.barra_w)
        if fill_w > 0:
            fill_rect = pygame.Rect(self.barra_x, self.barra_y, fill_w, self.barra_h)
            pygame.draw.rect(surf, P["acento"], fill_rect)

        # Thumb (indicador)
        thumb_x = self._vol_a_px()
        pygame.draw.rect(surf, P["blanco"],
                         (thumb_x - 6, self.barra_y - 6, 12, self.barra_h + 12))
        pygame.draw.rect(surf, P["panel_borde"],
                         (thumb_x - 6, self.barra_y - 6, 12, self.barra_h + 12), 2)

        # Porcentaje
        pct = int(AJUSTES["volumen"] * 100)
        texto_centrado(surf, f"{pct}%", "normal", P["texto"], cx, self.barra_y + 42)

        # ── TAMAÑO DE TEXTO ───────────────────────────────
        texto_centrado(surf, "TAMAÑO DE TEXTO Y BOTONES", "subtitulo", P["acento2"], cx, 320)

        for i, b in enumerate(self.btns_tamaño):
            es_activo = (AJUSTES["tamaño"] == self.TAMAÑOS[i])
            b.color_override = P["boton_activo"] if es_activo else None
            b.dibujar(surf)

        # ── CONTRASTE ─────────────────────────────────────
        texto_centrado(surf, "ACCESIBILIDAD", "subtitulo", P["acento2"], cx, 438)
        self.btn_contraste.dibujar(surf)

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

        # Imagen de escena (columna derecha)
        escena = self.sprites.get(d.get("escena_sprite", ""))
        if escena:
            img_x = self.ancho // 2 + 20
            img_y = 130
            img_w = self.ancho // 2 - 70
            img_h = 320
            escena_scaled = pygame.transform.scale(escena, (img_w, img_h))
            surf.blit(escena_scaled, (img_x, img_y))
            pygame.draw.rect(surf, acento, (img_x, img_y, img_w, img_h), 2)

        # Panel de texto (columna izquierda si hay imagen, ancho completo si no)
        panel_x = 50
        panel_w = (self.ancho // 2 - 70) if escena else (self.ancho - 100)
        panel = pygame.Surface((panel_w, 300), pygame.SRCALPHA)
        panel.fill((10, 14, 26, 210))
        surf.blit(panel, (panel_x, 140))
        pygame.draw.rect(surf, acento, (panel_x, 140, panel_w, 300), 2)

        titulo_cx = (panel_x + panel_w // 2) if escena else (self.ancho // 2)
        texto_centrado(surf, d["titulo"], "subtitulo", acento, titulo_cx, 100)

        dibujar_texto_multilinea(surf, d["historia"], "normal", C["texto"],
                                 80, 170, panel_w - 30)

        dibujar_texto_multilinea(surf, f"OBJETIVO: {d.get('objetivo', '')}",
                         "pequeña", acento, 80, 340, panel_w - 30)

        self.btn_continuar.dibujar(surf)

# ──────────────────────────────────────────────────────────
#  PANTALLA: RECOLECCIÓN DE EVIDENCIAS
# ──────────────────────────────────────────────────────────

class PantallaEvidencias:
    """Pantalla de recolección de evidencias.

    Mejoras visuales:
    - Partículas flotantes de fondo (estilo hacker/matrix)
    - Efecto scanlines semitransparente
    - Parpadeo de título (glitch leve)
    - Tooltip con la descripción real de la evidencia al hover
    - Pulso animado en tarjetas al hacer hover
    """

    # ── Partículas ─────────────────────────────────────────
    _NUM_PARTICULAS = 30

    def __init__(self, ancho, alto, nivel_data, sprites):
        self.ancho   = ancho
        self.alto    = alto
        self.datos   = nivel_data
        self.sprites = sprites
        self.tarjetas      = []
        self.recolectadas  = set()
        self.mensaje       = ""
        self.tick_msg      = 0
        self.tick          = 0

        # Partículas flotantes
        import random as _r
        self._particulas = [
            {
                "x":     _r.uniform(0, ancho),
                "y":     _r.uniform(0, alto),
                "vy":    _r.uniform(-0.4, -1.2),
                "vx":    _r.uniform(-0.3, 0.3),
                "radio": _r.randint(1, 3),
                "alpha": _r.randint(40, 150),
            }
            for _ in range(self._NUM_PARTICULAS)
        ]

        # Crear tarjetas con posiciones del nivel
        for ev in nivel_data["evidencias_disponibles"]:
            px, py = ev["posicion"]
            t = TarjetaEvidencia(ev, px, py, sprites, nivel_data)
            self.tarjetas.append(t)

        self.btn_continuar = Boton(
            (ancho - 220, alto - 70, 200, 44),
            "► ANALIZAR",
            color_texto=C["acento"]
        )
        self.btn_continuar.activo = False

    # ── Lógica ─────────────────────────────────────────────
    def _todas_requeridas(self):
        req = self.datos["evidencias_requeridas"]
        return req.issubset(self.recolectadas)

    def actualizar(self, eventos, pos_mouse):
        self.tick     += 1
        self.tick_msg += 1

        # Mover partículas
        import random as _r
        for p in self._particulas:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            if p["y"] < -5:
                p["y"] = self.alto + 5
                p["x"] = _r.uniform(0, self.ancho)

        for t in self.tarjetas:
            t.actualizar(pos_mouse)

        self.btn_continuar.activo = self._todas_requeridas()
        self.btn_continuar.actualizar(pos_mouse)

        for ev in eventos:
            for t in self.tarjetas:
                if t.fue_clickeado(ev):
                    t.recolectada = True
                    self.recolectadas.add(t.ev["id"])
                    self.mensaje   = f"✔  {t.ev['nombre']} recolectada"
                    self.tick_msg  = 0
            if self.btn_continuar.fue_clickeado(ev):
                if self._todas_requeridas():
                    return "pregunta"
                else:
                    self.mensaje  = "⚠  Faltan evidencias clave"
                    self.tick_msg = 0
        return None

    # ── Dibujo ─────────────────────────────────────────────
    def dibujar(self, surf):
        surf.fill(C["fondo"])
        d      = self.datos
        acento = d.get("color_acento", C["acento"])

        # Fondo de la escena
        bg = self.sprites.get(d.get("bg_sprite", ""))
        if bg:
            surf.blit(bg, (0, 0))
            oscuro = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
            oscuro.fill((10, 14, 26, 155))
            surf.blit(oscuro, (0, 0))

        # ── Partículas flotantes ───────────────────────────
        for p in self._particulas:
            ps = pygame.Surface((p["radio"] * 2, p["radio"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(ps, (*acento, p["alpha"]), (p["radio"], p["radio"]), p["radio"])
            surf.blit(ps, (int(p["x"]) - p["radio"], int(p["y"]) - p["radio"]))

        # ── Scanlines ─────────────────────────────────────
        scan = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        for sy in range(0, self.alto, 4):
            pygame.draw.line(scan, (0, 0, 0, 40), (0, sy), (self.ancho, sy))
        surf.blit(scan, (0, 0))

        # ── Título con efecto glitch leve ─────────────────
        glitch = (self.tick % 90) < 3        # parpadeo 3 frames cada 90
        titulo_col = C["rojo"] if glitch else acento
        offset_x   = 2 if glitch else 0

        # Panel HUD superior semitransparente
        hud_s = pygame.Surface((self.ancho, 98), pygame.SRCALPHA)
        hud_s.fill((8, 12, 26, 210))
        surf.blit(hud_s, (0, 0))
        pygame.draw.line(surf, acento, (0, 98), (self.ancho, 98), 2)
        # Bordes laterales de acento
        pygame.draw.rect(surf, acento, (0, 0, 4, 98))
        pygame.draw.rect(surf, acento, (self.ancho - 4, 0, 4, 98))

        # Sombra del título
        sombra_s = F["subtitulo"].render("RECOLECTA LAS EVIDENCIAS", True, (0, 0, 0))
        surf.blit(sombra_s, (self.ancho // 2 - sombra_s.get_width() // 2 + 2 + offset_x, 14))
        texto_centrado(surf, "RECOLECTA LAS EVIDENCIAS", "subtitulo", titulo_col,
                       self.ancho // 2 + offset_x, 12)

        # Contador
        recolectadas_n = len(self.recolectadas & self.datos["evidencias_requeridas"])
        total          = len(self.datos["evidencias_requeridas"])
        progreso_col   = C["verde"] if recolectadas_n == total else C["acento2"]
        texto_centrado(surf, f"▣ EVIDENCIAS  {recolectadas_n} / {total}",
                       "normal", progreso_col, self.ancho // 2, 52)

        # Barra de progreso mejorada con glow
        barra_w  = 400
        barra_x  = self.ancho // 2 - barra_w // 2
        barra_y  = 74
        barra_h  = 10
        pygame.draw.rect(surf, (20, 30, 50), (barra_x, barra_y, barra_w, barra_h), border_radius=5)
        if total > 0:
            fill = int(barra_w * recolectadas_n / total)
            if fill > 0:
                glow_bar = pygame.Surface((fill + 6, barra_h + 6), pygame.SRCALPHA)
                glow_bar.fill((*progreso_col, 70))
                surf.blit(glow_bar, (barra_x - 3, barra_y - 3))
                pygame.draw.rect(surf, progreso_col, (barra_x, barra_y, fill, barra_h), border_radius=5)
        pygame.draw.rect(surf, C["panel_borde"], (barra_x, barra_y, barra_w, barra_h), 1, border_radius=5)

        # ── Tarjetas (sin tooltip) ─────────────────────────
        for t in self.tarjetas:
            t.dibujar(surf)

        # ── Tooltips (encima de todo) ──────────────────────
        for t in self.tarjetas:
            t.dibujar_tooltip(surf, self.ancho, self.alto)

        # ── Mensaje flotante con fondo ─────────────────────
        if self.tick_msg < 140:
            alpha = min(255, (140 - self.tick_msg) * 4)
            es_error = "⚠" in self.mensaje
            msg_col  = C["rojo"] if es_error else C["verde"]
            msg_s = F["normal"].render(self.mensaje, True, msg_col)
            # Fondo del mensaje
            bx, by = 20, self.alto - 120
            msg_bg = pygame.Surface((msg_s.get_width() + 24, msg_s.get_height() + 14), pygame.SRCALPHA)
            msg_bg.fill((40 if es_error else 10, 10, 40 if not es_error else 10, 200))
            msg_bg.set_alpha(alpha)
            surf.blit(msg_bg, (bx - 12, by - 6))
            pygame.draw.rect(surf, msg_col,
                             (bx - 12, by - 6, msg_s.get_width() + 24, msg_s.get_height() + 14),
                             2, border_radius=4)
            msg_s.set_alpha(alpha)
            surf.blit(msg_s, (bx, by))

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
                            (self.ancho - 240 - 20, self.alto - 90, 240, 48),
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
