"""
niveles.py  –  CyberDetective: El Árbol de la Verdad
Generación aleatoria de niveles: mismo tipo de delito por nivel,
pero con víctimas, agresores, evidencias y gravedad distintos
en cada partida. Llama a generar_niveles() al inicio de cada juego.
"""
 
import random
from arbol_avl import NodoCaso
 
# ──────────────────────────────────────────────────────────
#  BANCOS DE DATOS ALEATORIOS
# ──────────────────────────────────────────────────────────
 
_VICTIMAS = [
    "Valeria", "Sofía", "Daniela", "Camila", "Luciana",
    "Mariana", "Isabella", "Natalia", "Gabriela", "Alejandra",
]
 
_AGRESORES_USUARIO = [
    "@shadow99", "@dark_wolf", "@ghost_fx", "@neon_viper",
    "@ctrl_alt_evil", "@byte_hater", "@null_ptr", "@xX_toxic_Xx",
    "@anon_storm", "@pixel_rage",
]
 
_AGRESORES_NOMBRE = [
    "Andrés M.", "Carlos R.", "Diego F.", "Sebastián L.",
    "Mateo G.", "Nicolás H.", "Julián P.", "Santiago V.",
]
 
_PLATAFORMAS = [
    "Instagram", "TikTok", "Twitter/X", "Facebook",
    "WhatsApp", "Discord", "Snapchat", "Telegram",
]
 
_COLEGIOS = [
    "el Colegio Distrital Simón Bolívar",
    "la I.E. Técnica Industrial",
    "el Colegio Nacional San José",
    "la Institución Educativa La Esperanza",
    "el Colegio Cooperativo del Norte",
]
 
# Rangos de gravedad por nivel (sin solapamiento para el AVL)
# Nivel 1: Injuria       → 1-3
# Nivel 2: Calumnia      → 4-5
# Nivel 3: Suplantación  → 6-7
# Nivel 4: Hostigamiento → 8-10
_RANGOS_GRAVEDAD = [
    (1, 3),   # nivel 1
    (4, 5),   # nivel 2
    (6, 7),   # nivel 3
    (8, 10),  # nivel 4
]
 
# ──────────────────────────────────────────────────────────
#  GENERADORES POR NIVEL
# ──────────────────────────────────────────────────────────
 
def _nivel_1_injuria(victima, agresor_user, agresor_nombre, plataforma, colegio, gravedad):
    """
    Nivel 1 – Injuria digital (Art. 220 C.P.)
    Varía: cantidad de mensajes, días, plataforma, usuarios.
    """
    num_mensajes = random.randint(8, 30)
    num_dias     = random.randint(3, 14)
    variantes_historia = [
        (
            f"{victima} comienza a recibir mensajes ofensivos en {plataforma}.\n"
            f"Al principio parecen bromas, pero {agresor_user} lleva\n"
            f"{num_dias} días enviando {num_mensajes} insultos."
        ),
        (
            f"En el grupo de {colegio}, {agresor_user}\n"
            f"publica comentarios hirientes sobre {victima} durante\n"
            f"{num_dias} días consecutivos."
        ),
        (
            f"{victima} descubre que {agresor_user} lleva semanas\n"
            f"enviando mensajes ofensivos desde {plataforma}.\n"
            f"Ya acumula {num_mensajes} insultos documentados."
        ),
    ]
    historia = random.choice(variantes_historia)
 
    evidencias_disponibles = [
        {
            "id": "ev1_1",
            "nombre": "Captura de pantalla",
            "descripcion": f"Mensaje ofensivo de {agresor_user} hacia {victima}.",
            "sprite": "captura",
            "posicion": (200, 320),
        },
        {
            "id": "ev1_2",
            "nombre": "Historial de chat",
            "descripcion": f"Registro de {num_mensajes} mensajes ofensivos en {num_dias} días.",
            "sprite": "chat",
            "posicion": (420, 280),
        },
        {
            "id": "ev1_3",
            "nombre": "Perfil del agresor",
            "descripcion": f"Usuario {agresor_user} identificado como emisor.",
            "sprite": "perfil",
            "posicion": (620, 350),
        },
    ]
 
    caso = NodoCaso(
        id_caso=f"CASO-{random.randint(1000, 9999)}",
        tipo_acoso="Injuria digital",
        gravedad=gravedad,
        evidencias=[
            f"Capturas de {num_mensajes} mensajes ofensivos",
            f"Historial de chat en {plataforma}",
            f"Perfil {agresor_user}",
        ],
        ley="Art. 220 Código Penal Colombiano",
        pena="Multa de 1 a 3 SMLV",
        descripcion=(
            f"Mensajes ofensivos repetidos de {agresor_user} "
            f"contra {victima} en {plataforma}. "
            f"Gravedad registrada: {gravedad}/10."
        ),
    )
 
    return {
        "id": 1,
        "titulo": "Nivel 1 – Las Primeras Señales",
        "historia": historia,
        "objetivo": "Recolecta las capturas de pantalla e identifica el tipo de agresión.",
        "evidencias_disponibles": evidencias_disponibles,
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
                "gestos o vías de hecho. Art. 220 del Código Penal Colombiano.\n"
                f"En este caso, {agresor_user} envió {num_mensajes} mensajes ofensivos."
            ),
        },
        "caso": caso,
        "bg_sprite": "bg_ciudad",
        "escena_sprite": "escena_injuria",
        "color_acento": (80, 200, 255),
        # Metadatos visibles en el reporte final
        "_victima": victima,
        "_agresor_user": agresor_user,
        "_agresor_nombre": agresor_nombre,
        "_plataforma": plataforma,
        "_gravedad": gravedad,
    }
 
 
def _nivel_2_calumnia(victima, agresor_user, agresor_nombre, plataforma, colegio, gravedad):
    """
    Nivel 2 – Calumnia en redes (Art. 221 C.P.)
    Varía: compartidos, origen del rumor, testimonios.
    """
    num_compartidos  = random.randint(50, 500)
    num_testimonios  = random.randint(2, 6)
    tipo_rumor = random.choice([
        f"acusaciones falsas de robo contra {victima}",
        f"fotos editadas que difaman a {victima}",
        f"historia inventada que implica a {victima} en una pelea",
        f"capturas falsas de conversaciones de {victima}",
    ])
    variantes_historia = [
        (
            f"Un post con {tipo_rumor} circula en {plataforma}\n"
            f"con {num_compartidos}+ compartidos. {agresor_nombre}\n"
            f"es señalado como el origen del rumor."
        ),
        (
            f"{agresor_user} publica {tipo_rumor} en {plataforma}.\n"
            f"El post se viraliza con {num_compartidos} compartidos\n"
            f"antes de que {victima} pueda reaccionar."
        ),
        (
            f"Compañeros de {colegio} comparten masivamente\n"
            f"{tipo_rumor} iniciado por {agresor_user},\n"
            f"acumulando {num_compartidos} interacciones."
        ),
    ]
    historia = random.choice(variantes_historia)
 
    evidencias_disponibles = [
        {
            "id": "ev2_1",
            "nombre": "Post original",
            "descripcion": f"Publicación falsa con {num_compartidos}+ compartidos.",
            "sprite": "post",
            "posicion": (180, 300),
        },
        {
            "id": "ev2_2",
            "nombre": "Metadata del post",
            "descripcion": f"IP aproximada y cuenta de origen rastreada a {agresor_nombre}.",
            "sprite": "metadata",
            "posicion": (450, 260),
        },
        {
            "id": "ev2_3",
            "nombre": "Testimonios",
            "descripcion": f"{num_testimonios} compañeros confirman que el rumor es falso.",
            "sprite": "testimonio",
            "posicion": (640, 330),
        },
        {
            "id": "ev2_4",
            "nombre": "Cuenta eliminada",
            "descripcion": f"{agresor_user} eliminó su cuenta tras la viralización.",
            "sprite": "cuenta_borrada",
            "posicion": (350, 420),
        },
    ]
 
    caso = NodoCaso(
        id_caso=f"CASO-{random.randint(1000, 9999)}",
        tipo_acoso="Calumnia en redes",
        gravedad=gravedad,
        evidencias=[
            f"Post viral falso ({num_compartidos} compartidos)",
            f"Metadata de origen: {agresor_nombre}",
            f"{num_testimonios} testimonios de compañeros",
        ],
        ley="Art. 221 Código Penal Colombiano",
        pena="Multa de 2 a 5 SMLV",
        descripcion=(
            f"Rumores falsos de {agresor_user} difundidos en {plataforma} "
            f"afectando la reputación de {victima}. "
            f"Gravedad: {gravedad}/10."
        ),
    )
 
    return {
        "id": 2,
        "titulo": "Nivel 2 – El Rumor Viral",
        "historia": historia,
        "objetivo": "Identifica la publicación original y rastrea quién inició el rumor.",
        "evidencias_disponibles": evidencias_disponibles,
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
                "Art. 221 del Código Penal Colombiano. Pena: multa.\n"
                f"{agresor_user} difundió {tipo_rumor}."
            ),
        },
        "caso": caso,
        "bg_sprite": "bg_red_social",
        "escena_sprite": "escena_calumnia",
        "color_acento": (255, 200, 60),
        "_victima": victima,
        "_agresor_user": agresor_user,
        "_agresor_nombre": agresor_nombre,
        "_plataforma": plataforma,
        "_gravedad": gravedad,
    }
 
 
def _nivel_3_suplantacion(victima, agresor_user, agresor_nombre, plataforma, colegio, gravedad):
    """
    Nivel 3 – Suplantación de identidad (Ley 1273/2009)
    Varía: tipo de contenido publicado, víctimas secundarias.
    """
    num_victimas_sec = random.randint(3, 12)
    tipo_contenido = random.choice([
        f"insultos dirigidos a compañeros de {colegio}",
        "fotos editadas ofensivas",
        "mensajes de odio hacia otros usuarios",
        "solicitudes de dinero a conocidos de la víctima",
        "contenido inapropiado en nombre de la víctima",
    ])
    variantes_historia = [
        (
            f"Aparece un perfil falso usando la foto de {victima} en {plataforma}.\n"
            f"Publica {tipo_contenido}, atacando\n"
            f"a {num_victimas_sec} usuarios con su identidad."
        ),
        (
            f"{agresor_user} crea una cuenta clonada de {victima}\n"
            f"en {plataforma} y comienza a publicar {tipo_contenido}.\n"
            f"{num_victimas_sec} personas ya han recibido ataques."
        ),
        (
            f"Una cuenta idéntica a la de {victima} aparece en {plataforma}.\n"
            f"Detrás está {agresor_nombre}, publicando {tipo_contenido}\n"
            f"y afectando a {num_victimas_sec} usuarios inocentes."
        ),
    ]
    historia = random.choice(variantes_historia)
 
    evidencias_disponibles = [
        {
            "id": "ev3_1",
            "nombre": "Perfil falso",
            "descripcion": f"Cuenta en {plataforma} con foto de {victima} y datos falsos.",
            "sprite": "perfil_falso",
            "posicion": (160, 290),
        },
        {
            "id": "ev3_2",
            "nombre": "IP de creación",
            "descripcion": f"IP registrada al crear la cuenta, vinculada a {agresor_nombre}.",
            "sprite": "ip",
            "posicion": (400, 250),
        },
        {
            "id": "ev3_3",
            "nombre": "Logs de actividad",
            "descripcion": f"Registro de accesos y publicaciones del perfil falso.",
            "sprite": "logs",
            "posicion": (620, 310),
        },
        {
            "id": "ev3_4",
            "nombre": "Denuncia de víctimas",
            "descripcion": f"{num_victimas_sec} usuarios atacados presentaron denuncia.",
            "sprite": "denuncia",
            "posicion": (300, 400),
        },
    ]
 
    caso = NodoCaso(
        id_caso=f"CASO-{random.randint(1000, 9999)}",
        tipo_acoso="Suplantación de identidad",
        gravedad=gravedad,
        evidencias=[
            f"Perfil falso en {plataforma}",
            f"IP vinculada a {agresor_nombre}",
            "Logs de actividad",
            f"{num_victimas_sec} denuncias de víctimas secundarias",
        ],
        ley="Ley 1273 de 2009 – Art. 9",
        pena="4 a 8 años de prisión + multa",
        descripcion=(
            f"Perfil falso de {victima} en {plataforma} usado por {agresor_user} "
            f"para publicar {tipo_contenido}. "
            f"Gravedad: {gravedad}/10."
        ),
    )
 
    return {
        "id": 3,
        "titulo": "Nivel 3 – La Cuenta Fantasma",
        "historia": historia,
        "objetivo": "Analiza el perfil falso y rastrea quién está detrás de la suplantación.",
        "evidencias_disponibles": evidencias_disponibles,
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
                "incluyendo la suplantación de identidad digital.\n"
                f"Penas de hasta 8 años. {agresor_nombre} creó un perfil falso de {victima}."
            ),
        },
        "caso": caso,
        "bg_sprite": "bg_hacker",
        "escena_sprite": "escena_suplantacion",
        "color_acento": (255, 80, 120),
        "_victima": victima,
        "_agresor_user": agresor_user,
        "_agresor_nombre": agresor_nombre,
        "_plataforma": plataforma,
        "_gravedad": gravedad,
    }
 
 
def _nivel_4_hostigamiento(victima, agresor_user, agresor_nombre, plataforma, colegio, gravedad):
    """
    Nivel 4 – Hostigamiento coordinado (Ley 1273 + acoso reiterado)
    Varía: número de cuentas, duración, tipo de ataques.
    """
    num_cuentas  = random.randint(3, 8)
    num_semanas  = random.randint(2, 6)
    tipo_ataque = random.choice([
        "mensajes de amenaza y hostigamiento",
        "ataques organizados con insultos coordinados",
        "campañas de desprestigio con noticias falsas",
        "spam masivo y reporte falso de cuentas",
    ])
    variantes_historia = [
        (
            f"{num_cuentas} cuentas distintas atacan a {victima} en {plataforma}\n"
            f"con {tipo_ataque} durante {num_semanas} semanas.\n"
            f"Todas pertenecen a {agresor_nombre}."
        ),
        (
            f"El detective descubre que {agresor_user} creó {num_cuentas} perfiles\n"
            f"para coordinar {tipo_ataque} contra {victima}.\n"
            f"La campaña lleva {num_semanas} semanas activa."
        ),
        (
            f"En {plataforma}, {num_cuentas} cuentas lanzan {tipo_ataque}\n"
            f"contra {victima} simultáneamente durante {num_semanas} semanas.\n"
            f"El rastreo apunta a {agresor_nombre} como autor."
        ),
    ]
    historia = random.choice(variantes_historia)
 
    evidencias_disponibles = [
        {
            "id": "ev4_1",
            "nombre": "Análisis de cuentas",
            "descripcion": f"{num_cuentas} cuentas con el mismo patrón de escritura.",
            "sprite": "analisis",
            "posicion": (150, 280),
        },
        {
            "id": "ev4_2",
            "nombre": "Horario de ataques",
            "descripcion": f"Todas activas en los mismos horarios durante {num_semanas} semanas.",
            "sprite": "horario",
            "posicion": (380, 240),
        },
        {
            "id": "ev4_3",
            "nombre": "Dispositivo único",
            "descripcion": f"Mismo fingerprint de dispositivo en las {num_cuentas} cuentas.",
            "sprite": "dispositivo",
            "posicion": (600, 300),
        },
        {
            "id": "ev4_4",
            "nombre": "Historial escolar",
            "descripcion": f"Conflicto previo entre {agresor_nombre} y {victima} en {colegio}.",
            "sprite": "historial",
            "posicion": (280, 410),
        },
        {
            "id": "ev4_5",
            "nombre": "Testigo digital",
            "descripcion": f"Un usuario vio a {agresor_user} crear las cuentas en vivo.",
            "sprite": "testigo",
            "posicion": (520, 400),
        },
    ]
 
    caso = NodoCaso(
        id_caso=f"CASO-{random.randint(1000, 9999)}",
        tipo_acoso="Hostigamiento coordinado",
        gravedad=gravedad,
        evidencias=[
            f"{num_cuentas} cuentas del mismo agresor",
            f"Mismo horario de ataques ({num_semanas} semanas)",
            "Fingerprint único de dispositivo",
            f"Antecedente escolar con {victima}",
            "Testigo digital",
        ],
        ley="Ley 1273/2009 + delitos de hostigamiento",
        pena="Proceso penal + medidas de protección",
        descripcion=(
            f"Campaña coordinada de {agresor_nombre} usando {num_cuentas} cuentas "
            f"para hostigar a {victima} en {plataforma} durante {num_semanas} semanas. "
            f"Gravedad: {gravedad}/10."
        ),
    )
 
    return {
        "id": 4,
        "titulo": "Nivel 4 – El Ataque Coordinado",
        "historia": historia,
        "objetivo": "Encuentra el patrón que conecta todas las cuentas con un solo responsable.",
        "evidencias_disponibles": evidencias_disponibles,
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
                "El hostigamiento reiterado y coordinado constituye acoso digital agravado.\n"
                "Puede conllevar proceso penal y medidas de protección inmediata.\n"
                f"{agresor_nombre} operó {num_cuentas} cuentas durante {num_semanas} semanas."
            ),
        },
        "caso": caso,
        "bg_sprite": "bg_matrix",
        "escena_sprite": "escena_hostigamiento",
        "color_acento": (180, 80, 255),
        "_victima": victima,
        "_agresor_user": agresor_user,
        "_agresor_nombre": agresor_nombre,
        "_plataforma": plataforma,
        "_gravedad": gravedad,
    }
 
 
# ──────────────────────────────────────────────────────────
#  FUNCIÓN PRINCIPAL: generar_niveles()
# ──────────────────────────────────────────────────────────
 
def generar_niveles():
    """
    Genera los 4 niveles del juego con valores aleatorios.
    Llama a esta función cada vez que inicia una nueva partida.
    Garantiza que las gravedades sean únicas (sin colisión en el AVL).
 
    Retorna: lista NIVELES y dict NIVEL_FINAL
    """
 
    # Sortear personajes (víctima distinta en cada nivel para más variedad)
    victimas    = random.sample(_VICTIMAS, 4)
    agresores_u = random.choices(_AGRESORES_USUARIO, k=4)
    agresores_n = random.choices(_AGRESORES_NOMBRE, k=4)
    plataformas = random.choices(_PLATAFORMAS, k=4)
    colegios    = random.choices(_COLEGIOS, k=4)
 
    # Seleccionar una gravedad única por nivel dentro de su rango
    gravedades_usadas = set()
    gravedades = []
    for rango_min, rango_max in _RANGOS_GRAVEDAD:
        candidatos = [g for g in range(rango_min, rango_max + 1)
                      if g not in gravedades_usadas]
        gravedad = random.choice(candidatos)
        gravedades_usadas.add(gravedad)
        gravedades.append(gravedad)
 
    generadores = [
        _nivel_1_injuria,
        _nivel_2_calumnia,
        _nivel_3_suplantacion,
        _nivel_4_hostigamiento,
    ]
 
    niveles = []
    for i, gen in enumerate(generadores):
        nivel = gen(
            victima        = victimas[i],
            agresor_user   = agresores_u[i],
            agresor_nombre = agresores_n[i],
            plataforma     = plataformas[i],
            colegio        = colegios[i],
            gravedad       = gravedades[i],
        )
        niveles.append(nivel)
 
    nivel_final = {
        "id": 5,
        "titulo": "Nivel Final – La Verdad Detrás del Acoso",
        "historia": (
            "El detective Alex ha reunido todas las evidencias.\n"
            "Es momento de recorrer el árbol completo y reconstruir\n"
            "la línea de hechos para presentar el reporte final."
        ),
        "bg_sprite": "bg_oficina",
        "escena_sprite": "escena_final",
        "color_acento": (80, 255, 160),
    }
 
    return niveles, nivel_final
 
 
# ──────────────────────────────────────────────────────────
#  COMPATIBILIDAD: NIVELES y NIVEL_FINAL globales
#  (se regeneran en cada importación Y al llamar generar_niveles)
# ──────────────────────────────────────────────────────────
NIVELES, NIVEL_FINAL = generar_niveles()