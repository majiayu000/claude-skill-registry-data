---
name: story-authoring
description: Use when writing or editing a story, variant, character sheet (identity, secret, knowledge, version), morning report or epilogue in Story1HijaPerfecta.cs, Story2NocheDeVerano.cs, Story3HumoYSilencio.cs or StoriesDatabase.json, or adding a character inspired by a real case.
---

# Escribir historias y fichas

Una ficha la lee un modelo 7B, no una persona. Lo que no está escrito se lo inventa, y lo que se contradice lo suelta tarde.

## Reglas

| Regla | Caso real que la motivó |
|---|---|
| Del caso real se toma el **patrón**, nunca el nombre. Se busca el nombre real en todos los textos que ven el jugador y el modelo, y un test lo vigila (`CaseDataValidationTests.LaVecinaYaNoSeLlamaComoLaPersonaReal`). La clave interna del arte puede quedarse. | La vecina se llamaba Rosario, como la madre condenada en el caso real. Pasó a Amparo y su `artId` siguió siendo `rosario`. |
| Todo familiar o persona que se pueda nombrar lleva nombre propio en la ficha. | Con "tu tía" el modelo inventó "tía María" (5 avisos en una partida). Con nombres (Remedios, Nerea, Hugo), 0. |
| Una ficha nunca pide a la vez contar X (en la pista) y ocultar X (en el secreto). El secreto oculta otra cosa. | A Álex se le pidió contar y ocultar el WhatsApp, y la ⚡ salía en los días 6-7. |
| El hecho de un testigo se escribe como algo que **le pareció raro**. | Andrés veía normal el bar a oscuras, y 2A salió en 3 de 10 partidas. |
| El hecho de una pista va en primera persona («Mamá me dejó…»). | 3B_noche pasó de 5/10 a 10/10. |
| Una ficha ocupa como mucho **565 palabras** (`MaxPromptWords`). | 460 → 540 → 565, cada vez con calibración completa. |
| Tras **cualquier** cambio de ficha, aunque sea un nombre, se recalibran las pistas de ese personaje (skill `calibration-run`). | Al poner nombre a la tía "Remedios", 3A_granada bajó a 3/6. |

## Antes de dar la edición por buena

1. `NarrativeValidator` en verde en las 9 variantes. Comprueba que la mentira la contradice una ⚡ de un inocente, que los partes no regalan pistas, que el epílogo no trae horas nuevas y que nadie está en dos sitios a la vez. En una auditoría encontró 17 incoherencias.
2. `CaseDataValidationTests` en verde: guarda de la ficha y de los partes, presupuesto de palabras y nombres reales.
3. Si un personaje es nuevo: lleva `portraitKey` propio (sin compartir retrato), `heightCm` y `artId`. Ver la skill `pixel-portrait-kitbash`.
4. Si se tocan pistas, ver la skill `clue-design`.
