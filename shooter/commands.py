"""
CAPA 1: Dominio y Comandos.

Acciones abstractas que un jugador puede solicitar al modelo.
El modelo no conoce teclas: solo conoce estos comandos, lo que permite
sustituir el teclado local por red (cliente/servidor) sin tocar el dominio.
"""

from enum import Enum


class Command(Enum):
    """Acciones abstractas que un jugador puede solicitar al modelo."""

    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"
    SHOOT = "shoot"
