"""
Paquete del juego Shooter 2D - Escenario B: Arquitectura Limpia (MVC).

Estructura modular (una capa por modulo):

    shooter/
        config.py         -> Constantes de juego (sin pygame: seguro para el dominio)
        commands.py       -> Capa 1: Comandos abstractos (Enum Command)
        entities.py       -> Capa 2: Modelo del dominio (Player, Bullet, Enemy)
        game_state.py     -> Capa 3: Estado central (GameState)
        input_handler.py  -> Capa 4: Captura de entradas (LocalInputHandler)
        renderer.py       -> Capa 5: Renderizador (PygameRenderer)
    main.py               -> Capa 6: Orquestador / bucle principal

Las capas 1-3 son Python puro y NO importan pygame, de modo que la logica
puede migrarse a un servidor autoritativo sin tocar la vista.
"""

from .commands import Command
from .game_state import GameState

__all__ = ["Command", "GameState"]
