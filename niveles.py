"""
niveles.py
Datos de cada nivel: situación, evidencias, preguntas, caso a insertar.
"""

from arbol_avl import NodoCaso

# ──────────────────────────────────────────────────────────
#  DEFINICIÓN DE NIVELES
# ──────────────────────────────────────────────────────────

NIVELES = [
    {
        "id": 1,
        "titulo": "Nivel 1 – Las Primeras Señales",
        "historia": (
            "Valeria comienza a recibir mensajes ofensivos en redes\n"
            "sociales. Al principio parecen bromas aisladas, pero se\n"
            "repiten constantemente día tras día."
        ),
        "objetivo": "Recolecta las capturas de pantalla e identifica el tipo de agresión.",
        "evidencias_disponibles": [
            {
                "id": "ev1_1",
                "nombre": "Captura de pantalla",
                "descripcion": "Mensaje ofensivo enviado a Valeria el lunes.",
                "sprite": "captura",
                "posicion": (200, 320),
            },
            {
                "id": "ev1_2",
                "nombre": "Historial de chat",
                "descripcion": "Registro de 14 mensajes ofensivos en una semana.",
                "sprite": "chat",
                "posicion": (420, 280),
            },
            {
                "id": "ev1_3",
                "nombre": "Perfil del agresor",
                "descripcion": "Usuario @shadow99 identificado como emisor.",
                "sprite": "perfil",
                "posicion": (620, 350),
            },
        ],
        "evidencias_requeridas": {"ev1_1", "ev1_2", "ev1_3"},
        "pregunta": {
            "texto": "¿Qué tipo de delito se cometió?",
            "opciones": [
                "Injuria (Art. 220 C.P.)",
                "Calumnia (Art. 221 C.P.)",
                "Suplantación – Ley 1273",
                "Hostigamiento digital",
            ],
            "correcta": 0,
            "explicacion": (
                "Injuria: ofender el honor de alguien mediante palabras,\n"
                "gestos o vías de hecho. Art. 220 del Código Penal Colombiano."
            ),
        },
        "caso": NodoCaso(
            id_caso="CASO-001",
            tipo_acoso="Injuria digital",
            gravedad=3,
            evidencias=["Capturas de mensajes ofensivos", "Historial de chat", "Perfil @shadow99"],
            ley="Art. 220 Código Penal Colombiano",
            pena="Multa de 1 a 3 SMLV",
            descripcion="Mensajes ofensivos repetidos contra Valeria en redes sociales.",
        ),
        "bg_sprite": "bg_ciudad",
        "color_acento": (80, 200, 255),
    },
    {
        "id": 2,
        "titulo": "Nivel 2 – El Rumor Viral",
        "historia": (
            "Publicaciones falsas sobre Valeria empiezan a circular\n"
            "masivamente. Compañeros de colegio las comparten sin\n"
            "verificar, dañando su reputación."
        ),
        "objetivo": "Identifica la publicación original y rastrea quién inició el rumor.",
        "evidencias_disponibles": [
            {
                "id": "ev2_1",
                "nombre": "Post original",
                "descripcion": "Publicación falsa con 200+ compartidos.",
                "sprite": "post",
                "posicion": (180, 300),
            },
            {
                "id": "ev2_2",
                "nombre": "Metadata del post",
                "descripcion": "Hora, IP aproximada y cuenta de origen rastreada.",
                "sprite": "metadata",
                "posicion": (450, 260),
            },
            {
                "id": "ev2_3",
                "nombre": "Testimonios",
                "descripcion": "3 compañeros confirman que el rumor es falso.",
                "sprite": "testimonio",
                "posicion": (640, 330),
            },
            {
                "id": "ev2_4",
                "nombre": "Cuenta eliminada",
                "descripcion": "El agresor eliminó su cuenta tras viralización.",
                "sprite": "cuenta_borrada",
                "posicion": (350, 420),
            },
        ],
        "evidencias_requeridas": {"ev2_1", "ev2_2", "ev2_3"},
        "pregunta": {
            "texto": "¿Cuál es el delito principal cometido?",
            "opciones": [
                "Injuria (Art. 220 C.P.)",
                "Calumnia (Art. 221 C.P.)",
                "Acceso abusivo – Ley 1273",
                "Amenaza digital",
            ],
            "correcta": 1,
            "explicacion": (
                "Calumnia: imputar falsamente a alguien una conducta típica.\n"
                "Art. 221 del Código Penal Colombiano. Pena: multa."
            ),
        },
        "caso": NodoCaso(
            id_caso="CASO-002",
            tipo_acoso="Calumnia en redes",
            gravedad=5,
            evidencias=["Post viral falso", "Metadata de origen", "Testimonios de compañeros"],
            ley="Art. 221 Código Penal Colombiano",
            pena="Multa de 2 a 5 SMLV",
            descripcion="Rumores falsos difundidos masivamente afectando la reputación de Valeria.",
        ),
        "bg_sprite": "bg_red_social",
        "color_acento": (255, 200, 60),
    },
    {
        "id": 3,
        "titulo": "Nivel 3 – La Cuenta Fantasma",
        "historia": (
            "Aparece un perfil falso usando la foto de Valeria.\n"
            "Publica contenido ofensivo haciéndose pasar por ella,\n"
            "atacando a otros usuarios con su identidad."
        ),
        "objetivo": "Analiza el perfil falso y rastrea quién está detrás de la suplantación.",
        "evidencias_disponibles": [
            {
                "id": "ev3_1",
                "nombre": "Perfil falso",
                "descripcion": "Cuenta con foto de Valeria y datos modificados.",
                "sprite": "perfil_falso",
                "posicion": (160, 290),
            },
            {
                "id": "ev3_2",
                "nombre": "IP de creación",
                "descripcion": "Dirección IP registrada al crear la cuenta.",
                "sprite": "ip",
                "posicion": (400, 250),
            },
            {
                "id": "ev3_3",
                "nombre": "Logs de actividad",
                "descripcion": "Registro de accesos y publicaciones del perfil falso.",
                "sprite": "logs",
                "posicion": (620, 310),
            },
            {
                "id": "ev3_4",
                "nombre": "Denuncia de víctimas",
                "descripcion": "Usuarios atacados por el perfil falso presentaron denuncia.",
                "sprite": "denuncia",
                "posicion": (300, 400),
            },
        ],
        "evidencias_requeridas": {"ev3_1", "ev3_2", "ev3_3", "ev3_4"},
        "pregunta": {
            "texto": "¿Qué ley aplica para la suplantación de identidad digital?",
            "opciones": [
                "Art. 220 Código Penal",
                "Ley 1273 de 2009 – Delitos informáticos",
                "Art. 221 Código Penal",
                "Ley 1098 de 2006",
            ],
            "correcta": 1,
            "explicacion": (
                "La Ley 1273 de 2009 tipifica delitos informáticos en Colombia,\n"
                "incluyendo la suplantación de identidad digital. Penas de\n"
                "hasta 8 años de prisión según el daño causado."
            ),
        },
        "caso": NodoCaso(
            id_caso="CASO-003",
            tipo_acoso="Suplantación de identidad",
            gravedad=7,
            evidencias=["Perfil falso detectado", "IP de creación rastreada", "Logs de actividad", "Denuncias recibidas"],
            ley="Ley 1273 de 2009 – Art. 9",
            pena="4 a 8 años de prisión + multa",
            descripcion="Perfil falso con identidad de Valeria usado para atacar otros usuarios.",
        ),
        "bg_sprite": "bg_hacker",
        "color_acento": (255, 80, 120),
    },
    {
        "id": 4,
        "titulo": "Nivel 4 – El Ataque Coordinado",
        "historia": (
            "Varias cuentas atacan a Valeria simultáneamente.\n"
            "El detective descubre que todas pertenecen\n"
            "a la misma persona: el agresor principal."
        ),
        "objetivo": "Encuentra el patrón que conecta todas las cuentas con un solo responsable.",
        "evidencias_disponibles": [
            {
                "id": "ev4_1",
                "nombre": "Análisis de cuentas",
                "descripcion": "5 cuentas distintas con el mismo patrón de escritura.",
                "sprite": "analisis",
                "posicion": (150, 280),
            },
            {
                "id": "ev4_2",
                "nombre": "Horario de ataques",
                "descripcion": "Todas las cuentas activas en los mismos horarios exactos.",
                "sprite": "horario",
                "posicion": (380, 240),
            },
            {
                "id": "ev4_3",
                "nombre": "Dispositivo único",
                "descripcion": "Mismo fingerprint de dispositivo en todas las cuentas.",
                "sprite": "dispositivo",
                "posicion": (600, 300),
            },
            {
                "id": "ev4_4",
                "nombre": "Historial escolar",
                "descripcion": "Conflicto previo entre el agresor y Valeria en el colegio.",
                "sprite": "historial",
                "posicion": (280, 410),
            },
            {
                "id": "ev4_5",
                "nombre": "Testigo digital",
                "descripcion": "Un usuario vio al agresor crear las cuentas en vivo.",
                "sprite": "testigo",
                "posicion": (520, 400),
            },
        ],
        "evidencias_requeridas": {"ev4_1", "ev4_2", "ev4_3", "ev4_4", "ev4_5"},
        "pregunta": {
            "texto": "¿Cuál es el delito más grave cometido en este nivel?",
            "opciones": [
                "Injuria simple",
                "Calumnia leve",
                "Hostigamiento y acoso reiterado digital",
                "Daño informático – Ley 1273",
            ],
            "correcta": 2,
            "explicacion": (
                "El hostigamiento reiterado y coordinado constituye acoso digital\n"
                "agravado. Puede conllevar proceso penal y medidas de protección\n"
                "inmediata para la víctima según la normativa colombiana."
            ),
        },
        "caso": NodoCaso(
            id_caso="CASO-004",
            tipo_acoso="Hostigamiento coordinado",
            gravedad=9,
            evidencias=["5 cuentas del mismo agresor", "Mismo horario de ataques", "Fingerprint único", "Antecedente escolar", "Testigo digital"],
            ley="Ley 1273/2009 + delitos de hostigamiento",
            pena="Proceso penal + medidas de protección",
            descripcion="Campaña coordinada de acoso usando múltiples cuentas falsas.",
        ),
        "bg_sprite": "bg_matrix",
        "color_acento": (180, 80, 255),
    },
]

# ──────────────────────────────────────────────────────────
#  NIVEL FINAL (reporte)
# ──────────────────────────────────────────────────────────

NIVEL_FINAL = {
    "id": 5,
    "titulo": "Nivel Final – La Verdad Detrás del Acoso",
    "historia": (
        "El detective Alex ha reunido todas las evidencias.\n"
        "Es momento de recorrer el árbol completo y reconstruir\n"
        "la línea de hechos para presentar el reporte final."
    ),
    "bg_sprite": "bg_oficina",
    "color_acento": (80, 255, 160),
}
