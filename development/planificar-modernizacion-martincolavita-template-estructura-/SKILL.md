---
name: planificar-modernizacion
description: >-
  Con el Cerebro ya poblado por absorber-aplicacion, decidir CON EL HUMANO qué se hace con una
  aplicación existente y dejar el plan listo: compara las estrategias (refactor en el lugar,
  migración por estrangulador slice por slice, corrida en paralelo, subir de versión de framework
  o de lenguaje, o no tocarla) con la tabla medida por los scripts, hace la curaduría de cada
  regla y cada comportamiento raro (migrar / descartar / decide el humano), escribe DEC-004 con el
  «sí», ordena los slices y arma una ficha por slice con su bloque de derivación. Usar cuando se
  pida "¿refactorizo o migro?", "planificá la migración de esta app", "armá el plan de
  modernización", "/planificar-modernizacion". No programa nada; no decide sola: propone con
  los números a la vista y pregunta. Español (Argentina).
---

# Planificar la modernización de una aplicación existente

Arranca donde termina [[absorber-aplicacion]]: el inventario y la radiografía corrieron, el Cerebro tiene
las entidades, reglas confirmadas y candidatas, integraciones, deuda y huecos de la aplicación. Esta
skill convierte eso en **una decisión escrita** (`DEC-004`) y **un plan por slices** que después ejecuta
[[modernizar-slice]] con la red de [[caracterizar-comportamiento]].

## Lo que NO hace

- **No toca la aplicación existente** ni escribe código.
- **No decide la estrategia.** Arma la tabla, propone con su porqué y **pregunta**. `DEC-004` la decide la
  persona y la escribe `cerebro-curator` con su "sí".
- **No arranca sin el Cerebro poblado.** Si falta el inventario, la radiografía o la matriz de cobertura
  de la absorción, la fase 0 es `SIN DATOS` y se vuelve a [[absorber-aplicacion]].
- **No arregla un bug viejo por criterio propio**: lo pone en la curaduría como «decide el humano».

## Fase 0 — Lo medido (lo traen los scripts)

Se leen, no se rehacen: `borrador/absorcion/<fecha>/01-inventario.md` (bloque «Para DEC-004»),
`01b-radiografia.md` (módulos, cruces de capa, ciclos), `04-cobertura.md` (qué se leyó y qué quedó
HUECO) y, si hay base, el esquema real con `bin/esquema-base.py <base-o-ddl> --salida borrador/absorcion/<fecha>/05-esquema.md`.
Un módulo HUECO en la cobertura **no se planifica**: se lee primero o se declara fuera de alcance.

## Fase 1 — Comparar estrategias (una tabla, no una recomendación suelta)

| Estrategia | Cuándo conviene | Qué exige | Lo que se mide |
|---|---|---|---|
| **Refactor en el lugar** | El stack sigue (`DEC-003`), los límites de módulo se pueden imponer donde está, hay o se puede poner red | Caracterización por módulo antes de tocar; un módulo por Tarea | red de tests, cruces de capa, deuda |
| **Migración por estrangulador** (slice por slice, la vieja sigue viva) | Cambia el stack o la estructura no se arregla en el lugar; la app tiene que seguir en producción | Contrato por slice sacado del código viejo, paridad contra el oráculo, un punto de enrutado | contrato de API, integraciones, volumen |
| **Corrida en paralelo** | Flujos que dan plata o con riesgo alto: la vieja y la nueva reciben lo mismo y se comparan salidas antes del corte | Lo mismo que el estrangulador, más captura de tráfico o doble escritura; es caro | criticidad del flujo |
| **Subir de versión** (framework o lenguaje) | El problema es la versión, no la forma | Cambios chicos y reversibles, salida vieja contra nueva, corte por bandera con vuelta atrás ([subir-de-version.md](../../skills/modernizar-slice/references/subir-de-version.md)) | dependencias vencidas, CVE |
| **No tocarla** | Funciona, está aislada y nadie la va a cambiar | Documentarla (ya se hizo en la absorción) y declararlo | — |

Las filas medibles salen del inventario con sus umbrales declarados; la skill **completa sólo** las de
lectura (límites de módulo) y encuadre (stack deseado, producción, plazo, quién la usa). Se cierra con una
**propuesta y su porqué, en criollo**, y **una pregunta**. La respuesta va a `arquitectura/decisiones.md`
como `DEC-004`, `Confirmado` sólo después del "sí". **Gran explosión (big bang) no es una opción**: si se
pide, se dice por qué no y se ofrece el estrangulador con un solo slice grande.

## Fase 2 — Curaduría de reglas y comportamientos

Por cada regla candidata `RC-nn` y cada comportamiento raro que la absorción dejó en `pendientes.md`, una
fila con **una** de tres decisiones, tomada por el humano con la evidencia (`archivo:línea`, fragmento,
test o «sin test») a la vista:

| Decisión | Qué significa | Adónde va |
|---|---|---|
| **MIGRAR** | Se reproduce tal cual, aunque parezca un bug: alguien puede depender de eso | `RN-<MOD>-nnn` confirmada; caso de paridad obligatorio |
| **DESCARTAR** | No se reproduce; se deja escrito por qué | `aplicacion/deuda.md` o `decisiones.md`; sin caso de paridad. Cuando la paridad corra y muestre esa diferencia, se la **acepta** con nombre en `aceptadas.json` ([[modernizar-slice]] §4) |
| **DECIDE EL HUMANO** | Todavía no se sabe; frena el slice que la toca | `pendientes.md` como `P-nnn`; el slice no pasa de «contrato» hasta cerrarla |

Se trabaja por tandas, una tabla por módulo y un "sí" que escribe esa tabla (modo lote).

## Fase 3 — Los slices y su orden

Un slice es **un conjunto de flujos que se puede cortar junto**: comparte contrato, datos y pantalla. Se
proponen desde la radiografía (módulos, endpoints, dependencias) con el orden **menos dependencias y más
valor primero**, y por cada uno:

- su **ficha** en `borrador/absorcion/<fecha>/03-plan/<slice>.md`, con entidades, reglas (ya confirmadas),
  flujos, integraciones y el bloque `## Derivación a backlog` propuesto `⚠` (`[S-nn]`, `[C-nn]`, `[F-nn]`);
- la **fila en `aplicacion/modernizacion.md`** (estado `pendiente`, estrategia, contrato, corpus, golden, paridad,
  corte aprobado por), que `bin/mapa-modernizacion.py ver` lee; es el tablero de avance de toda la modernización;
- qué **datos** mueve y cómo (expandir / migrar / contraer, [migracion-de-base.md](../../skills/desarrollo/references/metodo/migracion-de-base.md)).

Con el "sí" sobre las fichas, el pipeline es el de siempre: [[sincronizar-backlog]] o [[planificar-lote]]
→ Tareas → [[desarrollar-asignadas]]. La ejecución de cada slice la conduce [[modernizar-slice]].

## Barreras

- **Sin Cerebro poblado y matriz de cobertura, `SIN DATOS`**: no se planifica sobre una impresión.
- **`DEC-004` la decide la persona** (y la escribe `cerebro-curator` con su "sí"); sin ella confirmada no hay fichas ni Tareas.
- **Ninguna regla pasa a MIGRAR o DESCARTAR sin una persona**; lo que no se decide frena su slice, no el plan.
- **Un slice sin corpus de paridad planificado no es un slice**: cada ficha nombra qué casos lo prueban.
- **La aplicación vieja no se toca**, tampoco para "preparar" la migración: un desvío de tráfico es una Tarea con su "sí".
- Todo en español (Argentina). Sin PHI en fichas ni ejemplos.

## Cómo entra en el veredicto

| Estado | Cuándo |
|---|---|
| **OK** | `DEC-004` confirmada, curaduría cerrada por módulo, fichas por slice con derivación y la tabla de `modernizacion.md` con todos los slices en `pendiente` |
| **HALLAZGO** | Una regla migrada sin decisión humana, un slice sin casos de paridad, un módulo HUECO planificado igual |
| **SIN DATOS** | Falta el inventario, la radiografía o la cobertura de la absorción |
