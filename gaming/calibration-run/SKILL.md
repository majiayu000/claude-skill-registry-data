---
name: calibration-run
description: Use when measuring whether a change to clues, anchors, sheets, prompts or model parameters helped - running ClueCalibrator, PremiseCalibrator, EmotionCalibrator or BotPlayer, comparing before/after, or deciding if a drop is a regression or noise.
---

# Medir con el calibrador y el bot

Antes de medir, fija el umbral. Después, un solo cambio por brazo, la misma semilla y el mismo N.

## Comandos

Base: `"/c/Program Files/Unity/Hub/Editor/6000.3.2f1/Editor/Unity.exe" -batchmode -nographics -projectPath <worktree> -executeMethod <X> -logFile Logs/<x>.log`

| X | Opciones | Informe |
|---|---|---|
| `ClueCalibrator.RunFromCommandLine` | `-clues 2C_prueba` o `-variants 2C`, `-tries` (3 por defecto), `-temperature`, `-model`, `-noprecision` | `Logs/clue-calibration.md` |
| `PremiseCalibrator…` | `-tries 2` (72 respuestas) | `Logs/premise-calibration.md` |
| `EmotionCalibrator…` | `-tries 1` (144 respuestas) | `Logs/emotion-calibration.md` |
| `BotPlayer…` | `-variants`, `-games`, `-seed`, interruptores (`-noTimeRetry`, `-strictTimeNudge`, `-noLineupMarks`…) | `Logs/bot-playthroughs.md`, `Logs/bot/` |

## Reglas

| Regla | Caso real |
|---|---|
| Calibra en un worktree aparte (`git worktree add ../dng-calib HEAD`), nunca sobre la copia en la que editas. Al acabar: `git worktree remove --force` y `prune`. | Una edición a medias tumbó una calibración a 0.4 que hubo que tirar. |
| Antes de medir, copia el informe anterior (`cp Logs/clue-calibration.md Logs/clue-calibration-antes.md`): el calibrador lo sobrescribe. Logs/ no se versiona. | |
| Una pista: `-clues X -tries 10`, objetivo ≥7/10. Con 3 intentos, 80-85 % entre pasadas es ruido. | Un A/B dio 40/48 frente a 44/48 y las pistas que fallaban cambiaban de brazo. 2C_gps se confirmó con 17/20. |
| En el bot, ±2 sobre 18 partidas es ruido. | Culpable 11/18 → 9/18 resultó ruido. |
| Antes de fiarte del bot, comprueba que ve lo que ve un jugador (partes, marcas de la rueda) y revisa sus falsos positivos. | Sin leer los partes, 2B salía 0/20. Con las marcas de la rueda, 3/8. |
| Nunca redondees: da el rango de las sondas. | Premisas 5, 2 y 5 % se publicaron como "2 %" y hubo que corregirlo a "2-5 %". |
| Para el informe, mira la mediana y las pistas que bajaron, una por una. | |

**Umbrales de la Sesión A**: pistas ≥80 % (cada una ≥2/3), premisas ≤5 %, estados ≥95 %, bot ≥14/18.

Ollama tiene que estar arriba con `qwen2.5:7b-instruct`. Si no lo está, PremiseCalibrator falla en lugar de dar un informe vacío.
