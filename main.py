"""
CAPA 6: Orquestador / Bucle Principal (`main`).

Coordina el flujo secuencial de cada frame:
  1. Capturar comandos      (LocalInputHandler)
  2. Procesar comandos      (GameState.process_command)
  3. Actualizar simulacion  (GameState.update)
  4. Extraer snapshot       (GameState.get_snapshot)
  5. Dibujar escena         (PygameRenderer.render)

Ejecutar:  python main.py
Controles: Jugador 1 = <-- / --> + ESPACIO | Jugador 2 = A / D + W | ESC = salir
"""

import pygame

from shooter.config import ALTO, ANCHO, FPS
from shooter.game_state import GameState
from shooter.input_handler import LocalInputHandler
from shooter.renderer import PygameRenderer


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Shooter 2D - Arquitectura Limpia")
    clock = pygame.time.Clock()

    # Capas del sistema
    state = GameState()
    input_handler = LocalInputHandler()
    renderer = PygameRenderer(screen)

    running = True
    while running:
        dt_ms = clock.tick(FPS)  # limita a 60 FPS y devuelve el delta en ms

        # 0) Eventos de sistema (cerrar ventana)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # 1) Capturar comandos (InputHandler)
        commands = input_handler.poll()

        # 2) Procesar comandos en el modelo (GameState)
        current_time = pygame.time.get_ticks()
        for player_id, lista in commands.items():
            for command in lista:
                state.process_command(player_id, command, current_time)

        # 3) Actualizar simulacion fisica (GameState.update)
        state.update(dt_ms)

        # 4) Extraer snapshot (GameState.get_snapshot)
        snapshot = state.get_snapshot()

        # 5) Dibujar escena (PygameRenderer.render)
        renderer.render(snapshot)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
