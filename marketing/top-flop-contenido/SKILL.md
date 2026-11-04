---
name: top-flop-contenido
description: Úsalo al leer resultados de PIEZAS DE CONTENIDO publicadas en redes (reels, carruseles, stories) para decidir qué se repite, qué se pausa y qué se prueba después. Produce el insumo de conceptos-contenido. Para leer el lift de campañas internas por push, el skill es diseno-experimentos.
---

# Top/flop con hipótesis: leer para decidir el siguiente envío

Una tabla de resultados no decide nada. Lo que decide es la pareja top/flop con una hipótesis falsable de POR QUÉ, convertida en la variación del siguiente ciclo.


> ### Qué fuente social tiene Kaizen, y qué no (actualizado 2026-09-11)
>
> **Instagram, parcial:** `get_instagram_profile` lee los perfiles guardados en
> Marketing → Configuración (`list_marketing_accounts` dice cuáles). Trae lo
> PÚBLICO: seguidores, seguidos, y por publicación likes y comentarios, con un
> resumen ya calculado (promedios, mediana, por tipo, top 3). Eso es **pulso**:
> sirve para contextualizar, no para decidir. **No trae** alcance, impresiones,
> guardados, retención de video, clicks al link ni registros atribuidos —
> ninguno de los 5 KPIs del funnel—, y los números son del instante en que se
> lee, sin histórico.
>
> **TikTok, parcial (2026-09-18):** `get_tiktok_profile` lee SOLO la cuenta de
> FinZen (la Display API no lee terceros): seguidores, likes totales, videos, y
> por video views/likes/comentarios/compartidos/duración, con mediana de views y
> engagement sobre views calculados. **No trae** retención de video, alcance,
> vistas de perfil ni taps al link: esos siguen en el panel nativo. Criterio en
> `lectura-perfil-tiktok`.
>
> Para lo que la tool no trae, lo único que puedes hacer es aplicar el método a
> números que el socio te pegue en el chat, o citar los que estén guardados en
> el Cerebro. **No inventes cifras de redes ni las estimes**: si te piden un KPI
> social que no tienes, di que Kaizen no tiene acceso a esa fuente todavía.

## 0. Antes de empezar

1. `get_instagram_profile` con `publicaciones: 50` y `get_tiktok_profile` con `videos: 60` (las cuentas de FinZen); en TikTok el ranking es por **compartidos** y mediana de views, no por likes (skill `lectura-perfil-tiktok`). Instagram: la lista de piezas con likes y comentarios, y el resumen con la mediana **por tipo** (REELS vs FEED). Solo hay pulso, así que el ranking que sale de acá es de atención, no de resultado; dilo así. Si el socio te pega alcance, retención o clicks del panel nativo, eso manda sobre los likes.
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
