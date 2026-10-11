---
name: audit-autonomous-ticket-batch
version: 1.0.0
description: Auditoria aislada (contexto fresco, solo lectura) de un batch autonomo de tickets ya cerrado o parado, que re-deriva el PREDICATE de 8 condiciones comando a comando, audita las paradas y la recuperacion del ejecutor y propone, sin ejecutarlo, el cierre de sesion. Usar cuando un batch de orchestrate-autonomous-ticket-batch ha terminado o se ha detenido, ya no le quedan grupos ejecutables y existe su batch_run. No usar para auditar una cadena ticket a ticket (ver audit-pipeline, audit-pipeline-codeonly) ni desde el mismo agente que ejecuto el batch.
triggers: [/audit-autonomous-ticket-batch, audit-autonomous-ticket-batch, auditar-batch-autonomo]
author: agent
role: auditor
stage: review
writes_memory: false
quality_gate: false
tags: [core, system, audit, autonomy, isolation]
source_prompt: prompts/audit_autonomous_ticket_batch.md
contract_id: cid-audit-autonomous-ticket-batch-v1
---

# audit-autonomous-ticket-batch

Skill para auditar, con AISLAMIENTO fresh-context obligatorio, una corrida del
batch autonomo de tickets ejecutado por `orchestrate-autonomous-ticket-batch`
(`prompts/orchestrator_autonomous_ticket_batch.md`).

Es la pieza simetrica obligatoria de ese ejecutor: sin esta auditoria, la
autonomia del batch es auto-reporte, y `prompts/audit_agent_output.md` (CEM
v0) lo prohibe explicitamente. NO reimplementa el metodo: el flujo completo
(regla de aislamiento, herencia de las cuatro auditorias base, capa propia de
8 puntos, PREDICATE de 8 condiciones, propuesta de cierre) vive en
`prompts/audit_autonomous_ticket_batch.md`, que a su vez hereda de
`prompts/audit_agent_output.md`, `prompts/manager_review.md`,
`prompts/audit_pipeline.md` / `prompts/audit_pipeline_codeonly.md` (segun
modo) y `prompts/audit_goal_completion.md`. **El prompt es la fuente de
verdad; si algo diverge, prevalece el prompt.**

## Regla de aislamiento (antes de invocar esta skill)

**El agente que EJECUTO el batch no puede invocar esta skill sobre su propia
corrida.** Se requiere: (a) modelo distinto del ejecutor, o (b) sub-agente en
fresh-context sin el transcript de la sesion ejecutora. Sin una de las dos,
cualquier veredicto emitido es invalido: no lo trates como auditoria valida
aunque el texto tenga forma de informe.

Es **read-only sobre el sistema auditado**: no reabre tickets, no toca el
DAG-JSON, backlog, bloques de cierre, codigo ni estado operativo del batch.
Solo escribe sus propios dos artefactos de auditoria y una propuesta de
cierre para el humano/Manager.

## Cuando usarla

- Justo despues de que una corrida de `/orchestrate-autonomous-ticket-batch`
  termine (todos los grupos alcanzables cerrados, congelados o agotados por
  presupuesto).
- Antes de aceptar como valido cualquier `batch_run_<ts>.json` que declare la
  corrida `DONE`.
- Antes de alimentar `orchestrator_session_close_full_audit.md` con la
  propuesta de cierre de un batch.

## Cuando NO usarla

- Para auditar UN ticket individual fuera de un batch (usar
  `manager-review-implementation` o `audit-pipeline`/`audit-pipeline-codeonly`
  segun modo).
- Para conducir la ejecucion del batch (usar
  `orchestrate-autonomous-ticket-batch`).
- Para decidir el DAG de grupos (usar `backlog-triage`, read-only, anterior
  al batch).
- Si el agente invocandola es el mismo que ejecuto el batch en el mismo
  contexto: eso viola el aislamiento y el resultado no cuenta.

## Prompt canonico

Leer y aplicar integramente:

- `prompts/audit_autonomous_ticket_batch.md`

Ese prompt es la fuente de verdad. Hereda filosofia de
`prompts/audit_agent_output.md`, mecanica de review de
`prompts/manager_review.md`, base de meta-auditoria de cadena de
`prompts/audit_pipeline.md` o `prompts/audit_pipeline_codeonly.md` segun el
modo detectado (`is_motor_code_only()`), y el patron de aislamiento de
`prompts/audit_goal_completion.md`. Si algo diverge, prevalece
`prompts/audit_autonomous_ticket_batch.md`.

## Deteccion de modo (obligatoria antes de auditar)

```
from runtime.project_root import is_motor_code_only
```

`True` -> hereda `audit_pipeline_codeonly.md` como base de cadena. `False` ->
hereda `audit_pipeline.md`. Resuelve tambien el vinculo motor<->destino con
`resolve_motor_link(project_root)` (`from scripts.destination_context import
resolve_motor_link`). No asumas una topologia fija: enumera los repos desde
la resolucion real.

## La capa propia del batch (8 puntos, exclusivos de esta auditoria)

1. Decisiones de PARADA (ruido, o continuo donde debia parar?).
2. Exclusiones duras (se disparo la que debia? alguna se colo sin disparar?).
3. Recovery loops (enfoque distinto cada reintento, o bucle disfrazado?).
4. Checkpoints de confianza (4 condiciones cumplidas, o "verde" sin auditar
   la fila?).
5. Contencion (el fallo de un grupo se propago a un grupo independiente?).
6. Autoridad (el ejecutor reclasifico algun ticket? prohibido).
7. Portabilidad (la corrida asumio una topologia de dogfooding?).
8. `objetivo_huerfano` (herencia de `audit_goal_completion.md`): ticket verde
   con objetivo real incumplido.

## PREDICATE (8 condiciones, comando a comando)

`schema_valido`, `dag_aciclico`, `contabilidad_completa`, `cierres_auditables`,
`suite_final_verde`, `auditor_emitido`, `arboles_limpios`,
`estado_operativo_valido`. Detalle completo,
comandos exactos y formato de salida en
`prompts/audit_autonomous_ticket_batch.md` seccion 4.

## Start Context Isolation receipt (WOT-2026-044r)

El auditor tambien verifica el recibo de aislamiento de contexto
(`start_context_isolation.json`), que vive FUERA del bloque PREDICATE
(campo top-level del `batch_run_<ts>.json`). Verifica:
- `status: RESOLVED` (no PENDING/UNRESOLVED)
- `prompt_sha256` contra el fichero de arranque consumido
- `project_root_resolved` contra el destino de la topologia
- `scope` contra los tickets del DAG
- `approved_by` = actor EXTERNO al ejecutor (nunca autocertificacion)

Detalle en `prompts/audit_autonomous_ticket_batch.md` seccion 4.bis.

## Herramientas por fase

| Fase | Rol | Prompts | Scripts / comandos |
|---|---|---|---|
| Deteccion de modo | Auditor | `prompts/audit_autonomous_ticket_batch.md` | `is_motor_code_only()`, `resolve_motor_link()` |
| PREDICATE | Auditor | `prompts/audit_autonomous_ticket_batch.md` | `scripts/validate_batch_dag.py`, `scripts/check_backlog_commits_landed.py`, `scripts/run_pytest_safe.py` (leer output real, no exit del wrapper) |
| Capa propia (8 puntos) | Auditor | `prompts/audit_autonomous_ticket_batch.md`, `prompts/audit_goal_completion.md` | learning ledger (`manifest.jsonl`), `GROUP_STOP_REPORT`s, DAG-JSON original |
| Por ticket A/B | Auditor | `prompts/audit_agent_output.md`, `prompts/manager_review.md`, `prompts/audit_pipeline.md`/`prompts/audit_pipeline_codeonly.md` | `git show --stat`, `ruff check`, tests focales, `scripts/check_encoding_guard.py` |
| Informe + propuesta de cierre | Auditor | `prompts/audit_autonomous_ticket_batch.md` | `scripts/check_encoding_guard.py` sobre el informe |

## Salidas

- `<destino-rol>/orchestrator_pipeline/reports/audit_autonomous_batch_<timestamp>.md`
- `<destino-rol>/orchestrator_pipeline/reports/audit_autonomous_batch_<timestamp>.json`

Estructura detallada de ambos en `prompts/audit_autonomous_ticket_batch.md`.

## La propuesta de cierre NO es el cierre

El informe pre-rellena los bloques de
`prompts/orchestrator_session_close_full_audit.md` (salud del sistema,
adversarial sobre los N commits, `suite_optimization.md` sobre el
`run_history.jsonl` acumulado, `audit_git_publication.md` si hubo push,
memoria, follow-ups) pero **el batch nunca cierra la sesion por su cuenta**:
esa decision es del humano/Manager, dado el alto blast radius de tocar
memoria y backlog.

## Restriccion dura

- No emite veredicto sin aislamiento (B1) y read-only (B3) confirmados.
- No reabre tickets ni modifica el DAG-JSON, backlog, bloques de cierre,
  codigo ni estado operativo.
- No repara nada que encuentre roto: solo reporta.
- No ejecuta `--session-close` ni ninguna accion de cierre de sesion.
- No hardcodea un numero fijo de repos: enumera desde la topologia resuelta.
- La skill es puntero: no redeclara el metodo. Remite al prompt.

La reapertura de tickets, la adopcion de mejoras o el cierre de sesion los
decide el humano/Manager leyendo el informe.
