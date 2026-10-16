"""
CAPA 5: Renderizador (PygameRenderer).

Recibe EXCLUSIVAMENTE el diccionario generado por `GameState.get_snapshot()`
y lo dibuja. No tiene referencia al modelo: la vista es de solo lectura (RN-05).
Colores: jugadores verdes, proyectiles amarillos, enemigos rojos.
"""

import pygame


class PygameRenderer:
    """Dibuja la escena a partir unicamente del snapshot."""

    COLOR_FONDO = (18, 18, 28)
    COLOR_JUGADOR = (40, 200, 80)      # verde
    COLOR_PROYECTIL = (240, 220, 40)   # amarillo
    COLOR_ENEMIGO = (220, 60, 60)      # rojo
    COLOR_TEXTO = (235, 235, 235)

    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface
        pygame.font.init()
        self.font = pygame.font.SysFont("consolas", 20)
        self.big_font = pygame.font.SysFont("consolas", 48, bold=True)

    def render(self, snapshot: dict) -> None:
        self.surface.fill(self.COLOR_FONDO)

        # Enemigos: circulos rojos
        for enemy in snapshot["enemies"]:
            pygame.draw.circle(
                self.surface, self.COLOR_ENEMIGO,
                (int(enemy["x"]), int(enemy["y"])), int(enemy["radius"]),
            )

        # Proyectiles: rectangulos amarillos
        for bullet in snapshot["bullets"]:
            pygame.draw.rect(
                self.surface, self.COLOR_PROYECTIL,
                pygame.Rect(int(bullet["x"]), int(bullet["y"]),
                            int(bullet["width"]), int(bullet["height"])),
            )

        # Jugadores: rectangulos verdes
        for player in snapshot["players"]:
            if not player["alive"]:
                continue
            pygame.draw.rect(
                self.surface, self.COLOR_JUGADOR,
                pygame.Rect(int(player["x"]), int(player["y"]),
                            int(player["width"]), int(player["height"])),
            )

        # HUD: puntaje en la esquina superior izquierda
        hud = self.font.render(f"PUNTAJE: {snapshot['score']}", True, self.COLOR_TEXTO)
        self.surface.blit(hud, (10, 8))

        vidas = "  ".join(
            f"P{p['id']}: {max(p['lives'], 0)}" for p in snapshot["players"]
        )
        vidas_surf = self.font.render(f"VIDAS  {vidas}", True, self.COLOR_TEXTO)
        self.surface.blit(vidas_surf, (10, 32))

        if snapshot["game_over"]:
            texto = self.big_font.render("GAME OVER", True, self.COLOR_ENEMIGO)
            self.surface.blit(
                texto,
                (snapshot["width"] // 2 - texto.get_width() // 2,
                 snapshot["height"] // 2 - texto.get_height() // 2),
            )
