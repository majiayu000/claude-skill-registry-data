---
name: clue-design
description: Use when a clue is detected too rarely or too often, when adding or editing a clue (holder, topic, fact, anchors, calibration questions, sampleHits/sampleMisses), or when ClueDetector misses or false-fires on a suspect's answer.
---

# Diseñar y arreglar pistas

Una pista sale si el modelo la dice **y** el detector la reconoce. Cuando una pista baja, primero se averigua cuál de los dos falla.

## 1. Diagnosticar antes de tocar nada

- Abre las respuestas reales en `Logs/clue-calibration.md` (o en `Logs/sesionA-bloque2/`) y clasifica cada fallo:
  - **El detector no lo vio:** el modelo dio la pista, pero con otra forma. Solución: anclas.
  - **El modelo no la dio:** solución en la ficha (ver la skill `story-authoring`).
- Ejemplo de cada tipo: 1C_pantalla, 2C_prueba y 1A_frasco bajaron al 17 % y 11 % por la redacción, y era el detector. 1B_cena (33 %) es el modelo: Daniel se inventa otra coartada.
- Antes de llamarlo regresión, confírmalo con `-clues X -tries 10` (objetivo ≥7/10). Con 3 intentos, una diferencia de 80-85 % es ruido. Ver la skill `calibration-run`.

## 2. Reglas de datos

| Regla | Caso real |
|---|---|
| Anclas en todas las formas del verbo: despedir, despid-, despedida, adiós. Cada respuesta real que se detecte se guarda en `sampleHits`. | "despedir" no cazaba "despidiéndose", y la ⚡ de 3C se perdió en 6 partidas o más. |
| Cada pista lleva ≥2 grupos de anclas, ≥2 preguntas de calibración, ≥2 `sampleHits` y ≥1 `sampleMisses` (una coartada falsa real va como `sampleMiss`). | Mínimos de `CaseDataValidationTests`. |
| Las anclas nunca aparecen en la ficha del portador (test `LaFichaDelPortadorNoDisparaSusPropiasPistas`) ni en los partes (`UnParteDeLaMananaNoRegalaPistas`). | La guarda cazó "nerea"/"hugo" en el secreto de Álex y "con llave" en el parte del día 6 de 1A. |
| El portador sabe que tiene el dato, y la pista lleva el vínculo (¿de quién es el coche?). | Ruiz no sabía que tenía los fichajes y salió 1/28. "Coche rojo" no apuntaba a nadie hasta "como el de Lucía". |
| Si cambia el tema, cambia la pregunta de calibración por una que haría un jugador. | 3C_bar seguía con la pregunta de cuando era secreta. Con la nueva, 67 %. |
| Las raíces de desbloqueo no se solapan con las preguntas de ejemplo (`NaturalUnlocksTests`). | El hermano de la historia 3 se desbloqueaba el día 1 en 8 de 12 partidas. |

## 3. Criterio de aprobado

Cada pista ≥2/3 (`hits*3 >= total*2`) y media ≥80 % en las 48. Al terminar, actualiza `docs/CLUE-LOGIC.md`: la fila de la pista y la medida de después.
