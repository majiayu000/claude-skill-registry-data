---
name: deep-research
version: 1.0.0
description: Produce por escrito el contexto estructurado previo a un work_plan (estado actual, gaps de conocimiento, alternativas). Usar cuando el Manager o el usuario pide investigar antes de planificar un WP complejo. No usar para un WP que ya tiene work_plan aprobado (ver builder-implement-from-plan) ni para tareas triviales cuyo contexto ya esta en PROJECT.md.
triggers: [/deep-research, /research, /pre-plan-research]
author: agent
role: shared
stage: support
cycle_phase: [F2-contrato]
writes_memory: false
quality_gate: false
tags: [research, documentation, planning]
---

# deep-research

Skill documental para investigacion previa que produce contexto estructurado antes de abrir un work plan. No escribe codigo de produccion ni toca el runtime del bus.

## When to activate

- Antes de abrir un WP complejo que requiere entender el estado actual del sistema.
- Cuando el Manager o usuario pide "investiga X antes de planificar".
- Cuando necesitas identificar gaps de conocimiento antes de implementar.
- Para comparar enfoques alternativos antes de decidir una arquitectura.

## When NOT to activate

- Si ya existe un work plan aprobado (usar `builder-implement-from-plan`).
- Si la tarea es simple y no requiere investigacion (typos, cambios cosméticos).
- Si el contexto ya esta documentado en `PROJECT.md`, `AUDIT.md` o `execution_log.md`.

## Workflow (4 fases)

### Fase 1: Leer contexto base

Leer los siguientes archivos para establecer la linea base:
- `PROJECT.md` - estado actual y decisiones del proyecto
- `.agent/collaboration/work_plan.md` - ticket activo
- `.agent/collaboration/execution_log.md` - registro de implementacion
- `.agent/collaboration/STRATEGY_WOT-*.md` - estrategia del ticket (si existe; legacy-compat: `PLAN_WP-*.md`, `PLAN_WT-*.md`)
- `.agent/collaboration/AUDIT_WOT-*.md` - criterios de auditoria (si existe; legacy-compat: `AUDIT_WP-*.md`, `AUDIT_WT-*.md`)
- `.agent/runtime/memory/observations.jsonl` - memoria acumulada (ultimas 20 entradas)

### Fase 2: Identificar gaps

Documentar explicitamente:
- Que informacion falta para tomar decisiones informadas.
- Que archivos o modulos necesitan exploracion adicional.
- Que decisiones arquitectonicas requieren validacion externa.
- Riesgos conocidos no mitigados.

### Fase 3: Buscar fuentes

Si hay MCP GitHub disponible:
- Usar `mcp__github__search_code` para buscar patrones en repositorios externos.
- Usar `mcp__github__get_file_contents` para leer archivos especificos.
- Limitar a 8-12 archivos × 500 lineas por archivo (cap operativo).

Si no hay MCP:
- Documentar fuentes locales disponibles.
- Marcar busquedas externas como tarea humana pendiente.

### Fase 4: Producir resumen estructurado

El output debe seguir la plantilla en `references/research-template.md` con las secciones:
- `## Contexto` - resumen del estado actual
- `## Gaps` - informacion faltante o ambigua
- `## Fuentes` - referencias verificadas (locales o GitHub)
- `## Recomendacion` - accion inmediata sugerida

## Output path

El output se persiste en:
```
.agent/runtime/research/<topic>-<YYYY-MM-DD>.md
```

Este path esta excluido de git en `.gitignore`. No commitear investigaciones generadas.

## Constraints

- **Skill PURA**: no crear ningun `.py` bajo `skills/deep-research/`. El agente invocador usa sus propias herramientas.
- **No inventar**: si no puedes verificar algo, escribe `[NO VERIFICADO]` o `[NO ENCONTRADO]`.
- **Cap operativo**: maximo 12 archivos externos leidos. Contar invocaciones de herramientas de lectura.
- **Output gitignored**: `.agent/runtime/research/` esta en `.gitignore`. No commitear investigaciones.

## References

- `references/research-template.md` - Plantilla de output estructurado con secciones fijas.

## Troubleshooting

**P: ¿Que si MCP GitHub no esta disponible?**
R: Documentar en el output la limitacion. Usar fuentes locales. Marcar busquedas externas como tarea humana pendiente.

**P: ¿Que si el contexto base esta desactualizado?**
R: Notificar en la seccion `Gaps` que `PROJECT.md` o `AUDIT.md` requieren actualizacion antes de continuar.

**P: ¿Que si la investigacion revela que el WP ya existe?**
R: Documentar en `Recomendacion` que no es necesario abrir nuevo ticket y citar el WP existente.

## Example usage

```bash
# Usuario activa la skill
/deep-research topic="ECC capability pack"

# El agente ejecuta:
# FASE 1: Lee PROJECT.md, work_plan.md, execution_log.md, observations.jsonl
# FASE 2: Identifica gaps (ej. "no hay skill de investigacion previa")
# FASE 3: Busca fuentes (MCP GitHub si disponible, sino solo locales)
# FASE 4: Produce .agent/runtime/research/ecc-capability-2026-05-27.md
```
