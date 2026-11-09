---
name: estimar-story-points
description: >-
  Calcular los Puntos de historia (Story Points) de una historia / tarea /
  habilitador cuando el desarrollo lo hace la IA: el puntaje sale de la
  COMPLEJIDAD a nivel sistema + el CONSUMO DE TOKENS para resolver el desarrollo
  y para investigar historias/fichas relacionadas. NO usa Planning Poker ni
  estimación por consenso humano (desarrolla la IA). Usar cuando se pida "estimá
  esto", "cuántos puntos", "puntuá / asigná story points a esta historia",
  "/estimar-story-points". Salida en escala Fibonacci (1,2,3,5,8,13,20) por
  compatibilidad con el campo de Azure; 13+ => partir. La IA propone el número y
  el humano puede ajustarlo. NO inventa: lo que falta va (pendiente) y se
  pregunta. Español (Argentina). NO escribe en el board.
---

# Estimar Story Points

En este flujo **el desarrollo lo hace la IA**, así que el puntaje **no** sale de un
Planning Poker ni de un consenso de equipo: lo **calcula la IA** a partir de dos
cosas medibles a nivel sistema:

1. **Complejidad del desarrollo** — cuántas capas/módulos toca, algoritmos,
   manejo de estados, integraciones, reglas de negocio.
2. **Consumo de tokens** — cuánto le cuesta a la IA **resolver** el desarrollo y
   cuánto le cuesta **investigar** (navegar) las historias/fichas relacionadas.

El número se expresa en **Fibonacci** (1, 2, 3, 5, 8, 13, 20) solo por
compatibilidad con el campo *Puntos de historia* de Azure; de 13 para arriba, se parte.

> El punto acá **no** mide "cuánto tarda una persona": mide **cuánto le cuesta al
> sistema (la IA) entregarlo**. El token es la señal más directa de ese costo.

## Regla de oro

- **Lo calcula la IA, no un Planning Poker.** No hay votación ni consenso humano
  (desarrolla la IA). La IA propone el número con su justificación; **el humano
  puede ajustarlo**, pero no hace falta una ceremonia de estimación.
- **El token manda como señal de costo.** Cuanto más cuesta resolver + investigar
  (en tokens), más pesa el ítem. La complejidad a nivel sistema completa el cuadro.
- **NO inventar.** Si falta info para evaluar una señal (relacionadas,
  integraciones, reglas), se marca `⚠ (pendiente)` y se pregunta. Los umbrales
  token→banda no se inventan: se calibran con datos reales del historial.
- **13+ ⇒ partir.** Si da 13 o más, la acción es descomponer, no "estimar heroico".
- **Español (Argentina). Esta skill NO toca el board:** solo calcula/propone.

## Las señales

### A-priori — antes de desarrollar (estimación de entrada)
Antes de codear no se conocen los tokens reales, así que se estima con proxies
observables del ítem:

| # | Señal | Suma poco | Suma mucho |
|---|---|---|---|
| 1 | **Complejidad a nivel sistema** | cambio directo, patrón conocido, 1 capa | varias capas/servicios, algoritmo, manejo de estados |
| 2 | **Integraciones / dependencias** | interno, sin sistemas externos | uno o más sistemas externos, autenticación federada, otros servicios |
| 3 | **Reglas de negocio `[RN-…]`** | ninguna o una simple | varias, con bordes/excepciones |
| 4 | **Investigación en relacionadas** | 0-1 relacionada, superficial | muchas historias/fichas, grafo profundo |
| 5 | **Incertidumbre / claridad** | requerimiento claro, sin `⚠` | difuso, muchos `(pendiente)` |
| 6 | **Novedad vs. precedente `gold`** | hay un `gold` parecido para imitar | net-new, sin precedente |

### A-posteriori — el token real (la señal más fuerte)
Cuando la IA **efectivamente** resuelve o investiga, mide y usa:

- **Tokens para RESOLVER** — cuánto costó producir la solución (proxy directo de la
  complejidad real).
- **Tokens para NAVEGAR relacionadas** — cuánto costó leer/investigar historias y
  fichas para entender o resolver.

> El token real se conoce **durante/después** del desarrollo. Antes se usa el perfil
> de proxies (1-6); con el token real, la IA **ajusta** el número y lo **registra en
> el historial** para ir calibrando el mapeo "tantos tokens ≈ tanta banda". Los
> umbrales exactos arrancan `(pendiente)` y se fijan con datos.

## Flujo

1. **Traer el ítem.** Texto, o por MCP `get_work_item` (solo lectura) si es un `#ID`.
   Si hace falta, leer las relacionadas y las fichas del Cerebro Digital del tema
   (la ruta está declarada en [[contexto-proyecto]]).
2. **Evaluar las 6 señales a-priori** y, si la IA ya resolvió/investigó, sumar el
   **token real** (resolver + navegar).
3. **Mapear a una banda Fibonacci.** El conjunto de señales + el costo en tokens
   define la banda.
4. **Justificar en 1-2 líneas** qué pesó (p. ej. "8: toca 2 servicios + 4 reglas + 3
   relacionadas profundas; alto costo de investigación").
5. **Marcar `⚠`** toda señal que no se pueda evaluar por falta de info, y preguntar.
6. **Si da 13+**, proponer **partir** el ítem y estimar las partes.
7. **Registrar** el número (y, si hubo, los tokens reales) en la fila del
   [[historial/INDICE]] para calibrar las próximas.

## Cómo se combinan las señales → banda (orientativo)

| Perfil | Banda |
|---|---|
| Cambio directo, hay `gold` para imitar, casi sin investigación | 1 - 2 |
| Complejidad media, alguna regla, 1-2 relacionadas | 3 |
| Varias piezas o 1 integración simple; investigación media | 5 |
| Alta complejidad **o** integración externa **o** mucha investigación/incertidumbre; token de resolver alto | 8 |
| Varias señales altas a la vez (complejidad + integración + incertidumbre) | 13 ⇒ **partir** |

> Es una guía para no arrancar de cero cada vez, no una fórmula rígida. La IA
> propone; el humano puede ajustar.

## Contexto adicional

- Base de estimación (escala Fibonacci, Gravedad/Prioridad, MoSCoW): [[estimacion-y-priorizacion]]
- Control de que la historia esté lista para estimar: [[definicion-preparado-terminado]]
- Registro y calibración con tokens reales: [[historial/README]]
- Lectura de tarjetas por MCP: [[integracion-azure-mcp/00-index]]

---

### Ejemplo (genérico)

> Historia: *"Filtrar recursos por cercanía en un módulo"*. La IA evalúa: complejidad
> media (cálculo de distancia), 1 integración (un servicio externo de padrón/geo), 2
> reglas `[RN-…]`, 3 relacionadas a leer, sin `gold` previo; la investigación le costó
> bastante en tokens (leyó 3 fichas). Propone **8**, con la justificación, y sugiere
> partir en "endpoint de cercanía" + "UI del filtro". `⚠ (pendiente)`: ¿la distancia
> sale de un servicio existente o hay que crearlo? (define si sube a 13). El número lo
> propone la IA; el humano lo puede ajustar.
