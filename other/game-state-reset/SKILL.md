---
name: game-state-reset
description: Use when adding or changing state that lives across turns, days or games (fields in GameManager, InterrogationUI, AIConversationManager, statics, SaveData), or when someone reports that suspects or the game "remember" a previous game or lose progress after Continue.
---

# Estado entre partidas

Cada partida nueva empieza de cero, y **Continuar** conserva solo esa partida. Antes de añadir un campo, busca si ya existe: `currentSuspectId` / `SaveData.currentSuspect` ya guardan el sospechoso abierto.

## Al añadir o tocar estado, decide dónde vive

| Vive… | Va en… | Se limpia en… |
|---|---|---|
| Solo esta partida | El objeto de partida (`InvestigationState`, historiales) | `StartCase` / `ResetForNewCase` |
| Sobrevive a Continuar | `SaveData`, con su test pasando por Continuar | Se restaura en `RestoreCase` |
| Entre partidas (ajustes) | `GameSettings` | Nunca |
| `static` | Evítalo. Si hace falta, ponlo a cero en cada partida o tirada del bot. | |

## Test obligatorio, en rojo antes del cambio

En `StateMachineTests`, con proveedor falso (`FakeProvider.sent` guarda cada prompt):

1. Partida 1 con un marcador ("ZAFIRO") en una pregunta.
2. Comprueba que el marcador **no** aparece en el prompt de la partida 2 por ninguna de las cuatro entradas:
   - Jugar otra vez
   - Reiniciar desde Ajustes
   - Caso nuevo desde el menú (toca `ConfirmDialog.ConfirmName`)
   - La misma historia otra vez
3. Por **Continuar**, el marcador sí está y solo el de esa partida.

## Casos reales

- "Recuerdan la partida anterior": el código no tenía fuga. Era qwen diciendo "como ya le dije" (0,8 %). El bot reutiliza el gestor entre partidas y cuenta fugas descontando lo que la partida actual repite de la ficha (1 falso positivo). Ver la skill `character-voice`.
- Tras Continuar, `HintMemory` volvía al nivel 1 y cobraba otra vez. "Ayer: …" perdía el progreso de la mañana. La marca de caso forzado no se reiniciaba.
- Tocar una nota a mitad de pregunta guardaba dos mensajes de usuario seguidos. Nunca guardes con una petición en curso.
- `NoirPostFx` filtraba 2 VolumeProfiles en cada Reiniciar: destruye lo que se clona en ejecución y prueba a recargar la escena.
