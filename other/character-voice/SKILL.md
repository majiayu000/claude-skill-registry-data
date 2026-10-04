---
name: character-voice
description: Use when a suspect's answer sounds wrong in a game or log - fakes memory ("como ya le dije"), invents a time, relative or sighting, accepts a false premise, switches language or regional language, shows a malformed [ESTADO] tag, or has a wrong or monotone emotional state.
---

# Voz de los sospechosos

Primero se mira qué protección existe ya y por qué no actuó. Sin un test en rojo con la respuesta real no se toca la ficha ni el prompt.

## Qué existe y el caso que lo motivó

| Síntoma | Protección | Caso real |
|---|---|---|
| Finge memoria en el primer contacto | `ClaimsPriorTalk` + `FirstContactNudge` reintentan, y el bot marca `FalseMemory` (`AIConversationManager`) | 11 de 1342 primeras respuestas (0,8 %). Parecía que recordaba la partida anterior, pero no había fuga. Ver la skill `game-state-reset`. |
| Inventa una hora | `TimeCheck` + reintento más frío (0,3) | 27/619 → 7/630 (A/B de 18+18, semilla 59) |
| Repite lo anterior | `RepeatNudge` (+0,25 de temperatura) | |
| Cambia a chino o cirílico | `LanguageNudge` | En una partida de 3A, el historial lo arrastró 9 respuestas |
| Habla en gallego | `speechExample` siempre en castellano; el acento va en `speech` | Maruxa en gallego, ~1 de cada 60 respuestas |
| Acepta una premisa falsa | Regla "si no está en tu ficha, di que no te consta; lo que sí está, confírmalo" | "Niégalo" hacía negar amenazas reales a la madre (3A_audios). La regla actual deja el 2-5 %. |
| Está "nervioso" en todo | "Nervioso" solo por su tema propio; por la víctima, "triste" | 70-80 % nervioso → 42 % nervioso / 35 % triste, coherencia 95 % |
| `[MESTADO: x]` visible | El parser tolera el error y guarda la etiqueta canónica | Se copió 10 veces seguidas por el historial |
| Inventa un familiar o un avistamiento | Todo familiar con nombre y toda hora en la ficha, más "si no sabes la hora, di que no te fijaste" | La vecina "vio" a Elena a las 00:05, ya muerta |

## Cómo arreglarlo

1. Copia la respuesta real tal cual a un test con proveedor falso (estilo `AIConversationFlowTests`). Tiene que fallar.
2. Arregla el hueco concreto, por ejemplo que el reintento también falle o que otro reintento se adelante.
3. Mide el efecto con el bot en la misma semilla y el mismo N (ver la skill `calibration-run`). Un 7B no llega a 0: el objetivo es bajarlo con datos.
