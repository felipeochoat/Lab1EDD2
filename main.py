"""
main.py  –  CyberDetective: El Árbol de la Verdad
Juego educativo sobre ciberacoso y estructuras de datos (AVL).
 
Requisitos:
    pip install pygame
 
Controles:
    - Clic  → interactuar con botones y evidencias
    - Scroll → desplazar reporte final
"""
 
import sys
import pygame
 
from arbol_avl import ArbolAVL
from visualizador import cargar_sprites
from ui import (
    C, AJUSTES, init_fuentes,
    PantallaMenu, PantallaAyuda, PantallaAjustes,
    PantallaNarrativa, PantallaEvidencias,
    PantallaPregunta, PantallaArbol,
    PantallaReporte,
)
from niveles import generar_niveles   # ← importamos la función, no los datos fijos
 
# ──────────────────────────────────────────────────────────
#  CONFIGURACIÓN
# ──────────────────────────────────────────────────────────
ANCHO, ALTO = 1100, 700
FPS = 60
 
 
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("CyberDetective – El Árbol de la Verdad")
    reloj = pygame.time.Clock()
 
    # ── Música de fondo ───────────────────────────────────
    import os
    music_path = os.path.join(os.path.dirname(__file__), "music_cyberpunk.wav")
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(AJUSTES["volumen"])
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"[música] No se pudo cargar: {e}")
 
    init_fuentes()
    sprites = cargar_sprites(ANCHO, ALTO)
 
    arbol = ArbolAVL()
 
    # ── Estado global ─────────────────────────────────────
    estado = "menu"
    nivel_idx = 0
    pantalla_actual = None
    respuesta_correcta = False
 
    # Estos se generan al pulsar "Jugar" (ver ir_a → "narrativa")
    NIVELES = []
    NIVEL_FINAL = {}
 
    def nueva_partida():
        """Genera niveles frescos y reinicia el árbol."""
        nonlocal NIVELES, NIVEL_FINAL
        NIVELES, NIVEL_FINAL = generar_niveles()
        arbol.__init__()
 
    def ir_a(nuevo_estado):
        nonlocal estado, pantalla_actual, nivel_idx, respuesta_correcta
 
        estado = nuevo_estado
 
        if nuevo_estado == "menu":
            pantalla_actual = PantallaMenu(ANCHO, ALTO, sprites)
 
        elif nuevo_estado == "ayuda":
            pantalla_actual = PantallaAyuda(ANCHO, ALTO)
 
        elif nuevo_estado == "ajustes":
            pantalla_actual = PantallaAjustes(ANCHO, ALTO)
 
        elif nuevo_estado == "narrativa":
            if nivel_idx < len(NIVELES):
                datos = NIVELES[nivel_idx]
            else:
                datos = NIVEL_FINAL
            pantalla_actual = PantallaNarrativa(ANCHO, ALTO, datos, sprites)
 
        elif nuevo_estado == "evidencias":
            datos = NIVELES[nivel_idx]
            pantalla_actual = PantallaEvidencias(ANCHO, ALTO, datos, sprites)
 
        elif nuevo_estado == "pregunta":
            datos = NIVELES[nivel_idx]
            pantalla_actual = PantallaPregunta(ANCHO, ALTO, datos)
 
        elif nuevo_estado == "arbol":
            datos = NIVELES[nivel_idx]
            caso = datos["caso"]
            arbol.insertar(caso)
            pantalla_actual = PantallaArbol(ANCHO, ALTO, arbol, caso, sprites)
 
        elif nuevo_estado == "reporte":
            pantalla_actual = PantallaReporte(ANCHO, ALTO, arbol)
 
    # Estado inicial
    ir_a("menu")
 
    # ── Loop principal ────────────────────────────────────
    corriendo = True
    while corriendo:
        reloj.tick(FPS)
        pos_mouse = pygame.mouse.get_pos()
 
        eventos = []
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                corriendo = False
            else:
                eventos.append(ev)
 
        resultado = pantalla_actual.actualizar(eventos, pos_mouse)
 
        if resultado:
            if estado == "menu":
                if resultado == "jugar":
                    # ← Aquí se generan los niveles aleatorios nuevos
                    nueva_partida()
                    nivel_idx = 0
                    ir_a("narrativa")
                elif resultado == "ayuda":
                    ir_a("ayuda")
                elif resultado == "ajustes":
                    ir_a("ajustes")
                elif resultado == "salir":
                    corriendo = False
 
            elif estado == "ayuda":
                if resultado == "menu":
                    ir_a("menu")
 
            elif estado == "ajustes":
                if resultado == "menu":
                    ir_a("menu")
 
            elif estado == "narrativa":
                if resultado == "evidencias":
                    if nivel_idx < len(NIVELES):
                        ir_a("evidencias")
                    else:
                        ir_a("reporte")
 
            elif estado == "evidencias":
                if resultado == "pregunta":
                    ir_a("pregunta")
 
            elif estado == "pregunta":
                if resultado == "arbol":
                    ir_a("arbol")
 
            elif estado == "arbol":
                if resultado == "siguiente":
                    nivel_idx += 1
                    if nivel_idx < len(NIVELES):
                        ir_a("narrativa")
                    else:
                        ir_a("narrativa")   # narrativa del nivel final
 
            elif estado == "reporte":
                if resultado == "menu":
                    nivel_idx = 0
                    ir_a("menu")
 
        pantalla_actual.dibujar(pantalla)
        pygame.display.flip()
 
    pygame.quit()
    sys.exit()
 
 
if __name__ == "__main__":
    main()