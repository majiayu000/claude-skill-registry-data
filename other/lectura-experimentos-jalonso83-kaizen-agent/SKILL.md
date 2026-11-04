---
name: lectura-experimentos
description: Úsalo cuando venza la ventana de un experimento o campaña y toque emitir veredicto, o cuando alguien pida "cómo salió X". Complementa a diseno-experimentos (ese diseña antes; este lee después) y cierra el bucle escribiendo el aprendizaje al Cerebro.
---

# Lectura de experimentos: el veredicto se gana

El veredicto de un experimento se decide contra lo que se firmó ANTES de verlo correr. Si no hay umbral pre-registrado, no hay veredicto posible: hay observación.

## 0. Antes de empezar

1. `search_cerebro("<nombre del experimento>")` — recuperar hipótesis, umbral firmado, diseño (brazos, holdout, ancla de la métrica) y fecha de la ventana. **Leer el diseño ANTES de opinar sobre la validez del resultado.**
2. `get_campaign_results` (o `get_kpis` si la métrica es de producto) con conteos por brazo.
3. Al cerrar: `save_cerebro_note` con el aprendizaje. Sin excepción — un experimento leído que no se escribe no compone.

## 1. Las cinco reglas del veredicto

1. **Contra el umbral firmado, nunca contra la corazonada.** Si la condición era "≥18% sostenido dos semanas" y dio 17.24% y 23.40%, la condición NO se cumplió. Argumentar que "la semana 1 madura cruzaría" es correr la vara después de ver el resultado (error ya cometido y retractado en FinZen: no repetirlo).
2. **Brazo contra brazo concurrente, jamás contra la serie histórica.** La comparación no concurrente se contamina con el cambio de mezcla de tráfico.
3. **Piso de muestra antes de piso de emoción.** Una diferencia producida por 3 usuarios en el control (1.34% vs 1.97% con control n=152) es ruido aunque el panel imprima "el mensaje restó". Con n insuficiente el resultado se declara **direccional o no medible**, se dice cuánto n faltó, y no se recomienda revertir nada.
4. **Correlación con tendencia previa no es causa.** Si la métrica ya venía cayendo antes del experimento (la sobrevida D1→D7 caía desde tres cohortes antes), no se le atribuye la caída al experimento sin más evidencia.
5. **Confusores se declaran, no se descubren después.** Si durante la ventana entró otra intervención sobre la misma métrica (otra promo, otro slot, un deploy), el veredicto lo dice arriba, no en nota al pie.

## 2. Veredictos permitidos (elegir uno)

| Veredicto | Cuándo |
|---|---|
| Positivo / Negativo | Cruzó (o no) el umbral firmado, con n suficiente y sin confusor mayor |
| Positivo acotado | El mecanismo funciona pero la condición firmada no se cumplió completa; se documenta qué parte sí |
| No medible | Sin control, n insuficiente, o confusor dominante. Se dice qué haría falta para medirlo |
| Confirma, no decide | El dato ya estaba aritméticamente determinado por resultados previos; no aporta decisión nueva |

## 3. Cierre obligatorio (lo que hace que el sistema componga)

Al emitir veredicto, `save_cerebro_note` con: nombre, ventana, umbral firmado vs resultado (conteos), veredicto, confusores, y **la decisión que esto habilita o bloquea**. Si el veredicto contradice una nota previa del Cerebro, la nota nueva lo dice explícitamente ("supersede a X del [fecha]").

## 4. Ejemplo bueno (dato FinZen real)

La eval de H9 cerró como **positivo acotado**: la primaria firmada (≥18% dos semanas) no se cumplió (17.24% / 23.40%), el guardrail D7 quedó en 7.51% (32/426) contra banda 8-10% con IC95 [5.0, 10.0] cubriendo toda la banda — "lo único afirmable es que D7 no subió". Decisión derivada: queda en producción, no se escala sobre él, el foco pasa al tramo D1→D7. Ese es el nivel de matiz esperado.

## Anti-patrones

- Emitir veredicto sin haber leído el pre-registro (o inventar el umbral "razonable" a posteriori).
- Citar lifts de paneles con control vacío o brazos sin llenar.
- Cerrar la lectura sin escribir la nota al Cerebro.
- Reabrir un experimento cerrado negativo porque el resultado incomoda (buscar primero si ya está en decisiones cerradas).
- Prometer "se leerá cuando madure" sin fecha concreta de relectura.

## Formato de entrega

**Veredicto arriba, en una línea, con el nombre del experimento.** Después: umbral firmado vs resultado (conteos por brazo), confusores, qué se puede afirmar y qué no, decisión habilitada, y confirmación de que la nota quedó en el Cerebro. Máximo una pantalla.
