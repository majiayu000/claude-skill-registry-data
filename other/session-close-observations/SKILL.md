---
name: session-close-observations
version: 2.0.0
description: Genera observaciones curadas al final de una sesion para la memoria auto-mejorable, que luego se filtran y pueden promoverse a observations.jsonl. Usar cuando se completa un WP, se cierra una sesion larga o se descubre un patron o una decision arquitectonica. No usar para consolidar la memoria (ver memory-consolidate).
triggers: [/session-close, /close-observations, /generate-observations]
author: agent
role: shared
stage: close
cycle_phase: [F7-cierre-sesion]
writes_memory: true
quality_gate: false
tags: [core, system, memory]
---

# session-close-observations

Skill compartida para convertir lo aprendido al final de cada ciclo en observaciones curadas y reutilizables. El sistema mejora con las ejecuciones sin mezclar memoria viva con ruido operativo.

## Overview

Esta skill es invocada por Builder, Manager o Supervisor al cerrar una sesion para generar observaciones candidatas que seran filtradas y potencialmente promovidas a `observations.jsonl`.

### Cuando activar

- Al finalizar un WP (Work Plan) completado
- Al cerrar una sesion de trabajo larga (>2 horas)
- Cuando hay decisiones arquitectonicas o patrones descubiertos
- Antes de ejecutar `memory-consolidate` (Paso 9e de `project-finalize`; esta skill es el Paso 9d,
  prerequisito de 9e)

### Cuando NO activar

- Durante implementacion activa de un WP
- Si no hay eventos significativos que registrar
- En sesiones cortas de mantenimiento rutinario

## Workflow

### Paso 1: Recopilar eventos del ciclo

Identificar eventos significativos del ciclo actual:
- Decisiones arquitectonicas tomadas
- Convenciones establecidas o modificadas
- Patrones de codigo descubiertos
- Hechos tecnicos relevantes (bugs fijos, optimizaciones)
- Cambios en la estructura del proyecto

Fuentes tipicas:
- `execution_log.md` - registro de implementacion
- `.agent/collaboration/work_plan.md` - plan completado
- Commits recientes del repositorio
- Cambios en archivos de configuracion

### Paso 2: Generar observaciones candidatas

Para cada evento significativo, crear una observacion con el schema base:

```json
{
  "timestamp": "2026-05-25T12:00:00Z",
  "signal": "Descripcion clara y concisa del hecho",
  "category": "convention|decision|fact|pattern",
  "source_ticket": "WOT-2026-XXX",
  "topic": "tema principal",
  "source": "session-close"
}
```

### Paso 3: Aplicar filtros de curacion

Cada observacion candidata debe pasar tres reglas:

1. **Es un hecho**: Debe ser verificable y objetivo, no una opinion
2. **Sobrevive a otra sesion**: Debe ser util dentro de 1+ semanas
3. **Evita trabajo repetido**: No debe duplicar observaciones existentes

Filtros de exclusion automatica:
- Opiniones subjetivas ("me parece que...", "deberiamos...")
- Contexto efimero (traces de herramientas, logs temporales)
- Duplicados exactos o semanticamente equivalentes
- Entradas < 30 caracteres

### Paso 4: Escribir observaciones validadas

Las observaciones que pasan los filtros se appendean a:
- `.agent/runtime/memory/observations.jsonl`

Formato: una linea JSON por observacion, encoding UTF-8.

### Paso 5: Reportar resultado

Generar un resumen de cierre:
- Total de observaciones generadas
- Cuantas pasaron los filtros
- Cuantas fueron descartadas y por que
- Topics cubiertos en este ciclo

### Paso 6: Transferir al cierre de sesion del Manager

Cuando el cierre de observaciones detecte learnings que tambien deben clasificarse por alcance:
- referenciar `manager-session-closeout`
- pasar el contexto curado al siguiente paso de cierre
- evitar mezclar la memoria tecnica con el canal de salida humana del motor

## Schema de Observacion

| Campo | Tipo | Requerido | Descripcion |
|-------|------|-----------|-------------|
| `timestamp` | ISO 8601 | SI | Fecha/hora UTC de la observacion |
| `signal` | string | SI | Descripcion clara del hecho (min 30 chars) |
| `category` | enum | SI | `convention`, `decision`, `fact`, `pattern` |
| `source_ticket` | string | SI | WP-ID o referencia al origen |
| `topic` | string | SI | Tema principal para agrupacion |
| `source` | string | SI | Origen: `session-close`, `builder`, `manager`, etc. |

### Categorias validas

- **convention**: Convenciones de codigo, nombres, estructura
- **decision**: Decisiones arquitectonicas o de diseño
- **fact**: Hechos tecnicos verificables
- **pattern**: Patrones de diseño o implementacion

## Output Format

La skill no tiene output directo en stdout. Su efecto es:
- Append de observaciones a `observations.jsonl`
- Reporte opcional en `.agent/runtime/memory/session_close_report.md`

## References

- `references/schema.md` - Detalle del schema de observaciones
- `references/filter-rules.md` - Reglas de filtrado y curacion
- `../memory-consolidate/SKILL.md` - Consolidacion posterior
- `../project-finalize/SKILL.md` - Integracion en cierre de proyecto
- `../manager-session-closeout/SKILL.md` - Clasificacion de learnings de cierre y puente humano

## Constraints

- **NO** reemplaza `memory-consolidate`: solo genera candidatas
- **NO** escribe en `MEMORY.md` directamente: eso lo hace consolidate
- **NO** usa LLM para sintesis: filtrado deterministico
- **SIEMPRE** valida schema antes de appendear
- **SIEMPRE** pasa filtros de curacion

## Integration

Esta skill (`session_close_observations.py`) ES el Paso 9d de `project-finalize`, entre:
- Paso 9c: `local_audit.py` (snapshot de auditoria) — anterior
- Paso 9e: `memory_consolidate.py` (consolidacion de memoria) — posterior, depende de este 9d

Comandos tipicos:
```bash
# Modo ticket: extrae candidatos automaticos del work_plan.md activo
python scripts/session_close_observations.py --ticket WOT-2026-XXX

# Modo candidates: inyecta candidatos semanticos desde archivo JSON externo
python scripts/session_close_observations.py --candidates candidates.json

# Dry-run para previsualizar sin escribir
python scripts/session_close_observations.py --ticket WOT-2026-XXX --dry-run --verbose
```

**Nota de exclusion mutua:** `--ticket` y `--candidates` son mutuamente excluyentes.
Argparse impone que exactamente una de las dos flags debe estar presente por ejecucion.
No es posible usar ambas simultaneamente ni omitir las dos.

**Workflow con --candidates:**
1. El agente/LLM construye un archivo JSON con candidatos semanticamente ricos
2. Cada candidato debe seguir el schema de observacion (timestamp, signal, category, etc.)
3. El script valida schema, aplica filtros de curacion y chequea duplicados
4. Las observaciones validas se appendean a `observations.jsonl`

## Related Skills

- `memory-consolidate`: Dedupe + filter + archive observations
- `project-finalize`: Orquesta cierre profesional
- `local-audit`: Genera snapshot del estado del repo
