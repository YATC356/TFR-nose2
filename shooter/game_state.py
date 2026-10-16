"""
CAPA 3: Estado Central (Python puro).

`GameState` es la unica fuente de verdad del juego: toda modificacion de
vida, puntaje, creacion o eliminacion de entidades reside aqui y la vista
es de solo lectura (RN-05). No importa pygame.
"""

import random
from typing import Dict, List

from .commands import Command
from .config import (
    ALTO,
    ANCHO,
    ENEMIGO_RADIO,
    NAVE_ANCHO,
    PUNTOS_POR_IMPACTO,
    PROYECTIL_ALTO,
    PROYECTIL_ANCHO,
    SPAWN_MS,
    VEL_ENEMIGO_BASE,
)
from .entities import Bullet, Enemy, Player, colision_circulo_rect


class GameState:
    """Modelo central: jugadores, proyectiles, enemigos, puntaje y mapa 800x600."""

    def __init__(self, semilla: int | None = None) -> None:
        self.width = ANCHO
        self.height = ALTO
        self.players: Dict[int, Player] = {
            1: Player(1, x=ANCHO * 0.25 - NAVE_ANCHO / 2, y=ALTO - 70),
            2: Player(2, x=ANCHO * 0.75 - NAVE_ANCHO / 2, y=ALTO - 70),
        }
        self.bullets: List[Bullet] = []
        self.enemies: List[Enemy] = []
        self.score = 0
        self.game_over = False
        self._spawn_timer = 0.0                 # acumulador del temporizador
        self._rng = random.Random(semilla)      # rng inyectable (futuro servidor)

    # -- Comandos ------------------------------------------------------------
    def process_command(self, player_id: int, command: Command, current_time: float) -> None:
        """Ejecuta una accion pedida por un jugador en `current_time` (ms)."""
        player = self.players.get(player_id)
        if player is None or self.game_over:
            return

        if command is Command.MOVE_LEFT:
            player.intent = -1
        elif command is Command.MOVE_RIGHT:
            player.intent = 1
        elif command is Command.SHOOT:
            self._shoot(player, current_time)

    def _shoot(self, player: Player, current_time: float) -> None:
        """RN-01: solo dispara si han pasado >= 200 ms desde el ultimo disparo."""
        if not player.alive:
            return
        if current_time - player.last_shot_time < player.reload_time:
            return
        player.last_shot_time = current_time
        self.bullets.append(
            Bullet(
                x=player.x + player.width / 2 - PROYECTIL_ANCHO / 2,
                y=player.y - PROYECTIL_ALTO,
            )
        )

    # -- Simulacion ----------------------------------------------------------
    def update(self, dt_ms: float) -> None:
        """Avanza la simulacion un tick (`dt_ms` en milisegundos)."""
        if self.game_over:
            return
        dt_ms = min(dt_ms, 100.0)  # evita "teletransportes" tras una pausa
        dt = dt_ms / 1000.0

        # 1) Movimiento de naves + RN-03 (limites horizontales estrictos)
        for player in self.players.values():
            if player.alive:
                player.x += player.intent * player.speed * dt
                player.x = max(0.0, min(player.x, float(self.width - player.width)))
            player.intent = 0  # el input debe reafirmarse cada frame

        # 2) Movimiento de proyectiles y enemigos
        for bullet in self.bullets:
            bullet.y -= bullet.speed * dt
        for enemy in self.enemies:
            enemy.y += enemy.speed * dt

        # 3) Generacion de enemigos por temporizador
        self._spawn_timer += dt_ms
        while self._spawn_timer >= SPAWN_MS:
            self._spawn_timer -= SPAWN_MS
            self._spawn_enemy()

        # 4) Colision proyectil <-> enemigo (RN-02)
        self._resolve_bullet_enemy_collisions()

        # 5) Colision nave <-> enemigo (vida: unica instancia en GameState, RN-05)
        self._resolve_player_enemy_collisions()

        # 6) RN-04: recolector de basura / purga de entidades fuera del mapa
        self.bullets = [b for b in self.bullets if not b.y < 0]
        self.enemies = [e for e in self.enemies if not e.y > self.height]

        # 7) Condicion de fin de partida
        if not any(p.alive for p in self.players.values()):
            self.game_over = True

    def _resolve_bullet_enemy_collisions(self) -> None:
        """RN-02: el impacto destruye ambas entidades y otorga +10 puntos."""
        impacted_bullets: set[int] = set()
        impacted_enemies: set[int] = set()
        for bi, bullet in enumerate(self.bullets):
            if bi in impacted_bullets:
                continue
            for ei, enemy in enumerate(self.enemies):
                if ei in impacted_enemies:
                    continue
                if colision_circulo_rect(
                    enemy.x, enemy.y, enemy.radius,
                    bullet.x, bullet.y, bullet.width, bullet.height,
                ):
                    impacted_bullets.add(bi)
                    impacted_enemies.add(ei)
                    self.score += PUNTOS_POR_IMPACTO
        if impacted_bullets:
            self.bullets = [b for i, b in enumerate(self.bullets) if i not in impacted_bullets]
        if impacted_enemies:
            self.enemies = [e for i, e in enumerate(self.enemies) if i not in impacted_enemies]

    def _resolve_player_enemy_collisions(self) -> None:
        """El contacto nave-enemigo resta una vida y destruye el enemigo."""
        for player in self.players.values():
            if not player.alive:
                continue
            survivors = []
            for enemy in self.enemies:
                hit = colision_circulo_rect(
                    enemy.x, enemy.y, enemy.radius,
                    player.x, player.y, player.width, player.height,
                )
                if hit:
                    player.lives -= 1
                else:
                    survivors.append(enemy)
            self.enemies = survivors

    def _spawn_enemy(self) -> None:
        margin = ENEMIGO_RADIO + 5
        x = self._rng.uniform(margin, self.width - margin)
        speed = VEL_ENEMIGO_BASE + self._rng.uniform(-20.0, 60.0)
        self.enemies.append(Enemy(x=x, y=-ENEMIGO_RADIO, speed=speed))

    # -- Lectura (snapshot DTO / JSON-like) ----------------------------------
    def get_snapshot(self) -> dict:
        """Foto del estado con tipos nativos (int, float, list, dict)."""
        return {
            "width": int(self.width),
            "height": int(self.height),
            "score": int(self.score),
            "game_over": bool(self.game_over),
            "players": [
                {
                    "id": int(p.id),
                    "x": float(p.x),
                    "y": float(p.y),
                    "width": int(p.width),
                    "height": int(p.height),
                    "lives": int(p.lives),
                    "alive": bool(p.alive),
                }
                for p in self.players.values()
            ],
            "bullets": [
                {"x": float(b.x), "y": float(b.y),
                 "width": int(b.width), "height": int(b.height)}
                for b in self.bullets
            ],
            "enemies": [
                {"x": float(e.x), "y": float(e.y), "radius": int(e.radius)}
                for e in self.enemies
            ],
        }
