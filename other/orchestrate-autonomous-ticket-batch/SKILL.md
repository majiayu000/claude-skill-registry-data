---
name: orchestrate-autonomous-ticket-batch
version: 1.0.0
description: Ejecutor autonomo que consume el DAG de backlog-triage y cierra el maximo de tickets con barreras duras por ticket, delegando cada uno en el pipeline canonico del modo detectado; crea commits, mueve filas al archivo, escribe bus, ledger y memoria, puede publicar con push y nunca se audita a si mismo. Usar cuando hay un triage con DAG validado y fresco y un tercero ha resuelto el recibo de aislamiento de arranque. No usar para un pipeline por ticket (ver orchestrate-pipeline, orchestrate-pipeline-codeonly), para producir el DAG (ver backlog-triage) ni para auditar el batch (ver audit-autonomous-ticket-batch); nunca ejecuta tickets REQUIERE_HUMANO ni DISENO_PRIMERO.
triggers: [/orchestrate-autonomous-ticket-batch, orchestrate-autonomous-ticket-batch, batch-autonomo-de-tickets]
author: agent
role: orchestrator
stage: meta
writes_memory: false
quality_gate: false
tags: [core, system, orchestration, autonomy, batch]
source_prompt: prompts/orchestrator_autonomous_ticket_batch.md
contract_id: cid-orchestrator-autonomous-ticket-batch-v1
---

# orchestrate-autonomous-ticket-batch

Skill para ejecutar el BATCH AUTONOMO de tickets: consume el DAG de grupos
emitido por `/backlog-triage` (schema `autonomous-batch-dag/v1`) y cierra el
mayor numero de tickets posible **con garantias**.

NO reimplementa el metodo. El flujo completo (deteccion de modo y delegacion,
maquina de estados con ruteo al owner-stage, causas de parada dura,
`GROUP_STOP_REPORT`, regla de contencion, las 8 barreras no negociables por
ticket y las salidas de la corrida) vive en
`prompts/orchestrator_autonomous_ticket_batch.md`. **El prompt es la fuente de
verdad; si algo diverge, prevalece el prompt.**

## La garantia no es opcional: el auditor es la pieza hermana

Un ejecutor sin su auditoria es autonomia sin garantia, es decir auto-reporte,
y `prompts/audit_agent_output.md` (CEM v0) lo prohibe. Toda corrida de esta
skill se audita despues con `/audit-autonomous-ticket-batch`
(`prompts/audit_autonomous_ticket_batch.md`), **en fresh-context y por un
agente que NO sea el que ejecuto el batch**. El ejecutor no puede auditarse a
si mismo.

## Start Context Isolation receipt (WOT-2026-044r)

El recibo de aislamiento de contexto (`start_context_isolation.json`) es
obligatorio ANTES de tocar tickets. Verifica:
- `status: RESOLVED` (no PENDING/UNRESOLVED)
- `prompt_sha256` contra el fichero de arranque REALMENTE consumido
- `project_root_resolved` contra el destino de la topologia
- `scope` contra los tickets del DAG
- `approved_by` = actor EXTERNO al ejecutor (nunca auto-certificacion)

El auditor hermano (`audit_autonomous_ticket_batch.md`) tambien verifica este
recibo (seccion 4.bis). Paridad de los tres canales: ejecutor, auditor y skill
declaran el mismo requisito.

## Cuando usarla

- Hay varios tickets `APTO_AUTONOMO` ya clasificados por `/backlog-triage`, y
  ese triage emitio el DAG de grupos (`autonomous-batch-dag/v1`), validado con
  `scripts/validate_batch_dag.py`.
- Se quiere cerrar una tanda sin intervencion humana por ticket, aceptando que
  las barreras PARAN la corrida cuando no dan verde (parar limpio es su
  funcion, no su fallo).

## Cuando NO usarla

- Tickets `REQUIERE_HUMANO` o `DISENO_PRIMERO`: **jamas** entran en el batch.
- Sin DAG validado: sin schema congelado, el ejecutor no tiene contrato de
  datos. Corre `/backlog-triage` primero.
- Un solo ticket: usa el pipeline por ticket directamente
  (`/orchestrate-pipeline` o `/orchestrate-pipeline-codeonly` segun el modo).

## Restriccion dura

- El ejecutor **NUNCA reclasifica** un ticket (`class` / `autonomy_mode` los
  asigna el TRIAGE). Reclasificar para esquivar un gate es `falso_verde`.
- El ejecutor **jamas escribe** backlog, informes, follow-ups ni ledger en
  `repo_motor`: van al destino-rol.
- Tier 2 y Tier 3 **no estan implementados**. No los improvises.
