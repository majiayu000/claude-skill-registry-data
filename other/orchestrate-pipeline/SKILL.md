---
name: orchestrate-pipeline
version: 1.0.0
description: Coordinar por chat un pipeline multi-ticket en repo_destino usando Manager, Builder, reviews y cierre canonico. Usar cuando se orquesta el pipeline por-ticket en modo destino con bus vivo (bootstrap -> builder -> review -> cierre por bus). No usar para el modo motor code-only (ver orchestrator_pipeline_codeonly.md) ni para el ejecutor de batch autonomo (ver orchestrator_autonomous_ticket_batch.md) ni para el bootstrap de sesion.
triggers: [/pipeline, orchestrate-pipeline, run-backlog, ejecutar-backlog, implantar-planes]
author: agent
role: orchestrator
stage: meta
writes_memory: false
quality_gate: false
tags: [core, system, chat-flow]
source_prompt: prompts/orchestrator_pipeline.md
contract_id: cid-orchestrator-pipeline-v1
---

# orchestrate-pipeline

Skill para conducir por chat la implantacion de tickets desde un `repo_destino`
usando el motor externo `orquestador_de_agentes`.

Esta skill no sustituye al bus ni al supervisor terminal-driven. Es el contrato
operativo para coordinar Manager y Builder por chat cuando el usuario quiere
implantar planes desde backlog con supervision humana.

## Cuando usarla

Usar cuando el usuario pida:

- ejecutar o implantar tickets desde `backlog.md`;
- coordinar Manager y Builder por chat;
- avanzar una serie de planes en un `repo_destino`;
- operar un pipeline multi-ticket sin lanzar el supervisor completo;
- auditar y cerrar tickets dependientes en secuencia.

No usar para:

- implementar un unico ticket ya arrancado como Builder;
- revisar un diff puntual como Manager;
- cerrar una sesion completa ya terminada;
- reparar el runtime del bus sin ticket o plan explicito.

## Prompt canonico

Leer y aplicar:

- `prompts/orchestrator_pipeline.md`
- `references/destination-preflight.md`

Ese prompt es la fuente de verdad de este flujo. Esta skill es un wrapper
operativo y un mapa de herramientas; si alguna instruccion diverge, prevalece
`prompts/orchestrator_pipeline.md`.

## Topologia obligatoria

Antes de operar, confirmar:

- `repo_destino`: cwd del proyecto destino.
- `MOTOR_ROOT`: ruta absoluta del motor desde `.agent/config/motor_destination_link.json`.
- `AGENT_PROJECT_ROOT`: debe apuntar al `repo_destino`.
- Ticket activo, bus y proyecciones en `.agent/collaboration/`.

El estado operativo vive en `repo_destino`. Las operaciones git se ejecutan en
el repo que contiene los archivos modificados.

En comandos del motor, resolver siempre rutas contra `MOTOR_ROOT`; no asumir que
`agent_controller.py`, scripts o prompts existen en el cwd del `repo_destino`.

Durante pipelines de destino, tratar `repo_motor` como read-only salvo ticket
explicito. La barrera portable es `scripts/check_motor_pristine.py`: detectar
siempre, restaurar nunca automaticamente.

## Preflight del destino

Antes de arrancar cualquier ticket, aplicar
`references/destination-preflight.md`.

Si el preflight devuelve:

- `READY`: continuar.
- `NEEDS_RECONCILE`: reconciliar estado antes de Builder.
- `PIPELINE_BLOCKED`: detener y pedir intervencion humana o decision de Manager.

Para tickets que tocan hooks, CI o install (o que retiran copias motor-provides), el
preflight incluye ademas (ver `references/destination-preflight.md`, checks 7-8):
portabilidad de `.claude/settings.json` via
`check_claude_settings_portability.py`, hook de escritura fail-closed, y verificacion de
resolvers vivos antes de retirar copias locales. `install --sync` no es poda host-extends
segura hasta cerrar WOT-2026-003d.

## Fallback sin subagentes

Si la superficie actual no ofrece `task tool`, declarar `FALLBACK_SIN_TASK_TOOL`
en el reporte. En ese modo no se debe simular independencia:

- tickets `documentation`, `research` y `analysis` pueden cerrarse con gates y
  evidencia proporcional, declarando la independencia reducida;
- tickets `code` y `mixed` pueden implementarse, pero el cierre y el push
  requieren revision independiente externa al implementador o aprobacion humana
  explicita de cierre con rigor reducido;
- tickets de alto blast radius (`install --sync`, migraciones, borrados,
  seguridad, hooks, CI, bus, estado compartido, secretos o permisos) se dejan en
  `READY_FOR_REVIEW` o `BLOCKED_REVIEW_REQUIRED` hasta tener review
  independiente.
- Si un cierre en fallback deja `bus_drift` por eventos canonicos ausentes,
  reconciliarlo con `scripts/reconcile_ticket.py` y revalidar 0/0; no escribir
  eventos JSONL a mano ni rebajar el gate cuando existe herramienta sancionada.

## Bootstrap contextual

Antes de leer y ordenar tickets, cargar contexto real:

- aplicar `<MOTOR_ROOT>/prompts/orchestrator_destination_bootstrap.md`;
- fijar `AGENT_PROJECT_ROOT` al `repo_destino`;
- ejecutar `python <MOTOR_ROOT>/scripts/destination_context.py --bootstrap --project-root .`;
- leer `.agent/context/destination_map.md`;
- cargar memoria del destino con `python <MOTOR_ROOT>/scripts/memory_context.py --status` y `--bootstrap`;
- revisar `PROJECT.md`, `AGENTS.md`/`CLAUDE.md` si existen y `backlog.md`;
- revisar `AGENTS.md`, `audit_agent_output.md` y memoria del motor solo como
  filosofia/referencia, nunca como estado operativo del destino.

## Herramientas por fase

| Fase | Rol | Prompts | Skills | Scripts / comandos |
|---|---|---|---|---|
| Bootstrap | Orquestador | `<MOTOR_ROOT>/prompts/orchestrator_destination_bootstrap.md`, `<MOTOR_ROOT>/prompts/orchestrator_pipeline.md`, `<MOTOR_ROOT>/prompts/audit_agent_output.md` | esta skill | `python <MOTOR_ROOT>/scripts/destination_context.py --bootstrap --project-root .`, `python <MOTOR_ROOT>/scripts/memory_context.py --status`, `--bootstrap`, `python <MOTOR_ROOT>/scripts/check_motor_pristine.py --snapshot --out orchestrator_pipeline/session_close/motor_before_<TICKET_ID>.json`, `python <MOTOR_ROOT>/.agent/agent_controller.py --validate --json --project-root .` |
| Plan | Manager | `<MOTOR_ROOT>/prompts/audit_ticket_contract.md` | `<MOTOR_ROOT>/skills/manager-create-work-plan/SKILL.md`, `<MOTOR_ROOT>/skills/grill-work-plan/SKILL.md` si hay dudas, `<MOTOR_ROOT>/skills/_shared/ticket-anti-patterns.md` | `python <MOTOR_ROOT>/.agent/agent_controller.py --reset-turn --force --project-root .`, `--bootstrap-ticket`, `--validate` |
| Implementacion | Builder | `<MOTOR_ROOT>/prompts/orchestrator_launch_builder.md` | `<MOTOR_ROOT>/skills/builder-implement-from-plan/SKILL.md`, `<MOTOR_ROOT>/skills/builder-run-quality-gates/SKILL.md`, `<MOTOR_ROOT>/skills/builder-self-audit/SKILL.md` | gates del plan, `python <MOTOR_ROOT>/scripts/run_pytest_safe.py --project-root .`, `ruff`, `python <MOTOR_ROOT>/.agent/agent_controller.py --pre-handoff`, `--mark-ready` |
| Review 1 | Manager | `<MOTOR_ROOT>/prompts/manager_review.md`, `<MOTOR_ROOT>/prompts/audit_agent_output.md` | `<MOTOR_ROOT>/skills/manager-review-implementation/SKILL.md` | `git show`, `git status`, tests focales, `python <MOTOR_ROOT>/.agent/agent_controller.py --validate` |
| Review 2 | Manager adversarial | `<MOTOR_ROOT>/prompts/manager_review.md`, `<MOTOR_ROOT>/prompts/audit_agent_output.md` | `<MOTOR_ROOT>/skills/manager-review-implementation/SKILL.md`, `<MOTOR_ROOT>/skills/builder-self-audit/SKILL.md` como input critico | buscar counterexamples en diff real, revalidar bus/scope/gates |
| Cierre | Orquestador | `<MOTOR_ROOT>/prompts/orchestrator_pipeline.md`, `<MOTOR_ROOT>/prompts/orchestrator_session_close_chat.md` | `<MOTOR_ROOT>/skills/session-close-observations/SKILL.md`, `<MOTOR_ROOT>/skills/manager-session-closeout/SKILL.md`, `<MOTOR_ROOT>/skills/memory-consolidate/SKILL.md` si hay aprendizaje reusable | `python <MOTOR_ROOT>/scripts/memory_consolidate.py --apply --project-root .`, `python <MOTOR_ROOT>/.agent/agent_controller.py --session-close --dry-run --project-root .`, `python <MOTOR_ROOT>/.agent/agent_controller.py --session-close --project-root .` |
| Meta-auditoria | Auditor (read-only) | `<MOTOR_ROOT>/prompts/audit_pipeline.md`, `<MOTOR_ROOT>/prompts/audit_agent_output.md`, `<MOTOR_ROOT>/prompts/manager_review.md` | `<MOTOR_ROOT>/skills/audit-pipeline/SKILL.md` | `git show --stat`, `ruff check`, tests focales, `python <MOTOR_ROOT>/scripts/check_motor_pristine.py --check`, `python <MOTOR_ROOT>/scripts/check_encoding_guard.py` |

## Integridad del motor

Antes de cada ticket:

- ejecutar `python <MOTOR_ROOT>/scripts/check_motor_pristine.py --snapshot --out orchestrator_pipeline/session_close/motor_before_<TICKET_ID>.json`.

Despues de cada ticket:

- ejecutar `python <MOTOR_ROOT>/scripts/check_motor_pristine.py --check --snapshot-file orchestrator_pipeline/session_close/motor_before_<TICKET_ID>.json --report orchestrator_pipeline/session_close/motor_after_<TICKET_ID>.json`.

Si una escritura al motor es denegada por el harness:

- no reintentar con otro metodo;
- registrar `MOTOR_WRITE_DENIED` con `--record-denied`;
- continuar si el ticket puede completarse sin tocar el motor;
- bloquear solo si el ticket no puede cumplir sus criterios sin ese cambio.

Si aparece `MOTOR_DIRTY_DETECTED`:

- no restaurar automaticamente;
- incluir `motor_head_before`, `motor_head_after`, `pre_existing_dirty`,
  `motor_status_new`, status y diff stat en el informe;
- separar evidencia git de explicacion del agente.

## Presupuesto operativo

Usar estos tiempos como limites recomendados para evitar bloqueos largos por
chat:

| Fase | Maximo |
|---|---:|
| Manager plan | 30 min |
| Builder implementacion | 60 min |
| Manager review | 20 min |
| Total por ticket | 120 min |

Si se excede un limite, marcar `TIMEOUT`, registrar diagnostico accionable y no
cerrar el ticket.

## Reglas para Manager

- Crear planes binarios, no narrativos.
- Declarar `deliverable_type`.
- Separar `Files Likely Touched`, `Read/inspect only` y `Manager-only`.
- Incluir gates ejecutables y rutas reales.
- Crear `STRATEGY_WOT-<ticket>.md` y `AUDIT_WOT-<ticket>.md`.
- Usar `audit_ticket_contract.md` antes de pasar a Builder.
- En review, no aceptar el reporte del Builder sin evidencia propia.

## Reglas para Builder

- Implementar solo el ticket activo.
- Respetar `Files Likely Touched`.
- Registrar justificacion CEM antes de ampliar scope.
- Ejecutar y registrar gates con comandos exactos y resultados reales.
- Usar `builder-self-audit` antes de `mark-ready`.
- Si necesita limpiar archivos, moverlos a
  `repo_destino/orchestrator_pipeline/cleanup/<TICKET_ID>/`, no borrarlos.

## Reglas para Review 2

La segunda revision no repite la primera. Debe intentar refutar el cierre:

- buscar regresiones no cubiertas;
- buscar scope creep;
- buscar fixtures irreales o mock drift;
- comprobar bus, `STATE.md`, `TURN.md` y `execution_log.md`;
- contrastar claims del Builder contra diff, tests y eventos reales.

Si no encuentra blockers, puede confirmar cierre.

## Cierre e informe

Al cerrar un ticket, generar:

- `repo_destino/orchestrator_pipeline/reports/closeout_<TICKET_ID>.md`

El informe debe incluir:

- decisiones relevantes;
- decisiones tomadas por autonomia;
- commits y repos afectados;
- integridad del motor (`motor_head_before`, `motor_head_after`,
  `pre_existing_dirty`, `motor_status_new`, `motor_status_after`,
  `motor_diff_stat_after`, `denied_attempts`);
- gates con comandos exactos y exit codes;
- etiquetas de evidencia;
- limpieza no destructiva realizada;
- riesgos residuales;
- validate final y bus si aplica.

Cada claim relevante del informe debe incluir etiqueta de evidencia y artefacto
concreto (`path:`, `commit:`, `command:` + `exit_code:`, `event_seq:` o
equivalente). Etiquetas sin artefacto concreto cuentan como relato.

Antes de cerrar, pasar `scripts/check_encoding_guard.py` sobre el informe de
cierre. Si falla, corregir encoding antes de declarar cierre.

## Cierre global del pipeline

Cuando no queden tickets ejecutables, ejecutar cierre de sesion, no solo cierre
de tickets:

- generar `repo_destino/orchestrator_pipeline/reports/pipeline_closeout_<timestamp>.md`;
- aplicar `<MOTOR_ROOT>/prompts/orchestrator_session_close_chat.md`;
- ejecutar `python <MOTOR_ROOT>/.agent/agent_controller.py --session-close --dry-run --project-root .`;
- si el dry-run tiene FAIL, no ejecutar cierre real y documentar el bloqueo;
- si el dry-run es aceptable, ejecutar `python <MOTOR_ROOT>/.agent/agent_controller.py --session-close --project-root .`;
- consolidar memoria del destino si hay aprendizaje reusable;
- clasificar mejoras como `repo_destino`, `repo_motor` o `dudoso`;
- crear follow-ups para mejoras del motor en vez de tocar el motor desde un
  ticket de destino no declarado.

## Fase final: meta-auditoria read-only

Despues del cierre global, cuando ya no quedan tickets ejecutables, ejecutar la
meta-auditoria con `<MOTOR_ROOT>/skills/audit-pipeline/SKILL.md` (trigger
`/audit-pipeline`).

Es read-only: audita el cuerpo completo de trabajo cerrado, no reabre tickets ni
modifica backlog/codigo/estado. Produce:

- `repo_destino/orchestrator_pipeline/reports/pipeline_audit_<timestamp>.md`;
- `repo_destino/orchestrator_pipeline/reports/pipeline_audit_<timestamp>.json`.

No confundir con Review 1/2: aquellos son intra-ticket; esta es post-pipeline y
transversal. Sus follow-ups no se ejecutan automaticamente: el humano decide.

## Contrato de fallo

El pipeline no cierra un ticket si Builder, Review 1 o Review 2 fallan.

Ante fallo:

- no marcar `completed`;
- no convertir un fallo de Builder/Manager en cierre cosmetico ni en
  `completed` sin evidencia nueva;
- registrar diagnostico accionable;
- reabrir ciclo Builder/Manager si hay correccion posible;
- bloquear el ticket si falta una precondicion, permiso o decision humana.

## Principio de autonomia

Si hay duda no bloqueante, resolverla por la jerarquia y los tenets de
`<MOTOR_ROOT>/CONSTITUTION.md` (carga ON-DEMAND; leelo ENTERO). Fuente unica
(T5); este bloque NO re-declara sus criterios (skill apunta, prompt gobierna
-- X-09).

Jerarquia de decision (propia de este pipeline, no redundante con la de
arriba):

1. Preservar integridad del `repo_destino`.
2. Minimizar blast radius.
3. Para dudas de forma, elegir la opcion mas cercana a la evidencia tecnica.
4. Para dudas de fondo, bloquear con diagnostico accionable.

Si hubo decisiones de autonomia relevantes, documentar: decision, duda resuelta,
regla aplicada, evidencia y riesgo evitado. Si no hubo, declarar
`Decisiones de autonomia: ninguna`. Si la decision puede cambiar arquitectura,
seguridad, datos o alcance, detenerse y pedir confirmacion humana.
