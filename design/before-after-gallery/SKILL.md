---
name: before-after-gallery
description: Use when showing a visual change to Cristian - before/after comparisons, galleries or contact sheets of screens, portraits or animations, or any image meant to prove that a UI or art change looks right.
---

# Galerías antes/después

Una comparación solo vale si lo único que cambia entre las dos columnas es el cambio que se enseña.

## Reglas

| Regla | Caso real |
|---|---|
| En las dos columnas, **la misma pantalla, la misma historia (Caso 1, no "al azar") y el mismo instante** (mismos segundos tras la misma acción). | Galería del bloque 4 de la Sesión A. |
| "Antes" = la misma build con el ajuste nuevo del tema **apagado** (`Theme.<ajuste> = false` mediante `ThemeManager.Override` antes de cargar la escena). Así se demuestra también que se puede desactivar. Sin ajuste, saca el "antes" de un worktree del commit anterior, nunca de una captura vieja de otra herramienta. | `AnimationCapture.AntesDespues` |
| Di cualquier diferencia residual con el original de verdad. | "La pared marca 110-200 en vez de 130-190." |
| Retratos a **tamaño de juego** (recorte de la captura de 540×960, ×2 sin suavizar) e historia por historia: los ids se repiten entre historias. | La primera galería de retratos mezclaba historias. |
| Cada hoja de revisión lleva un **nombre nuevo**. Mira a tamaño real y mide (brillo y posición por fotograma) en vez de fiarte de la miniatura. | Una miniatura vieja con el mismo nombre enseñaba algo que ya no era así. La entrada se midió: termina a los 0,6 s. |
| Al repositorio solo va el JPEG de la galería (`docs/screenshots/<fecha>/galeria/`). Los PNG en bruto (`anim/`) no se versionan: se regeneran. | En `ff30092` se subieron ~300 MB de capturas en bruto por error. |

## Cómo

1. Añade una captura (por ejemplo `AntesDespues`) en `Assets/Tests/PlayMode/AnimationCapture.cs` con un bucle `foreach (bool after in {false, true})`: tema → escena → mismas acciones → `Shot($"ad_{tag}_...")`.
2. `.superpowers/capture-anim.sh "AnimationCapture.AntesDespues"`. Ver la skill `batchmode-capture`.
3. Monta la galería con un script en `Tools/make_gallery_<sesión>.py`: columnas ANTES y AHORA y una línea de texto por fila.
4. Enlázala en el informe (ver la skill `session-report`).
