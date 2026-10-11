---
name: builder-write-deliverable
version: 2.0.0
description: Generar un deliverable markdown (no codigo) a partir de su descripcion, output_path y acceptance criteria del work_plan. Usar cuando el ticket es documental y el ciclo no debe invocar ruff ni pytest. No usar para implementar codigo (ver builder-implement-from-plan).
triggers: [/write-deliverable, /deliverable, /write-doc]
author: agent
role: builder
stage: implement
cycle_phase: [F5-implementacion]
writes_memory: false
quality_gate: false
tags: [core, system]
---

# builder-write-deliverable

Skill genérica para producir deliverables markdown. Pensada como prueba de
que el bus puede operar tareas no-código sin tocar el engine.

## Cuándo usar

- Cuando el work_plan pide un deliverable de tipo markdown / texto / informe.
- Cuando el ciclo del bus debe ejecutarse sin invocar ruff/pytest.

## Workflow

1. Leer `Deliverable.description`, `Deliverable.output_path`, `Deliverable.acceptance_criteria` del work_plan.
2. Generar el contenido pedido (idioma, longitud y estructura según el acceptance).
3. Escribir el archivo en `output_path` usando `pathlib`.
4. Verificar que cumple cada acceptance criterion antes de declarar completado.

## Constraints

- NO escribir código Python como parte del deliverable salvo que el acceptance lo pida.
- NO invocar ruff/pytest sobre el deliverable.
- Si el acceptance pide un word count, contar palabras de forma determinista (split por whitespace).

## Triggers no colisionan

Validado contra `python scripts/check_skill_collisions.py` antes de mergear.
