---
name: tomar-tarea
description: >-
  Antes de ponerse a trabajar una historia/tarea/bug de Azure DevOps, "tomarla":
  asignarla a la persona y pasarla a Active, avisando ANTES si ya la tomó otra
  persona (evita que dos trabajen la misma en paralelo y se desincronicen). Usar
  cuando se pida "tomo esta HU", "voy a trabajar la #NNNN", "asigname / agarro la
  tarea", "empiezo con la historia X", "/tomar-tarea". Lee por MCP (solo lectura);
  la asignación y el cambio de estado se escriben con confirmación. Español (Argentina).
---

# Tomar tarea (coordinación / evitar desincronización)

> **Tablero local (`DEC-006`):** si el proyecto usa el tablero local, «el board» es `cerebro-digital/<modulo>/backlog/`
> y se opera con `bin/tablero-local.py`, con los mismos GATEs y sin MCP (detalle: `backlog/README.md` del módulo).
> Con Azure DevOps, Jira u otro tablero, las operaciones se traducen con la tabla de `integracion-azure-mcp/00-index.md`.

Resuelve el problema de dos personas agarrando el mismo work item en momentos
distintos. Usa los campos nativos de Azure **Assigned To** (quién la tiene) y
**State** (New → Active…) para dejar claro que está tomada y **avisar si ya lo está**.

## Regla de oro
- **GATE de TABLERO (duro).** La tarjeta debe pertenecer al tablero autorizado (org `{{AZURE_ORG}}` · proyecto `{{AZURE_PROYECTO}}` · team `{{AZURE_TEAM}}`); antes de cambiar `AssignedTo`/`State` verificá el destino y, si es otro tablero, **no escribas** y mostrá la advertencia ([[tablero-autorizado]]).
- **Chequear ANTES de tomar.** Si ya está Assigned a otra persona o en Active, AVISAR (quién y desde cuándo) y **no pisarla** sin tu confirmación explícita.
- **Escritura con confirmación.** Cambiar Assigned To / State es una acción con efecto: mostrás qué vas a cambiar y se hace con tu OK — no en el mismo impulso.
- **GATE de TARJETA CONGELADA (duro).** Una tarjeta **en un sprint y ya tomada** (Estado distinto de `New`) no se reasigna ni se le cambia el Estado: sólo se comenta. Tomar una tarjeta que está en `New` sí se puede —todavía no está congelada—, y es justamente la escritura que la congela. Detalle: [[cambios-en-el-backlog]] §4.
- **No inventar · sin PHI · español (Argentina).**

## Flujo
1. **Traer la tarjeta** por MCP: `get_work_item` (solo lectura). Si te pasan un `#ID`, usalo; si no, `search_work_items` / `list_work_items` para ubicarla.
2. **Chequear coordinación:** mirar `System.AssignedTo` y `System.State`.
   - **Libre** (sin asignar / New) → paso 3.
   - **Ya tomada** (Assigned a otra persona o en Active) → **AVISAR**: "ya la tiene `<persona>` desde `<fecha>`, en estado `<estado>`" y **esperar tu decisión** (¿la tomás igual?, ¿coordinás?). No escribir sin confirmación. *(«¿La tomás igual?» vale sólo si **no** está en un sprint: ver el caso siguiente.)*
   - **Ya es tuya y está en Active** → no hay nada que escribir.
   - **Ya tomada, en un sprint y con Estado distinto de `New`** → está **congelada**: la IA **no la reasigna**, ni con confirmación. Avisa quién la tiene y ofrece dejar un comentario con @mención para coordinar; si hay que reasignarla, lo hace una persona desde Azure.
3. **Tomarla** (con tu OK): `update_work_item` → `AssignedTo` = vos, `State` = Active.
   Si está en un sprint, el preview lo avisa: *«Al tomarla queda congelada: desde ahí sólo se
   puede comentar.»*
4. (Opcional) dejar un comentario "tomada por `<vos>` el `<fecha>`" con `[[comentar-tarea]]`.

## Sin barrera de auditoría

Tomar una Tarea **no** exige el sello de [[auditar-tarea]] (decisión de diseño del template): las
auditorías son opcionales y corren sólo si alguien las pide. Exigirlas acá gastaba muchos
tokens y volvía a preguntar cosas ya cerradas o que no hacían falta para arrancar.

Si al trabajarla aparece un hueco o un gris, no se frena: queda **como pendiente en la
tarjeta** ([[comentar-tarea]] §«Pendientes a confirmar»), y se mira **antes de cerrarla**.

## Contexto adicional
- Herramientas MCP y escritura con confirmación: [[integracion-azure-mcp/04-automatizar-con-ia]] · [[integracion-azure-mcp/00-index]].
- Dejar comentarios en la tarjeta: [[comentar-tarea]].

---

### Ejemplo (genérico)
> A las 9 hs, la persona A escribe "tomo la #NNNN". La skill hace `get_work_item`,
> ve que está libre y —con su OK— la asigna a A y la pasa a Active. A las 11 hs la
> persona B escribe "voy a trabajar la #NNNN": la skill ve que ya está Assigned a A
> desde las 9 hs y **avisa** en vez de dejar que B la trabaje en paralelo. B coordina
> con A. No hay desincronización.
