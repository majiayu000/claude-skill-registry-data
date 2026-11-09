---
name: cognitive-doc-design
description: Patrones de diseño de documentación cognitiva para borradores funcionales del proyecto. Prioriza legibilidad, progressive disclosure, tablas de decisión y evita texto denso.
license: Apache-2.0
---

# Cognitive Doc Design — Patrones de Documentación Cognitiva

## Cuándo se usa

Aplicar SIEMPRE al redactar, estructurar o corregir borradores funcionales en el OKF del proyecto:
- Borradores de reglas de negocio (`F-Draft`).
- Notas de contexto, flujos y guías de diseño.
- Cualquier documento que vaya a ser leído por un humano (funcional, no técnico) o por un agente.

NO aplica a: `log.md` (audit log operativo) ni `index.md` (índice).

## Principios

1. **Legibilidad por encima de completitud.** Un lector debe entender la regla en menos de 30 segundos. Si necesita releer, el diseño falló.
2. **Progressive disclosure.** Lo esencial primero, el detalle bajo demanda. Nunca sepultar la regla en contexto histórico.
3. **Tablas de decisión para reglas condicionales.** Toda regla con condiciones (si X → Y) va en tabla. Prohibido anidar condiciones en prosa.
4. **Sin texto denso.** Párrafos de más de 4 líneas → partir. Listas de más de 7 ítems → agrupar. Jerga innecesaria → eliminar.
5. **Idioma del lector (criollo para el funcional).** Si el documento o la pregunta va a un **funcional** (no técnico), va en **criollo**: sin siglas en la cara del lector (`RN-…`, `P-…`, `[S-nn]`, "OKF", "bloque de derivación"), con un ejemplo concreto. Las siglas y la trazabilidad quedan **por debajo** (nota al pie o capa interna), para el sistema — no se pierden, no se muestran. Aplica SIEMPRE que se genere documentación o Historias de cara al funcional, sea desde un mockup o en el flujo normal. (Lo **técnico para un dev** — contrato, tests de una Tarea — mantiene su precisión: cada audiencia, su idioma.)

## Estructura del borrador

Un borrador funcional se organiza así (en este orden):

1. **Propósito** (2-3 líneas): qué resuelve este documento.
2. **Glosario** (solo si hay términos ambiguos): término → definición en una línea.
3. **Reglas de negocio**: numeradas con el prefijo del módulo (RN-<MOD>-001, RN-<MOD>-002…; nunca RN-nnn suelto), cada una con título descriptivo.
4. **Flujo** (si aplica): pasos numerados o diagrama de secuencia simple.
5. **Dudas y preguntas**: bloque explícito al final con lo que falta validar con el equipo funcional.
6. **`## Derivación a backlog`** (en toda ficha de flujo o funcional): `Slices [S-nn]`,
   `Capacidades [C-nn]` y `Flujos [F-nn]` **enumerados**, y **cada regla de la ficha
   asignada a un `[F-nn]`** o declarada fuera de alcance con su motivo. Es el bloque que
   después fija el conteo **1:1** de Épicas/Features/Historias: sin él la ficha **no se
   deriva**, y si está incompleto el árbol sale mal **de forma determinista** — todos los
   LLM producen el mismo árbol equivocado. Lo incierto va `⚠` a confirmar por el humano.
   Detalle del formato: [[organizacion-y-trazabilidad]] §5.

## Tablas de decisión

Formato canónico para reglas condicionales:

| # | Condición | Acción |
|---|-----------|--------|
| 1 | `<condición textual de la regla>` | `<acción que corresponde>` |
| 2 | `<la condición contraria>` | `<la otra acción>` |

> **El ejemplo va con marcadores a propósito.** Antes tenía un caso "real" (un umbral de antelación) que **no corresponde a ninguna regla del Cerebro**: un ejemplo inventado en una skill se copia como si fuera doctrina. Si necesitás un ejemplo concreto, tomá una regla que exista y citá su ruta.

Reglas:
- Una fila por combinación de condición → acción.
- Condiciones binarias (sí/no) → dos filas explícitas.
- Si hay más de 6 filas, agrupar por familia de condición (ej: "por ventana horaria", "por rol").

## Consulta guiada al funcional (cuando falta info)

Cuando para completar algo (el bloque `## Derivación a backlog`, una regla, un campo)
**falta un dato que solo el funcional puede dar** —o la IA tendría que inventar—, NO se
vuelca una lista técnica y se espera. Se **conduce** la consulta:

- **Se dispara sola.** El funcional no invoca nada: apenas aporta una pantalla/mockup o
  reglas para el backlog y aparece un hueco, la IA abre la consulta. (El funcional no
  sabe qué preguntar; la IA lo conduce — es el problema que esto resuelve.)
- **Ítem por ítem, en criollo.** Una pregunta a la vez, en lenguaje llano y con un
  ejemplo; se espera la respuesta antes de la siguiente. Nunca una lista técnica seguida
  de silencio.
- **Reusa el patrón de decisión por ítem** del [[cerebro-orquestador]] (Guardar / Ignorar
  / Editar y Guardar): misma mecánica, aplicada a completar la ficha.
- **La trazabilidad va por debajo.** Cada pregunta guarda el `[RN-…]`/`[P-…]` que la
  origina (para el sistema); el funcional solo ve la pregunta en criollo.
- **No inventar.** Lo que el funcional no cierra queda como pendiente; nunca se completa
  por suposición. El bloque `## Dudas y preguntas` es el registro escrito; esta consulta
  es cómo se resuelve, conversando.

## Anti-patrones

| Anti-patrón | Ejemplo | Reemplazo |
|-------------|---------|-----------|
| Condicional anidado en prosa | "Si la solicitud es urgente y además el recurso tiene disponibilidad, entonces…" | Tabla de decisión |
| Párrafo-muralla | 8 líneas seguidas de regla + excepciones + antecedente | Partir en propósito + tabla + nota |
| Completitud ciega | Documentar 20 casos borde sin priorizar los que ocurren en la operación | Priorizar por frecuencia e impacto |
| Sin trazabilidad | Mencionar "según el manual" sin citar la fuente | Wikilink a `fuentes.md` y cita de sección |

## Checklist de entrega (F-Draft)

- [ ] Propósito de 2-3 líneas al inicio.
- [ ] Reglas numeradas con título descriptivo.
- [ ] Condicionales en tablas de decisión (no en prosa).
- [ ] Sin párrafos de más de 4 líneas.
- [ ] Bloque "Dudas y preguntas" al final si hay algo sin validar.
- [ ] Wikilinks a `fuentes.md` o a la nota relacionada (trazabilidad).
- [ ] **Bloque `## Derivación a backlog`** con `[S-nn]`/`[C-nn]`/`[F-nn]` enumerados (en fichas de flujo o funcionales).
- [ ] **Cada flujo de negocio que aparece en la prosa está enumerado como `[F-nn]`**, o declarado fuera de alcance **con su motivo escrito**. Este es el chequeo que evita el error más caro del pipeline: un flujo que quedó en la prosa y no en la lista **no puede convertirse en Historia nunca**, en ningún LLM — la Regla de cardinalidad prohíbe crear nodos fuera de la enumeración. El error se vuelve **determinista**.
- [ ] **Cada regla de la ficha asignada a algún `[F-nn]`**, o declarada fuera de alcance. Sin residuo: el bloque fija **cuántas** Historias, pero si no dice **qué regla va en cuál**, ese reparto lo decide el modelo y las reglas no asignadas desaparecen para todo lo que viene después.
