---
name: portal-code-review
description: Review pull requests for the Portal Centralizado de Datos Financieros with project checklists — root AGENTS.md NON-NEGOTIABLE rules, QA gate, traceability to User Stories, and frequent project risks. Use when reviewing PRs before merging to develop or main.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal Code Review Skill

## Rules — NON-NEGOTIABLE (del AGENTS.md raíz)

- Idioma: código (identificadores, comentarios, docstrings Google-style) en inglés; prosa visible al lector (UI, docs) en español neutro. UI SOLO en español (no hay i18n).
- Sin emojis en código, comentarios, prints, commits ni logs.
- Logging con `structlog.get_logger()`, nunca `print()`.
- Type hints obligatorios en todo Python.
- SoC: router recibe → service procesa → model persiste; tools ADK en `ml/agent/tools/`; sin lógica de negocio en routers ni componentes Vue.
- DRY: función usada 2+ veces → `backend/app/utils/`, `ml/utils/` o `frontend/app/composables/`.

## Checklist Universal

- [ ] Rama `feature/E{epic}-US-XXX-{slug}` y Conventional Commit con scope de épica (`feat(E2): ...`)
- [ ] PR referencia la US del plan (`context/planeacion_proyecto.md`); si toca US absorbida del backlog consolidado (§18), la cita
- [ ] `make check` limpio (lint + secrets-scan)
- [ ] Cobertura mantenida: ≥70% backend, ≥50% frontend
- [ ] Sin trailer `Co-Authored-By` de asistentes IA en commits
- [ ] Sin secretos hardcodeados; sin binarios >1 MB en git

## QA Gate por área tocada

| Si el PR toca... | Exigir |
|-------------------|--------|
| Schema de BD | Migración dbmate incluida (`db/migrations/*.sql` con `-- migrate:up/down`), `schema.sql` actualizado; jamás `create_all()` |
| Auth/permisos | Pruebas 401/403 parametrizadas por rol en verde; matriz en `docs/security.md` actualizada (skill `portal-security-audit`) |
| Chat/agente | Evento `tool_call` emitido ANTES del texto; cancelación sin tareas colgadas; toda cifra proviene de un tool call |
| Capa semántica | Consulta estructurada Pydantic + compilador determinístico; el LLM/cliente jamás aporta Polars/SQL libre; 422 con fuzzy match |
| Infra/CI | Checklist de `portal-terraform-gcp` + `portal-finops` (scale-to-zero, secrets, lifecycle) |
| Entregable UX | Checklist de la actividad contra la rúbrica (A1: §24 del plan) |

## Riesgos frecuentes del proyecto — buscar activamente

### 1. Bloqueo del event loop con Polars síncrono

```python
# MAL — bloquea todas las requests concurrentes
async def read_silo(silo: str) -> pl.DataFrame:
    return pl.read_parquet(f"data/silos/{silo}.parquet")

# BIEN — delegado a threadpool
async def read_silo(silo: str) -> pl.DataFrame:
    return await asyncio.to_thread(pl.read_parquet, f"data/silos/{silo}.parquet")
```

Grep de sospecha: `grep -rn "pl.read_\|\.collect()" backend/app/ ml/data/ | grep -v to_thread`.

### 2. Reactividad profunda sobre payloads masivos (Nuxt 4)

```typescript
// MAL — ref() profundo sobre 1M de puntos congela la UI
const { data } = await useFetch('/api/liquidez', { deep: true })

// BIEN — shallowRef default de Nuxt 4; ECharts recibe el objeto plano
const { data } = await useFetch('/api/liquidez')   // no forzar deep: true
```

Revisar también: componentes pesados con prefijo `Lazy*`, agregación server-side antes de graficar (degradación acordada: 500 K).

### 3. Cifras sin tool call en el agente (R07)

Toda cifra en una respuesta del agente debe provenir de un tool call gobernado y citar la fuente del catálogo. Rechazar prompts/parsers que permitan al LLM inventar números u omitir la cita; sin tool call no se muestran números.

### Otros a vigilar

- Endpoints nuevos sin `Security(scopes=...)` (bloqueo inmediato).
- `SessionService`/generadores SSE sin cleanup en cancelación.
- Contraseñas o prompts crudos en logs (solo `llm.prompt_hash`).
- Reactivación de descartados: fastapi-users, Alembic, Redis, refresh tokens, i18n, EPICs 6–11.

## Decision Tree

```
PR toca codigo      -> checklist universal + reglas AGENTS.md
PR toca schema      -> + fila "Schema de BD"
PR toca auth        -> + fila "Auth/permisos" + portal-security-audit
PR toca chat/agente -> + fila "Chat/agente" (tarjeta tool_call antes del texto)
PR toca frontend    -> + riesgo 2 (reactividad) + estados skeleton/vacio/error
PR toca infra/CI    -> + fila "Infra/CI" + portal-finops
PR es entregable UX -> + rubrica de la actividad (regla de oro: UX gana)
```

## Veredicto del review

- **Aprobar**: checklist completo, riesgos revisados, CI verde.
- **Solicitar cambios**: cualquier NON-NEGOTIABLE violado o QA gate incompleto — citar la regla exacta y el archivo:línea.
- **Comentar**: sugerencias de estilo/simplificación que no bloquean.
