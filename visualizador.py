"""
visualizador.py
Manejo de sprites y assets gráficos para CyberDetective.
Genera placeholders pixel-art cuando no hay imágenes reales.
"""

import pygame
from ui import C, F, RADIO_NODO


def _px(surf, color, x, y, size=1):
    """Dibuja un 'pixel' de tamaño size."""
    pygame.draw.rect(surf, color, (x, y, size, size))


# ──────────────────────────────────────────────────────────
#  GENERADORES DE SPRITES PLACEHOLDER (pixel-art sintético)
# ──────────────────────────────────────────────────────────

def _sprite_captura(w=40, h=40):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    # Marco de pantalla
    pygame.draw.rect(s, (60, 120, 200), (2, 2, w-4, h-4), 2)
    # Líneas de texto simulado
    for i in range(3):
        pygame.draw.rect(s, (80, 180, 255), (6, 10 + i*8, 28, 3))
    # Ícono de cámara
    pygame.draw.rect(s, (255, 200, 60), (14, 26, 12, 8))
    pygame.draw.circle(s, (255, 200, 60), (20, 30), 3)
    return s

def _sprite_chat(w=40, h=40):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    # Burbuja de chat
    pygame.draw.rect(s, (40, 160, 80), (2, 4, 30, 20), border_radius=4)
    pygame.draw.polygon(s, (40, 160, 80), [(6, 24), (2, 30), (14, 24)])
    for i in range(2):
        pygame.draw.rect(s, (200, 255, 200), (6, 10 + i*6, 22, 3))
    # Segunda burbuja (respuesta)
    pygame.draw.rect(s, (80, 80, 140), (8, 30, 30, 8), border_radius=3)
    return s

def _sprite_perfil(w=40, h=40):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.circle(s, (80, 130, 200), (20, 14), 10)
    pygame.draw.ellipse(s, (80, 130, 200), (4, 26, 32, 14))
    pygame.draw.circle(s, (200, 220, 255), (20, 14), 7)
    return s

def _sprite_perfil_falso(w=40, h=40):
    s = _sprite_perfil(w, h)
    # Cruz roja encima
    pygame.draw.line(s, (220, 60, 60), (0, 0), (w, h), 3)
    pygame.draw.line(s, (220, 60, 60), (w, 0), (0, h), 3)
    return s

def _sprite_post(w=40, h=40):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, (30, 50, 90), (0, 0, w, h), border_radius=3)
    pygame.draw.rect(s, (255, 80, 80), (0, 0, w, h), 2, border_radius=3)
    for i in range(3):
        pygame.draw.rect(s, (200, 100, 100), (4, 6 + i*10, 32, 4))
    return s

def _sprite_metadata(w=40, h=40):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, (20, 40, 70), (0, 0, w, h))
    # Ícono de lupa
    pygame.draw.circle(s, (80, 200, 255), (16, 16), 9, 3)
    pygame.draw.line(s, (80, 200, 255), (23, 23), (34, 34), 3)
    return s

def _sprite_testimonio(w=40, h=40):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    # Persona
    pygame.draw.circle(s, (200, 180, 140), (20, 12), 7)
    pygame.draw.ellipse(s, (200, 180, 140), (8, 22, 24, 14))
    # Comillas
    pygame.draw.rect(s, (255, 200, 60), (6, 32, 4, 6))
    pygame.draw.rect(s, (255, 200, 60), (12, 32, 4, 6))
    return s

def _sprite_ip(w=40, h=40):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, (20, 40, 70), (2, 8, 36, 28), border_radius=3)
    pygame.draw.rect(s, (80, 200, 255), (2, 8, 36, 28), 2, border_radius=3)
    for i in range(3):
        pygame.draw.rect(s, (80, 200, 255), (6, 14 + i*7, 28, 3))
    return s

def _sprite_logs(w=40, h=40):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, (10, 20, 10), (0, 0, w, h))
    cols = [(0, 255, 0), (0, 200, 0), (0, 150, 0), (0, 100, 0)]
    for i in range(4):
        pygame.draw.rect(s, cols[i], (4, 4 + i*9, 32, 4))
    return s

def _sprite_denuncia(w=40, h=40):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, (240, 230, 200), (4, 2, 32, 36), border_radius=2)
    pygame.draw.rect(s, (200, 60, 60), (4, 2, 32, 36), 2, border_radius=2)
    for i in range(4):
        pygame.draw.rect(s, (150, 100, 80), (8, 8 + i*7, 24, 3))
    return s

def _sprite_analisis(w=40, h=40):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    # Grafo pequeño
    puntos = [(10, 20), (30, 10), (30, 30), (20, 35)]
    for p in puntos:
        pygame.draw.circle(s, (160, 80, 255), p, 4)
    pygame.draw.line(s, (160, 80, 255), puntos[0], puntos[1], 2)
    pygame.draw.line(s, (160, 80, 255), puntos[0], puntos[2], 2)
    pygame.draw.line(s, (160, 80, 255), puntos[1], puntos[3], 2)
    return s

def _sprite_horario(w=40, h=40):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.circle(s, (80, 80, 140), (20, 20), 16, 3)
    pygame.draw.line(s, (255, 200, 60), (20, 20), (20, 8), 3)
    pygame.draw.line(s, (255, 200, 60), (20, 20), (30, 20), 2)
    return s

def _sprite_dispositivo(w=40, h=40):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, (40, 40, 80), (8, 2, 24, 36), border_radius=3)
    pygame.draw.rect(s, (80, 200, 255), (8, 2, 24, 36), 2, border_radius=3)
    pygame.draw.rect(s, (80, 200, 255), (10, 6, 20, 22))
    pygame.draw.circle(s, (255, 255, 255), (20, 34), 2)
    return s

def _sprite_historial(w=40, h=40):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(s, (240, 220, 180), (4, 2, 32, 36), border_radius=2)
    pygame.draw.rect(s, (180, 140, 80), (4, 2, 32, 36), 2, border_radius=2)
    for i in range(5):
        pygame.draw.rect(s, (120, 80, 40), (8, 8 + i*5, 24, 2))
    return s

def _sprite_testigo(w=40, h=40):
    s = _sprite_testimonio(w, h)
    # Ojo extra
    pygame.draw.circle(s, (80, 200, 255), (20, 12), 4, 2)
    pygame.draw.circle(s, (80, 200, 255), (20, 12), 2)
    return s

def _sprite_cuenta_borrada(w=40, h=40):
    s = _sprite_perfil(w, h)
    # Tachado
    pygame.draw.line(s, (220, 60, 60), (2, 2), (38, 38), 4)
    return s

def _sprite_bg(ancho, alto, color_base, patron="cuadricula"):
    s = pygame.Surface((ancho, alto))
    s.fill(color_base)
    c_linea = tuple(min(255, v + 15) for v in color_base)
    if patron == "cuadricula":
        for x in range(0, ancho, 40):
            pygame.draw.line(s, c_linea, (x, 0), (x, alto), 1)
        for y in range(0, alto, 40):
            pygame.draw.line(s, c_linea, (0, y), (ancho, y), 1)
    elif patron == "diagonal":
        for i in range(-alto, ancho, 30):
            pygame.draw.line(s, c_linea, (i, 0), (i + alto, alto), 1)
    elif patron == "puntos":
        for x in range(0, ancho, 20):
            for y in range(0, alto, 20):
                pygame.draw.rect(s, c_linea, (x, y, 2, 2))
    return s


# ──────────────────────────────────────────────────────────
#  CARGADOR DE SPRITES
# ──────────────────────────────────────────────────────────

def cargar_sprites(ancho, alto):
    """
    Intenta cargar imágenes reales de /assets/.
    Si no existen, genera placeholders pixel-art.
    Retorna dict: { nombre: Surface }
    """
    sprites = {}
    escala_icono = (40, 40)

    # Iconos de evidencia
    generadores = {
        "captura":       _sprite_captura,
        "chat":          _sprite_chat,
        "perfil":        _sprite_perfil,
        "perfil_falso":  _sprite_perfil_falso,
        "post":          _sprite_post,
        "metadata":      _sprite_metadata,
        "testimonio":    _sprite_testimonio,
        "ip":            _sprite_ip,
        "logs":          _sprite_logs,
        "denuncia":      _sprite_denuncia,
        "analisis":      _sprite_analisis,
        "horario":       _sprite_horario,
        "dispositivo":   _sprite_dispositivo,
        "historial":     _sprite_historial,
        "testigo":       _sprite_testigo,
        "cuenta_borrada":_sprite_cuenta_borrada,
    }

    for nombre, gen in generadores.items():
        try:
            img = pygame.image.load(f"assets/{nombre}.png").convert_alpha()
            sprites[nombre] = pygame.transform.scale(img, escala_icono)
        except Exception:
            sprites[nombre] = gen()

    # Fondos
    bg_configs = {
        "bg_ciudad":     ((10, 14, 26), "cuadricula"),
        "bg_red_social": ((14, 20, 36), "diagonal"),
        "bg_hacker":     ((8,  16,  8), "cuadricula"),
        "bg_matrix":     ((6,  12,  6), "puntos"),
        "bg_oficina":    ((20, 18, 30), "diagonal"),
    }
    for nombre, (color, patron) in bg_configs.items():
        try:
            img = pygame.image.load(f"assets/{nombre}.png").convert()
            sprites[nombre] = pygame.transform.scale(img, (ancho, alto))
        except Exception:
            sprites[nombre] = _sprite_bg(ancho, alto, color, patron)

    # Imágenes de escena narrativa (una por nivel)
    escenas = [
        "escena_injuria",
        "escena_calumnia",
        "escena_suplantacion",
        "escena_hostigamiento",
        "escena_final",
    ]
    for nombre in escenas:
        try:
            img = pygame.image.load(f"assets/{nombre}.png").convert_alpha()
            sprites[nombre] = pygame.transform.scale(img, (500, 320))
        except Exception:
            sprites[nombre] = None  # PantallaNarrativa lo ignora si es None

    # Logo / título
    try:
        logo = pygame.image.load("assets/logo.png").convert_alpha()
        sprites["logo"] = pygame.transform.scale(logo, (500, 100))
    except Exception:
        sprites["logo"] = None  # ui.py manejará el fallback

    return sprites
