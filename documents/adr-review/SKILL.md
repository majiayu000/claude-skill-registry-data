---
name: adr-review
description: Aplica el patrón ultrathink de revisión Nivel 1 a un ADR del corpus de Runcriticon. Detecta gaps en bloques A-G, propone sub-decisiones con anchors, lanza tandas de preguntas con AskUserQuestion, y termina con PRs encadenadas de revisión + aceptación. Úsala cuando se proponga reabrir un ADR aceptado, cuando entre un ADR nuevo, o cuando el equipo quiera auditar un ADR contra el patrón consolidado.
disable-model-invocation: true
---

# ADR Review (Nivel 1) — Runcriticon

Patrón consolidado tras aplicarse a los 16 ADRs del corpus en mayo de 2026. Reproducible para cualquier ADR futuro.

## Cuándo usar esta skill

- Reabrir un ADR aceptado porque se ha activado un **disparador** documentado en [`docs/adr/0015-temas-aplazados-fuera-del-mvp.md`](../../../docs/adr/0015-temas-aplazados-fuera-del-mvp.md) (matriz configurable, multi-rol, soporte interno, segundo club, etc.).
- Auditar un ADR existente que se sospecha desactualizado por nuevas decisiones.
- Auditar que un ADR nuevo aplicó correctamente el patrón Nivel 1 (`adr-creator` ya lo genera para decisiones compuestas; esta skill verifica si el resultado es correcto antes de la primera PR de revisión).

## Patrón canónico (ultrathink en 7 bloques)

1. **Veredicto** — 1 párrafo honesto: qué está sólido + cuántos problemas centrales hay (típicamente 1-3) y cómo de profundos.
2. **Lo que está bien hecho** — lista numerada de fortalezas explícitas. No es decoración; el ADR original tiene que recibir crédito por lo que ya hace bien.
3. **Debilidades y lagunas en bloques A-G** — el núcleo de la revisión:
   - **A — Estructura plana sin Nivel 1**: enumerar las sub-decisiones latentes (D1-DN) que el cuerpo ya contiene implícitamente, con capa (Estratégica / Operativa).
   - **B — Premisas heredadas**: qué ADRs aceptados (con sub-decisión concreta) deberían figurar como premisas heredadas explícitas.
   - **C — NFRs propios faltan**: dimensiones cuantitativas que el ADR debe fijar y que hoy no aparecen.
   - **D — Decisiones implícitas críticas**: las cosas que el equipo necesitará el día 1 y no están escritas. Numerar D-1, D-2... con voto fuerte si lo tengo.
   - **E — Coherencia con ADRs aceptados**: cruces explícitos detectados (`ADR-XXXX DN`) y conflictos.
   - **F — Cosas que envejecerán mal**: formulaciones cualitativas sin cifras, disparadores difusos, magic numbers, dependencias en alguna tecnología propietaria sin alternativa.
   - **G — Decisiones que el equipo encontrará el día 1**: los huecos de gobierno (roles, ciclo de vida, ownership) sin abordar.
4. **Decisiones implícitas que el equipo necesitará el día 1** — tabla resumen de los huecos del bloque D con impacto si se omite.
5. **Cosas que envejecerán mal** — recuperar el bloque F como puntos de acción.
6. **Sugerencias priorizadas** — etiquetadas A-N por importancia. Tres categorías:
   - **Imprescindibles antes de aceptar** (lo que toca decidir sí o sí).
   - **Útiles** (mejoras razonables que no bloquean).
   - **Menores** (revisión periódica, notas).
7. **Recomendación + pregunta final** — qué propongo aplicar de un barrido vs qué necesita confirmación, y la primera tanda de preguntas con `AskUserQuestion`.

## Estructura del ADR resultante (Nivel 1 consolidado)

Cada ADR revisado debe quedar con esta forma:

```markdown
# ADR-NNNN — Título

- **Estado**: Propuesto
- **Fecha**: YYYY-MM-DD · revisado YYYY-MM-DD (resumen de cambios)
- **Decisores**: ...
- **Relacionado con**: lista de ADRs relacionados

## Índice de sub-decisiones

Este ADR fija una **decisión arquitectónica compuesta** sobre [tema]. Las N sub-decisiones se agrupan en M áreas:

- **Área 1 (D1-Dk)** — resumen 1 línea
- **Área 2 (Dk+1-DN)** — resumen 1 línea

| #   | Sub-decisión                                          | Capa         |
|-----|-------------------------------------------------------|--------------|
| D1  | [Título corto](#d1)                                   | Estratégica  |
| ... | ...                                                   | ...          |

## Contexto y problema
## Premisas heredadas (no se revisan en este ADR)
## Requisitos no funcionales
## Drivers de la decisión
## Opciones consideradas
## Decisión

<a id="d1"></a>
### D1 — Título corto
...

<a id="d2"></a>
### D2 — Título corto
...

## Consecuencias
### Positivas
### Negativas / coste asumido
### Riesgos y mitigaciones

## Notas
```

**Reglas estrictas**:

- Cada `<a id="dN"></a>` va **en línea aparte** antes del `### DN — Título`.
- Las sub-decisiones son planas `### DN` (no se agrupan en `### Área` en el cuerpo; la agrupación vive solo en la tabla del índice).
- **NFRs antes que Drivers** (orden coherente con los 16 ADRs aceptados).
- Los aplazamientos conscientes se numeran como `AN` (no `DN`).
- Cruces inline a sub-decisiones de otros ADRs con formato `(ADR-XXXX DN)`.
- Cifras concretas en disparadores. Sin "cuando duela", "si el negocio lo justifica" o equivalentes.

## Patrón de preguntas multi-tanda

Las decisiones del bloque D suelen requerir input del usuario. Estrategia:

1. **Presentar el análisis completo primero** (bloques A-G + sugerencias).
2. **Empaquetar 1-4 preguntas relacionadas por tanda** con `AskUserQuestion`.
3. **Cada pregunta tiene un voto Recomendado en la primera opción**.
4. **Las opciones son completas, no "Otra"** — la propia tool permite "Otra".
5. **Capturar la respuesta, sintetizar las decisiones en una tabla, lanzar la siguiente tanda**.
6. **Terminar con confirmación** antes de aplicar al ADR.

Volumen típico observado en los 16 ADRs aceptados: **2-3 tandas de 3-4 preguntas** cada una.

## Aplicación al ADR (cadena de PRs)

Patrón de entrega que el corpus exige:

1. **PR de revisión** `feature/revision-adr-NNNN`:
   - Aplica todas las decisiones consensuadas.
   - Estado del ADR sigue siendo `Propuesto`; la marca `· revisado YYYY-MM-DD (resumen de cambios)` se añade en la línea **Fecha** (convención del corpus — el Estado va plano).
   - Cuerpo del PR enumera las sub-decisiones nuevas + cruces consolidados.
2. **Merge de la PR de revisión**.
3. **PR de aceptación** `feature/acepta-adr-NNNN`:
   - Cambia `Propuesto` → `Aceptado` en la línea **Estado** + añade `· **aceptado YYYY-MM-DD**` en la línea **Fecha**.
   - Actualiza el índice de [`docs/adr/README.md`](../../../docs/adr/README.md) marcando el ADR como `Aceptado`.
4. **Merge de la PR de aceptación**.

Si el ADR introduce o modifica un **aplazamiento**, también:

5. Actualizar [`docs/adr/0015-temas-aplazados-fuera-del-mvp.md`](../../../docs/adr/0015-temas-aplazados-fuera-del-mvp.md) en el mismo barrido (la tabla maestra) — bien en la PR de revisión o en una PR independiente posterior.

## Convenciones de naming

- Sub-decisiones: `D1`, `D2`, ... (decisiones activas).
- Aplazamientos en el índice maestro: `A1`, `A2`, ... (sin decisión activa, solo política y disparador).
- Anchors: minúsculas `<a id="d1"></a>`, `<a id="a1"></a>`.
- Cruces inline: `(ADR-XXXX DN)` o `(ADR-0015 AN)`.

## Antipatrones a evitar

- **Disparadores cualitativos** ("cuando crezca el equipo", "si el rendimiento lo justifica") sin métrica medible.
- **Mezclar agrupación visual con anchors** (`### Bloque` con sub-decisiones `#### DN` anidadas — rompe el patrón consolidado).
- **`<a id>` inline en la misma línea que el heading** — viola la convención.
- **Mantener entradas obsoletas** en ADR-0015 si otro ADR posterior las decidió activamente (corregir explícitamente; ver §"Aplazamientos retirados" del 0015).
- **NFRs después de Drivers** — invertir el orden del 0003/0010/0009/0014/etc.
