---
name: top-flop-hipotesis
description: Úsalo al leer resultados de mensajes, piezas o campañas (get_campaign_results, get_message_type_performance) para decidir qué se repite, qué se pausa y qué se prueba después. Produce el insumo de propose_campaign y de los borradores de contenido.
---

# Top/flop con hipótesis: leer para decidir el siguiente envío

Una tabla de resultados no decide nada. Lo que decide es la pareja top/flop con una hipótesis falsable de POR QUÉ, convertida en la variación del siguiente ciclo.

## 0. Antes de empezar

1. `get_message_type_performance` o `get_campaign_results` de la ventana + las 4 previas.
2. `search_cerebro("pausado")` y `search_cerebro("decisiones de contenido")` — no reproponer lo que ya se pausó ni relitigar lo cerrado.
3. El output alimenta `propose_campaign` / `save_content_draft`, pero este skill NO los llama: primero la lectura, después la propuesta.

## 1. Normalizar antes de rankear

- Rankear por **tasa sobre el denominador correcto** (por entregado, por alcanzado, por expuesto), nunca por absolutos: la pieza más enviada siempre "gana" en absolutos.
- Si dos brazos o piezas tienen denominadores de tamaños muy distintos, decir el n de cada uno junto a la tasa.
- Muestra chica se declara: con pocas piezas o segmentos pequeños la lectura es **direccional** y se etiqueta así.

## 2. Top Y flop, ambos obligatorios, cada uno con hipótesis

Formato de la hipótesis: **elemento concreto → mecanismo → acción falsable.**

| Componente | Pregunta que responde |
|---|---|
| Elemento | ¿Qué parte del mensaje explica el resultado? (hook, ángulo, formato, timing, segmento) |
| Mecanismo | ¿Por qué ese elemento produjo ese comportamiento en ESE segmento? |
| Acción falsable | ¿Qué repetimos/pausamos y qué número, en qué ventana, nos diría que la hipótesis era falsa? |

Sin hipótesis, el top es suerte y el flop es mala suerte: no se aprende nada accionable.

## 3. Reglas de decisión

| Situación | Acción |
|---|---|
| Ganador claro (supera al resto en su métrica normalizada) | Doblar con UNA variación por ciclo (cambiar todo a la vez rompe la atribución) |
| Perdedor consistente 2-3 ciclos seguidos | Pausar con criterio escrito de reactivación. Un solo mal resultado NO pausa |
| Formato entero en cero sostenido | Pausar el formato con fecha de decisión estructural, no pieza por pieza |
| Resultado bueno en métrica de pulso pero cero en métrica de decisión | No doblar: retiene atención pero no mueve el funnel. Ajustar el CTA antes de repetir |
| Costo por resultado fuera de rango vs pares (>5-10x) | Auditar el creativo/segmento antes de invertir un peso más |

## 4. Ejemplo bueno y malo (datos FinZen reales)

- **Bueno:** el reel "Muchos crecimos sin educación financiera" hizo 3.38% de moneda social con 15 shares (récord del mes). Hipótesis: hook de identidad colectiva ("crecimos sin...") en pilar educación → convierte en shares porque comparte identidad, no solo información. Acción: 2 piezas del mismo patrón con CTA explícito; falsable si ninguna supera 1% en 2 semanas.
- **Bueno:** tercera foto estática consecutiva con cero acciones y cero seguidores → se pausó el formato completo con criterio: si en 2 semanas los videos nativos siguen sumando y las fotos no, la decisión pasa a ser estructural.
- **Malo:** una campaña con costo por registro de $2.41 cuando sus pares de la misma plataforma rondaban $0.06-0.32 (hasta 40x) siguió corriendo sin auditoría del creativo. Ese caso se detecta en este paso, no en el cierre mensual.

## Anti-patrones

- Rankear por absolutos o mezclar denominadores.
- Reportar solo el top (el flop es la mitad del aprendizaje).
- Pausar por un solo mal resultado, o doblar cambiando 3 variables a la vez.
- Hipótesis inverificables ("el contenido no conectó") sin elemento ni número falsable.
- Proponer de nuevo un ángulo/segmento que el Cerebro registra como pausado o cerrado.

## Formato de entrega

**Top (con hipótesis) · Flop (con hipótesis) · máximo 3 acciones para el ciclo siguiente**, cada acción con la métrica y ventana que la validará, y la marca de confianza (direccional si la muestra es chica). Cierra con qué quedó pausado y su criterio de reactivación.
