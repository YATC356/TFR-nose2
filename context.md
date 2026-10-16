# Documento de Especificación Técnica: Juego Shooter 2D (Escenario B - Arquitectura Limpia)

> **Instrucciones para OpenCode:** Actúa como un Arquitecto de Software y Desarrollador Senior de Python. Tu tarea es mantener y evolucionar la implementación de un juego de disparos 2D en `pygame` (o `pygame-ce`) siguiendo estrictamente la especificación de arquitectura y reglas de negocio descritas a continuación.

---

## 1. Objetivo del Proyecto

Construir una aplicación de juego 2D en Python utilizando únicamente figuras geométricas primitivas (rectángulos y círculos) en modo *Standalone*, implementando una **Arquitectura Desacoplada (Model-View-Controller / Arquitectura Limpia)** organizada en **un módulo por capa arquitectónica**.

El código debe estar estructurado de tal manera que la lógica del juego pueda migrarse a un servidor autoritativo de red en el futuro sin modificar la capa del modelo ni la capa de renderizado.

---

## 2. Reglas de Negocio (Business Rules)

1. **RN-01 (Cadencia de Disparo):** Cada jugador tiene una cadencia máxima de disparo. No se puede emitir un proyectil si han transcurrido menos de 200 ms desde el disparo anterior.
2. **RN-02 (Asignación de Puntos):** Cada impacto de proyectil contra un enemigo destruye ambas entidades y otorga +10 puntos al puntaje global.
3. **RN-03 (Límites Espaciales):** La posición horizontal `x` de la nave debe restringirse estrictamente dentro del rango `0 .. ANCHO - ancho_nave`.
4. **RN-04 (Recolector de Basura / Purga):** Toda entidad de proyectil con `y < 0` y enemigo con `y > ALTO` debe eliminarse del estado para prevenir fugas de memoria.
5. **RN-05 (Soberanía del Estado):** Toda modificación de vida, puntaje, creación o eliminación de entidades reside únicamente dentro del modelo `GameState`. La vista es de solo lectura.

---

## 3. Estructura del Proyecto (Modular)

El código está dividido en una capa por módulo. Las capas 1-3 son **Python puro y no importan `pygame`** (verificable por análisis del código fuente); solo las capas 4-6 dependen de la librería de presentación.

```
TFR-nose2/
├── context.md                  # Este documento de especificación
├── main.py                     # Capa 6: orquestador / bucle principal
└── shooter/                    # Paquete del juego
    ├── __init__.py             # Documenta la estructura y expone Command, GameState
    ├── config.py               # Constantes compartidas (sin pygame)
    ├── commands.py             # Capa 1: comandos abstractos
    ├── entities.py             # Capa 2: modelo del dominio
    ├── game_state.py           # Capa 3: estado central
    ├── input_handler.py        # Capa 4: captura de entradas
    └── renderer.py             # Capa 5: renderizador
```

---

## 4. Especificación de Arquitectura y Componentes

### Capa 1: Dominio y Comandos — `shooter/commands.py`

* Define un `Enum` llamado `Command` con las acciones abstractas: `MOVE_LEFT`, `MOVE_RIGHT`, `SHOOT`.
* El modelo no conoce teclas: solo conoce estos comandos, lo que permite sustituir el teclado local por red sin tocar el dominio.

### Capa 2: Modelo del Dominio (Puro Python) — `shooter/entities.py`

* **`Player`**: Representa la nave. Mantiene coordenadas `(x, y)`, dimensiones, velocidad, tiempo del último disparo, tiempo de recarga 200 ms, vidas e intención de movimiento.
* **`Bullet`**: Representa el proyectil vertical. Contiene coordenadas `(x, y)`, dimensiones y velocidad.
* **`Enemy`**: Representa un obstáculo circular. Contiene coordenadas `(x, y)` (centro), radio y velocidad.
* **`colision_circulo_rect(...)`**: función pura que resuelve colisiones circulo-rectángulo algebraicamente.
* **RESTRICCIÓN CRÍTICA:** Ninguna de estas clases puede importar o instanciar objetos de `pygame` (como `pygame.Rect` o `pygame.Surface`). Las colisiones deben calcularse algebraicamente.

### Constantes — `shooter/config.py`

* Único módulo de constantes compartido por todas las capas (dimensiones, velocidades, cadencia, colores de regla de negocio).
* **RESTRICCIÓN:** no importa `pygame`, para que el dominio pueda usarlo sin arrastrar la dependencia de renderizado.

### Capa 3: Estado Central (`GameState`) — `shooter/game_state.py`

* Mantiene el diccionario de jugadores, lista de proyectiles, lista de enemigos, puntaje total y dimensiones del mapa 800x600.
* **`process_command(player_id, command, current_time)`**: Ejecuta las acciones indicadas por las abstracciones de comandos.
* **`update(dt_ms)`**: Avanza la simulación lógica en un tick, genera enemigos con un temporizador, resuelve colisiones y aplica las reglas de negocio.
* **`get_snapshot()`**: Devuelve una representación en diccionario plano (Data Transfer Object / JSON-like) con tipos nativos (`int`, `float`, `list`, `dict`) conteniendo la foto del estado actual.
* El generador aleatorio es inyectable (`random.Random(semilla)`) para la futura migración a servidor autoritativo determinista.

### Capa 4: Captura de Entradas (`LocalInputHandler`) — `shooter/input_handler.py`

* Lee eventos de teclado mediante `pygame.key.get_pressed()`.
* Mapea teclas locales a una lista de enum `Command` (ejemplo: `K_LEFT` → `Command.MOVE_LEFT`).
* Mapeo actual: Jugador 1 = `←` / `→` / `ESPACIO`; Jugador 2 = `A` / `D` / `W`.

### Capa 5: Renderizador (`PygameRenderer`) — `shooter/renderer.py`

* Recibe exclusivamente el diccionario generado por `get_snapshot()`.
* Limpia la pantalla y dibuja:
  * Jugadores como **rectángulos verdes**.
  * Proyectiles como **rectángulos amarillos**.
  * Enemigos como **círculos rojos**.
  * Puntaje en la esquina superior izquierda usando `pygame.font`.

### Capa 6: Orquestador / Bucle Principal (`main`) — `main.py`

* Configura la ventana a 800 x 600 px a 60 FPS.
* Coordina el flujo secuencial en cada frame:
  1. Capturar comandos (`LocalInputHandler`).
  2. Procesar comandos en el modelo (`GameState.process_command`).
  3. Actualizar simulación física (`GameState.update(dt_ms)`).
  4. Extraer snapshot (`GameState.get_snapshot()`).
  5. Dibujar escena (`PygameRenderer.render(snapshot)`).

---

## 5. Requisitos de Entrega para OpenCode

1. Entrega el código siguiendo principios SOLID y clean code, respetando la estructura de un módulo por capa descrita en la sección 3.
2. Asegúrate de que el archivo funcione tanto con `pygame` tradicional como con `pygame-ce`.
3. Incluye comentarios breves identificando cada capa arquitectónica para su presentación y análisis.
4. Al modificar una capa, no introducir dependencias de `pygame` en las capas 1-3 (dominio) ni referencias al modelo en la capa 5 (vista).
5. Mantener vigentes todas las reglas de negocio RN-01 .. RN-05.

---

## 6. Ejecución y Verificación

* **Ejecutar:** `python main.py`
* **Controles:** Jugador 1 = `←` / `→` + `ESPACIO` · Jugador 2 = `A` / `D` + `W` · `ESC` = salir.
* **Verificación esperada:**
  * RN-01: un segundo disparo dentro de los 200 ms es ignorado.
  * RN-02: cada impacto reduce ambas listas a 0 para esas entidades y suma +10.
  * RN-03: la nave nunca sale del rango horizontal del mapa.
  * RN-04: no quedan proyectiles con `y < 0` ni enemigos con `y > ALTO` tras un tick.
  * RN-05: `get_snapshot()` devuelve solo tipos nativos y el renderer no modifica el estado.
