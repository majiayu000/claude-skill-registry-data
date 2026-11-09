---
name: consultar-backlog
description: >-
  (Solo lectura) Consultar y AUDITAR el backlog de Azure DevOps sin escribir
  nada: responder si una funcionalidad ya tiene historia y dónde está, auditar
  la COBERTURA (fichas del Cerebro Digital sin ticket, tickets sin documento
  fuente) y detectar DESFASE (drift) entre el documento vigente del Cerebro
  Digital y el contenido de la tarjeta. Usar cuando se pida "¿esta funcionalidad
  tiene historia?", "¿a qué tarjeta corresponde X?", "auditá la cobertura del
  board", "¿la #NNNN está al día con su doc?", "detectá desfases",
  "/consultar-backlog". NUNCA crea ni edita (solo herramientas de lectura del
  MCP). Español (Argentina); no inventa (los #ID y estados son dato duro).
---

# Consultar backlog (solo lectura)

> **Tablero local (`DEC-006`):** si el proyecto usa el tablero local, «el board» es `cerebro-digital/<modulo>/backlog/`
> y se opera con `bin/tablero-local.py`, con los mismos GATEs y sin MCP (detalle: `backlog/README.md` del módulo).
> Con Azure DevOps, Jira u otro tablero, las operaciones se traducen con la tabla de `integracion-azure-mcp/00-index.md`.

Es la contraparte de **lectura** de las skills de escritura: donde
[[sincronizar-backlog]] y [[cargar-a-azure]] **escriben** en el board,
`consultar-backlog` solo **lee y audita**. No tiene riesgo: no llama a ninguna
herramienta de escritura del MCP.

> Simetría del paquete: el Cerebro Digital (`cerebro-digital/`) tiene sus propias
> skills para crear/mantener las fichas; este paquete las **lee**. Leer/
> escribir el **board** lo cubren **`consultar-backlog` (leer)** y
> `sincronizar-backlog` / `cargar-a-azure` (escribir).

## Qué responde (tres usos)

1. **Localización.** "¿Esta funcionalidad ya tiene historia? ¿Dónde? ¿Está
   linkeada a su documento fuente?" → busca por **etiqueta temática**, **objetivo/
   alcance** y **documento fuente** (comparando objetivo/alcance, **NO título** — un
   título distinto no prueba que no sea duplicado) y devuelve los `#ID` + links.
   **Este uso es el MOTOR de deduplicación** que [[cargar-a-azure]] y
   [[sincronizar-backlog]] invocan como precondición obligatoria **antes de crear**,
   produciendo el **Bloque de dedup** que gatea la escritura (ver
   [[deduplicacion-antes-de-crear]]).
2. **Cobertura (auditoría).** Cruza el Cerebro Digital con el board:
   - **Fichas sin ticket**: documentos con el bloque `## Derivación a backlog`
     cerrado que todavía no bajaron al backlog.
   - **Tickets sin documento fuente**: tarjetas que no referencian ninguna ficha
     (traza rota).
3. **Desfase (drift).** Compara el **documento vigente** del Cerebro Digital con
   el **contenido de la tarjeta** (Description, Criterios de aceptación, `[RN-…]`)
   y marca dónde difieren. **Solo detecta**; la actualización con su DIFF y el
   aviso al equipo la hace [[sincronizar-backlog]] (ver [[cambios-en-el-backlog]]).

## Herramientas (todas de lectura)

`list_projects`, `get_work_item`, `search_work_items`, `list_work_items`,
`get_work_item_comments`. Nunca `create_*` / `update_*` / `manage_*`.

## Flujo

1. **Entender el pedido**: localización, cobertura o desfase (o varios).
2. **Leer del board** por MCP (etiqueta temática, `#ID`, iteración, estado,
   responsable) y del **Cerebro Digital** del proyecto (la ruta está declarada en
   [[contexto-proyecto]]) lo que haga falta para cruzar.
3. **Cruzar y reportar**:
   - Localización → tabla `funcionalidad → #ID → link → doc fuente`.
   - Cobertura → dos listas: fichas sin ticket · tickets sin doc fuente.
   - Desfase → por tarjeta, qué difiere respecto del doc vigente (`+` falta, `~`
     cambió, con su `[RN-…]` si se puede rastrear).
4. **Derivar la acción** (sin ejecutarla): si hay desfase o falta cobertura,
   indicar qué skill de escritura lo resolvería ([[sincronizar-backlog]] /
   [[cargar-a-azure]]) — pero esta skill **no escribe**.

## Barreras

- **Solo lectura.** Si el pedido implica crear/editar/comentar, esta skill
  **no** lo hace: lo deriva a la skill de escritura correspondiente.
- **No inventar.** Los `#ID`, estados y fechas son dato duro; lo que no se puede
  leer se marca `⚠`, no se supone.
- **Sin PHI** en lo que se reporte (marcadores `<persona>`, `<documento>`, …).
- **Español (Argentina)**, al grano.

## Contexto adicional

- Actualizar una tarjeta desfasada y avisar al equipo: [[cambios-en-el-backlog]]
- Escritura en lote desde una ficha / re-sincronización: [[sincronizar-backlog]]
- Escritura de un item suelto: [[cargar-a-azure]]
- Trazabilidad (etiqueta, documento fuente, `[RN-…]`): [[organizacion-y-trazabilidad]]
- Memoria del trabajo (log de tickets): [[historial/INDICE]]

---

### Ejemplo (genérico)

> "¿La ficha `un-modulo` ya está en el board y al día?" La skill busca por la
> etiqueta temática, encuentra la Épica `#4801` con 3 Historias hijas, confirma
> que cada una referencia `cerebro-digital/.../un-modulo.md`, y detecta que la ficha
> agregó una regla `[RN-…]` que **no** figura en los criterios de la `#4803`
> (desfase). Reporta la cobertura y el desfase, y sugiere resolverlo con
> [[sincronizar-backlog]] (que propone el DIFF y avisa al que la tenga asignada).
> No escribe nada.
