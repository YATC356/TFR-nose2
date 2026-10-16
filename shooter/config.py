"""
Configuracion central del juego.

Unico modulo de constantes compartido por todas las capas.
RESTRICCION: no importa pygame, para que el dominio (capas 1-3)
pueda usarlo sin arrastrar la dependencia de renderizado.
"""

# --- Mapa y ciclo de vida ----------------------------------------------------
ANCHO = 800                      # ancho de la ventana / mapa (px)
ALTO = 600                       # alto de la ventana / mapa (px)
FPS = 60                         # frecuencia de refresco

# --- Reglas de negocio -------------------------------------------------------
COOLDOWN_DISPARO_MS = 200        # RN-01: cadencia maxima de disparo (ms)
RECARGA_MS = 200                 # "tiempo de recarga" del Player (RN-01)
PUNTOS_POR_IMPACTO = 10          # RN-02
VIDAS_INICIALES = 3              # vidas de cada jugador

# --- Velocidades (px / segundo) ---------------------------------------------
VEL_JUGADOR = 320.0
VEL_PROYECTIL = 540.0            # hacia arriba
VEL_ENEMIGO_BASE = 110.0         # hacia abajo

# --- Dimensiones de las entidades -------------------------------------------
NAVE_ANCHO, NAVE_ALTO = 64, 28
PROYECTIL_ANCHO, PROYECTIL_ALTO = 6, 14
ENEMIGO_RADIO = 18

# --- Temporizador de aparicion de enemigos -----------------------------------
SPAWN_MS = 900                   # intervalo de generacion (ms)
