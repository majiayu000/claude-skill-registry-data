---
name: builder-run-quality-gates
version: 2.0.0
description: Ejecutar los quality gates que corresponden al deliverable_type del work_plan activo mediante run_gates_dispatch.py. Usar cuando el Builder termino un cambio sustancial y necesita validarlo antes de pedir review. No usar para autorizar el handoff, porque un exit 0 no autoriza BUILDER_EXIT ni READY_FOR_REVIEW (ver builder-self-audit).
triggers: [/gates, quality-gates, /check]
author: agent
role: builder
stage: quality
cycle_phase: [F5-implementacion]
writes_memory: false
quality_gate: true
tags: [core, system]
---

# builder-run-quality-gates

Skill para ejecutar la batería de gates correspondiente al tipo de deliverable del WP activo. Dispatchea automáticamente — el agente solo invoca el wrapper.

## Cuándo usar
- Durante la implementación, tras cada cambio sustancial.
- Como paso previo (necesario, NO suficiente) al cierre canónico.

## Workflow

1. Ejecuta `python scripts/run_gates_dispatch.py`.
2. Si exit code != 0: lee el output, corrige, vuelve a ejecutar.
3. Si exit code == 0: los gates de este dispatcher están pasados. Eso **no**
   autoriza `BUILDER_EXIT` ni `READY_FOR_REVIEW` por sí solo.

## Este gate no autoriza el handoff

Un exit code 0 de este dispatcher es evidencia de loop rápido, no de cierre. La
distinción canónica (loop rápido vs cierre canónico) y los requisitos reales del
handoff — suite canónica con `tested_commit_sha == HEAD`, `validate` 0/0, y los
eventos `BUILDER_EXIT` + `STATE_CHANGED` emitidos por `--mark-ready` — los define
el prompt canónico, no esta skill:

- `prompts/orchestrator_launch_builder.md`, secciones "Gates focales (loop rapido
  - NO autorizan handoff)" y "Loop rapido vs cierre canonico (politica
  WOT-2026-011g)" (`cid-bui-implement-v1`).

Si esta skill y el prompt divergen, prevalece el prompt.

## Dispatch table (informativo — secuencia real de `run_code_gates()` en `scripts/run_gates_dispatch.py`)

| deliverable_type | Gates ejecutados |
|---|---|
| code | `ruff check .` -> `ruff format --check .` -> `run_pytest_safe.py --level all` (si hay tests locales) -> `pip_audit_project.py` (condicional por politica) |
| mixed | code gates + deliverable existence check |
| documentation | deliverable existence check |
| research | deliverable existence check |
| analysis | deliverable existence check |
| (missing) | fallback a code + warning |

## Constraints

- NO saltar el dispatcher invocando ruff/pytest manualmente.
- NO modificar el dispatcher por WP — usa el wrapper.
