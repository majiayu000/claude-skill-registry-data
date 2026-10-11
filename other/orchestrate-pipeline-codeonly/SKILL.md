---
name: orchestrate-pipeline-codeonly
version: 1.0.0
description: Pipeline multi-ticket del motor en CODE-ONLY MODE que muta codigo en la worktree _dev, con work_plan, STRATEGY y AUDIT por ticket, dos revisiones (la segunda en contexto fresco) y cierre por commit directo sin bus. Usar cuando el ticket tiene delivery_authority repo_motor, se trabaja en la worktree _dev y el motor esta en CODE-ONLY MODE; el push va agrupado al final y con autorizacion explicita. No usar para el pipeline canonico con bus vivo (ver orchestrate-pipeline), para decidir que pipeline lanzar (ver backlog-triage) ni para auditar la cadena cerrada (ver audit-pipeline-codeonly).
triggers: [/orchestrate-pipeline-codeonly, orchestrate-pipeline-codeonly, pipeline-codeonly]
author: agent
role: manager
stage: implement
writes_memory: false
quality_gate: true
tags: [core, system, pipeline, codeonly, dogfooding]
source_prompt: prompts/orchestrator_pipeline_codeonly.md
contract_id: cid-orchestrator-pipeline-codeonly-v1
---

# orchestrate-pipeline-codeonly

Skill para conducir un pipeline de tickets del MOTOR cuando este esta en
**CODE-ONLY MODE**: se trabaja en la worktree `_dev`, no hay destino externo
montado, el bus esta bloqueado y el cierre de cada ticket es **commit-directo**
(git es el registro; el ID va en el mensaje del commit).

Es la variante especializada de `orchestrate-pipeline` para el dogfooding del
propio motor. NO reimplementa el metodo: el flujo completo (preflight, flujo por
ticket, cierre de cadena, riesgos codificados) vive en
`prompts/orchestrator_pipeline_codeonly.md`. **El prompt es la fuente de verdad;
si algo diverge, prevalece el prompt.**

## Cuando usarla

Las TRES condiciones a la vez (si falta una, NO es este pipeline):

- `delivery_authority: repo_motor` (el ticket entrega codigo del motor);
- se trabaja en la worktree **`_dev`** (rama `main`), no en el principal (detached)
  ni en el workspace (backlog);
- **CODE-ONLY MODE**: sin destino externo -> el bus esta bloqueado
  (`--session-close`/`--bootstrap-ticket`/`--mark-ready` dan
  `[ERROR] Motor code-only mode`).

## Cuando NO usarla

- Si el motor SI tiene destino externo montado (bus vivo): usar
  `orchestrate-pipeline` canonico (`prompts/orchestrator_pipeline.md`).
- Para decidir QUE pipeline lanzar (usar `backlog-triage`, read-only).
- Para auditar un pipeline ya cerrado (usar `audit-pipeline`, read-only).
- Para un `repo_destino` generico (ese es el flujo canonico con bus).

## Preflight (recolector, obligatorio)

Antes de tocar nada, correr el recolector determinista
`scripts/preflight_codeonly_pipeline.py` (SHAs de los 3 repos + validate + guard de
topologia + barrera "0 consumidores runtime" del token a retirar). Es un TESTIGO
read-only: reporta senales, el agente juzga. Detalle en el prompt (Paso 0).

## Workflow

El metodo (preflight, flujo por ticket, cierre de cadena, riesgos codificados) vive
INTEGRO en `prompts/orchestrator_pipeline_codeonly.md`. Esta skill no lo redeclara:
lee ese prompt y ejecutalo. Si algo diverge, prevalece el prompt.

## Restriccion dura

- SOLO `repo_motor` + `_dev` + code-only. Cierre commit-directo, sin bus.
- La skill es puntero: no redeclara el metodo. Remite al prompt.
