---
name: batchmode-capture
description: Use when running Unity tests or taking screenshots/animation frames in batchmode, when checking that a UI change looks right, or when a test run or capture "passed" suspiciously fast or shows old content.
---

# Tests y capturas en batchmode

Un XML o un PNG viejo parece un éxito. Si la compilación falla, Unity aborta sin ejecutar nada y deja lo anterior.

## Scripts (Git Bash, desde la raíz, con el editor cerrado)

| Para | Comando | Resultado |
|---|---|---|
| EditMode completo | `.superpowers/run-tests.sh` | `Logs/editmode-results.xml` |
| PlayMode completo | `.superpowers/run-play.sh` | `Logs/playmode-results.xml` |
| Unos tests | `.superpowers/run-filter.sh EditMode "Clase1;Clase2"` | Borra el XML y avisa "SIN RESULTADOS" |
| Capturas | `.superpowers/capture-anim.sh "AnimationCapture.X\|AnimationCapture.Y" [1200]` | `docs/screenshots/<fecha>/anim/*.png` |

Las capturas van **sin `-nographics`** (necesitan GPU), y el script ya lo hace. No uses `ScreenshotTool` para validar una pantalla. Si no existe una captura de esa pantalla, añade un `[UnityTest]` a `AnimationCapture.cs`.

## Cada vez

1. `rm -f Logs/*.xml` antes de lanzar (solo `run-filter.sh` lo hace solo).
2. Si sale "Aborting batchmode" o "SIN RESULTADOS": `grep "error CS" Logs/*.log`.
3. Para UI, primero `run-filter.sh EditMode LayoutValidationTests`. Mide 1080×1920, 1080×2340 y 1536×2048, alto contraste y texto muy grande. Si añades una sección, métela en el peor caso del test (no veía notas ni partes).
4. Antes de mirar un PNG, comprueba su hora (`ls -la --time-style=+%H:%M:%S`). Míralo a tamaño real con Read, y para la versión de 2400 px usa `capture-anim.sh <filtro> 1200`.
5. Al acabar: `git checkout -- ProjectSettings/UnityConnectSettings.asset` (el editor lo activa solo) y `git status`. Revierte los archivos que la build o el editor dejen cambiados solo en los finales de línea.

## Casos reales

- Un heredoc rompió un `.cs`. La captura "pasó" leyendo un `capture-results.xml` viejo.
- Una hoja de revisión mostraba una miniatura vieja con el mismo nombre de archivo.
- Hay fallos que solo salen en capturas en juego: la lista desplegable se abría media pantalla fuera.
- En batchmode, la "pantalla" del editor es 640×480 en horizontal.
- La salida con `-nographics` se cuelga 1 de cada 4 a 12 veces. En bucles, usa `timeout 45`.
