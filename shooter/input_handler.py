"""
CAPA 4: Captura de Entradas (LocalInputHandler).

Traduce el teclado local a comandos abstractos. Es la unica capa que
conoce las teclas; el modelo solo recibe enum Command.
"""

from typing import Dict, List

import pygame

from .commands import Command


class LocalInputHandler:
    """Lee eventos de teclado y los mapea a una lista de enum Command por jugador."""

    MAPEO: Dict[int, Dict[int, Command]] = {
        # jugador_id: {tecla pygame -> comando}
        1: {
            pygame.K_LEFT: Command.MOVE_LEFT,
            pygame.K_RIGHT: Command.MOVE_RIGHT,
            pygame.K_SPACE: Command.SHOOT,
        },
        2: {
            pygame.K_a: Command.MOVE_LEFT,
            pygame.K_d: Command.MOVE_RIGHT,
            pygame.K_w: Command.SHOOT,
        },
    }

    def poll(self) -> Dict[int, List[Command]]:
        """Devuelve los comandos activos de cada jugador en este frame."""
        keys = pygame.key.get_pressed()
        commands: Dict[int, List[Command]] = {}
        for player_id, mapa in self.MAPEO.items():
            activos = [cmd for key, cmd in mapa.items() if keys[key]]
            if activos:
                commands[player_id] = activos
        return commands
