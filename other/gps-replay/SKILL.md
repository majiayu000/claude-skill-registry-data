---
name: gps-replay
description: Reproducir una ruta GPX/KML real de Mallorca en el emulador (adb emu geo fix) con su cadencia o a velocidad fija, para probar navegación y notas; no instala la app (android-install-and-logcat).
argument-hint: "[archivo.gpx|archivo.kml] [--velocidad x2|--kmh 60]"
allowed-tools: Read, Glob, Bash(node scripts/gps-replay.mjs*), Bash(adb *), Bash(emulator *)
---

# gps-replay

Simula el movimiento del coche en el emulador enviando posiciones de una traza con `node scripts/gps-replay.mjs`. Archivo: `$0`; opciones: el resto de `$ARGUMENTS`.

## Cuándo usarla
- Probar en emulador la posición, velocidad, navegación giro a giro, lectura de notas, alertas o cronometraje sobre una carretera real.
- Escenarios de `qa-scenario` que necesitan movimiento (`screen-off`, `background`, `gps-loss`, `doze`).

## Cuándo NO usarla
- Instalar o arrancar la app, leer logcat o capturar pantalla → usa `android-install-and-logcat`.
- Tests automáticos de geometría o notas → usa `test-write` (tipo `motor`) con fixtures; no dependen del emulador.
- En dispositivo físico: `adb emu` solo funciona con el emulador; en el teléfono hace falta una app de ubicación simulada (pedirlo al usuario).

## Precondiciones
- Emulador arrancado (`adb devices` muestra `emulator-5554` en estado `device`; si no, `emulator -avd trombito-36 -no-snapshot-save &`). La app instalada con permiso de ubicación concedido.
- Traza en `docs/rutas/` (rutas reales de Mallorca, con su atribución OSM en el propio archivo o en `docs/rutas/README.md`). Formatos: GPX (`trkpt`/`rtept` con `ele` y `time` opcionales) o KML (`LineString`/`gx:Track`).
- Node ≥ 22. El script no necesita dependencias.

## Pasos
1. Elegir la traza (`Glob docs/rutas/*`) y el modo:
   - Por defecto: respeta los `time` del GPX (cadencia real).
   - `--velocidad x2` (o `x0.5`): acelera o frena respecto a los tiempos originales.
   - `--kmh 60`: ignora los tiempos y recorre la traza a velocidad constante, interpolando puntos cada ~1 s (obligatorio si la traza no tiene `time`).
   - `--serial emulator-5556`: si hay varios emuladores.
2. Ejecutar en segundo plano para poder interactuar mientras tanto: `node scripts/gps-replay.mjs docs/rutas/<archivo> [opciones]`. El script envía `adb emu geo fix <lon> <lat> <alt>` (ojo: longitud primero) y muestra progreso (punto, distancia, velocidad).
3. Verificar que el emulador recibe la posición: `adb shell dumpsys location | grep -i "last location"` (o la pantalla de la app con velocidad actual).
4. Para simular un túnel (escenario `gps-loss`): parar el script (Ctrl+C) y relanzarlo con `--desde <índice|km>` más adelante.
5. Al terminar, el script deja la última posición fijada; no hace falta restaurar nada.

## Validaciones / tests
- `adb shell dumpsys location` muestra una posición dentro de Mallorca (lat ≈ 39.2–40.0, lon ≈ 2.3–3.5) que cambia durante la reproducción.
- La velocidad mostrada por la app es coherente con la de la traza o con `--kmh`.

## Definition of Done
- [ ] Traza reproducida completa (o el tramo pedido) sin errores del script.
- [ ] Posición verificada en el emulador.
- [ ] Rutas nuevas añadidas a `docs/rutas/` con su origen y atribución.

## Docs a actualizar
- `docs/rutas/README.md` si se añade una traza · docs/ESTADO.md (skill `session-handoff`) con lo probado
