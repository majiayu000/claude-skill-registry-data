---
name: portal-ux-patterns
description: Reference for the six committed UX patterns of the Portal (progressive disclosure, predictive insight cards, tool-call visibility with explainable overlays, real streaming plus stop, role-based workspaces, shared dashboard-chat state). Use when designing or reviewing any UI flow, writing UX deliverables (A2-A5), or verifying that an implementation honors a committed pattern and its acceptance criteria.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal UX Patterns Skill (§6.2)

## Rules — NON-NEGOTIABLE

- Estos 6 patrones son el **compromiso UX del proyecto** (§6.2 del plan): toda pantalla, componente o entregable que los toque debe respetar su criterio de aceptación textual. No se degradan sin acuerdo de equipo documentado.
- Cada patrón tiene fundamento en un paper 2026 verificado (`docs/papers/`); al justificarlo en entregables (A2–A5) citar el paper, no opinión.
- Honestidad de demo: previsiones SIEMPRE etiquetadas como simuladas; jamás fingir ML real.
- La transparencia del agente (tarjetas + overlay) no es decorativa: es auditable — parámetros y fuentes reales del tool call, nunca texto inventado.
- UI en español neutro, sin emojis; los nombres de patrón pueden citarse en inglés en docs técnicos.

## Los 6 patrones

### 1. Progressive Disclosure

- **Qué es**: resumen → detalle → herramientas avanzadas; el usuario decide cuándo profundizar (refuerzo empírico §3.5: hasta el agente navega jerárquicamente).
- **Dónde**: tarjeta → panel expandible con serie ECharts → tabla de detalle → enlace al explorador.
- **Criterio verificable**: 3 niveles de profundidad, **≤2 clics** entre niveles; estados skeleton/vacío sin layout shift en cada nivel.

### 2. Predictive Insight Cards

- **Qué es**: previsiones calculadas visibles en la vista principal directiva, antes que los datos técnicos.
- **Dónde**: `InsightCard.vue` en `/dashboard`; cálculo server-side con Polars.
- **Criterio verificable**: cada tarjeta lleva **etiqueta honesta de método**, p. ej. "Riesgo de liquidez +12 % próximo mes — proyección lineal sobre sintéticos". Sin etiqueta, la tarjeta no pasa QA.

### 3. Tool-Call Visibility + Explainable Overlays

- **Qué es**: auditar qué base consultó la IA **antes** de leer su texto (paper 07, Catch-22 de la transparencia: tres focos — usuario final ve progreso legible, desarrollador ve parámetros exactos, gobernanza ve fuentes y permisos).
- **Dónde**: `ToolCallCard.vue` (estados anuncio/ejecución/resultado/error) + `LazyLineageOverlay.vue`.
- **Criterio verificable**: por cada tool call, tarjeta con (1) anuncio, (2) estado de ejecución con tiempo, (3) resultado renderizado (mini-tabla o cifra) antes del texto generado; el overlay de linaje muestra tools llamadas, parámetros y fuentes del catálogo; los eventos `tool_call` alimentan las tarjetas **sin re-render del historial completo**.

### 4. Streaming + Stop real

- **Qué es**: la respuesta se genera en vivo y el Stop corta la llamada al LLM en milisegundos — cancelación real, no cosmética (paper 10, Stream2LLM; presupuesto de latencia §3.10).
- **Dónde**: `/api/chat` SSE + `useChatStream` (ver `portal-sse-streaming`).
- **Criterio verificable**: TTFT p50 < 700 ms; Stop registra el evento y no deja tareas colgadas (prueba de cleanup); error a mitad de stream ofrece Reintentar sin borrar la conversación.

### 5. Workspaces por rol con defaults

- **Qué es**: configuración default de módulos por perfil + reordenamiento ligero. Fundamento paper 09 (Generative UI Personalization): acuerdo inter-evaluador kappa 0.25 sobre la "mejor" UI → **no imponer una vista única**; defaults sensatos y control al usuario.
- **Dónde**: homes por rol desde el JWT: **Operativo** = buscador arriba; **Analista** = explorador + exportaciones; **Directivo** = tarjetas predictivas + resumen del agente.
- **Criterio verificable**: el rol del JWT determina el home y los módulos visibles (`HOME_BY_ROLE`, `hasScope`); un usuario nunca ve módulos fuera de su scope; el default de cada perfil coincide con la tabla anterior.

### 6. Estado compartido dashboard↔chat

- **Qué es**: los filtros del dashboard son contexto del agente y viceversa (paper 06, TwinBI: BI y conversación como gemelos sincronizados).
- **Dónde**: store Pinia `workspace`; drill-down de ECharts alimenta `filters`; acción **"Resumir vista actual"** desde el dashboard directivo.
- **Criterio verificable**: los filtros activos viajan como contexto en cada consulta del chat (visible en el overlay de linaje); "Resumir vista actual" produce un resumen coherente con los filtros aplicados, no con el dataset completo.

## Tabla de trazabilidad

| # | Patrón | Paper | Gate de QA |
|---|--------|-------|------------|
| 1 | Progressive Disclosure | planteamiento + §3.5 | 3 niveles, <=2 clics |
| 2 | Predictive Insight Cards | honestidad de demo | etiqueta de método presente |
| 3 | Tool-Call Visibility + Overlays | 07 Catch-22 Transparency | tarjeta antes del texto; linaje real |
| 4 | Streaming + Stop real | 10 Stream2LLM | TTFT p50<700 ms; cancelación limpia |
| 5 | Workspaces por rol | 09 Generative UI (kappa 0.25) | defaults por perfil desde JWT |
| 6 | Estado dashboard↔chat | 06 TwinBI | contexto en consulta + Resumir vista |

## Uso en entregables UX (A2–A5)

- **A2 (journey maps)**: cada escenario debe evidenciar al menos un patrón en el momento de dolor que resuelve.
- **A3 (competitivo + IA)**: comparar competidores contra estos 6 patrones como ejes.
- **A4 (alta fidelidad)**: las pantallas del prototipo web deben mostrar los estados intermedios (skeleton, tarjeta de tool call en ejecución, etiqueta de método) — no solo el happy path; los cuatro estados no felices (vacío, cargando, error, sin permiso) son criterio de US-UX-07.
- **A5 (SUS)**: las tareas del test de usabilidad se derivan de los criterios verificables de esta tabla.

## QA Checklist

- [ ] Cambio de UI revisado contra la tabla de trazabilidad (qué patrón toca)
- [ ] Ningún patrón degradado sin decisión de equipo documentada
- [ ] Previsiones con etiqueta de método en toda instancia
- [ ] Overlay de linaje refleja tool calls reales (parámetros + fuentes)
- [ ] Defaults por rol verificados con los 3 perfiles seed + admin
- [ ] Entregable UX de la semana cita el paper correcto por patrón
