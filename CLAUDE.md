# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Proyecto

Tetris en JavaScript vanilla con HTML5 Canvas y CSS. Sin dependencias, sin bundler, sin transpilador, sin `package.json`. Tres archivos: `index.html`, `style.css`, `game.js`.

## Ejecutar

No hay build ni tests. Para desarrollo se recomienda un servidor estático (los `<canvas>` funcionan igual abriendo el archivo, pero un servidor evita problemas de rutas/CORS):

```bash
python3 -m http.server 8000   # o: npx serve .
```

Luego abrir `http://localhost:8000`.

## Arquitectura (`game.js`)

Toda la lógica vive en `game.js` (~300 líneas) con estado global en variables de módulo (`board`, `current`, `next`, `score`, etc.). Puntos clave para trabajar con seguridad:

- **Tablero**: matriz `ROWS × COLS`; cada celda es `0` (vacía) o un índice `1–7` que indexa tanto `COLORS` como `PIECES`. Estos tres arrays están alineados por índice y empiezan con un elemento `null` en la posición 0 — mantener esa alineación al añadir/quitar piezas.
- **Piezas**: matrices; la rotación (`rotateCW`) es transposición + reverso de filas. `tryRotate` aplica wall kicks probando desplazamientos `[0, -1, 1, -2, 2]`.
- **Game loop** (`loop`): basado en `requestAnimationFrame`, acumula `dt` y baja la pieza al superar `dropInterval`. La pausa cancela el frame; reanudar reinicia `lastTime` antes de volver a llamar a `loop`.
- **Flujo de piezas**: `spawn()` mueve `next` a `current` y genera la siguiente; si la nueva pieza ya colisiona, dispara `endGame()`.
- **Nivel/velocidad**: nivel sube cada 10 líneas; `dropInterval = max(100, 1000 - (level-1)*90)` ms.

## Sincronización HTML ↔ JS

Las dimensiones del canvas del tablero están fijadas en `index.html` (`width="300" height="600"`) y deben coincidir con `COLS × BLOCK` y `ROWS × BLOCK` de `game.js`. Al cambiar `COLS`, `ROWS` o `BLOCK`, actualizar también el `<canvas id="board">`. `game.js` obtiene los elementos del DOM por `id`, así que renombrar un `id` en el HTML requiere actualizar la referencia correspondiente.
