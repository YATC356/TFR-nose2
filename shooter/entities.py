"""
CAPA 2: Modelo del Dominio (Python puro).

RESTRICCION CRITICA: ninguna de estas clases importa ni instanciona objetos
de `pygame` (ni `pygame.Rect` ni `pygame.Surface`); las colisiones se
calculan algebraicamente.
"""

from .config import (
    ENEMIGO_RADIO,
    NAVE_ALTO,
    NAVE_ANCHO,
    PROYECTIL_ALTO,
    PROYECTIL_ANCHO,
    RECARGA_MS,
    VEL_ENEMIGO_BASE,
    VEL_JUGADOR,
    VEL_PROYECTIL,
    VIDAS_INICIALES,
)


class Player:
    """La nave del jugador: coordenadas, dimensiones, velocidad y cadencia."""

    def __init__(self, player_id: int, x: float, y: float) -> None:
        self.id = player_id
        self.x = float(x)
        self.y = float(y)
        self.width = NAVE_ANCHO
        self.height = NAVE_ALTO
        self.speed = VEL_JUGADOR
        self.last_shot_time = 0.0      # ms del disparo anterior (RN-01)
        self.reload_time = RECARGA_MS  # ms minimos entre disparos
        self.lives = VIDAS_INICIALES
        self.intent = 0                # -1 izquierda, 0 quieto, +1 derecha

    @property
    def alive(self) -> bool:
        return self.lives > 0


class Bullet:
    """Proyectil vertical (rectangulo) que sube hacia los enemigos."""

    def __init__(self, x: float, y: float) -> None:
        self.x = float(x)
        self.y = float(y)
        self.width = PROYECTIL_ANCHO
        self.height = PROYECTIL_ALTO
        self.speed = VEL_PROYECTIL


class Enemy:
    """Obstaculo circular que baja hacia la nave."""

    def __init__(self, x: float, y: float, speed: float = VEL_ENEMIGO_BASE) -> None:
        self.x = float(x)              # centro del circulo
        self.y = float(y)              # centro del circulo
        self.radius = ENEMIGO_RADIO
        self.speed = speed


def colision_circulo_rect(
    cx: float, cy: float, r: float,
    rx: float, ry: float, rw: float, rh: float,
) -> bool:
    """Colision circulo-rectangulo calculada algebraicamente (sin pygame.Rect)."""
    nearest_x = min(max(cx, rx), rx + rw)
    nearest_y = min(max(cy, ry), ry + rh)
    dx = cx - nearest_x
    dy = cy - nearest_y
    return dx * dx + dy * dy <= r * r
