---
name: audit-pipeline
version: 1.0.0
description: Meta-auditoria retrospectiva de un pipeline multi-ticket ya cerrado en un repo_destino con bus, que re-deriva cada closeout desde git, tests y bus en doble pasada A/B y emite informe y decision artifact. Usar cuando el pipeline de un repo_destino ha cerrado y ya no quedan tickets ejecutables. No usar para revisar un ticket concreto (ver manager-review-implementation) ni para el motor en CODE-ONLY MODE (ver audit-pipeline-codeonly); no reabre tickets ni toca backlog.
triggers: [/audit-pipeline, audit-pipeline, auditar-pipeline]
author: agent
role: auditor
stage: review
writes_memory: false
quality_gate: false
tags: [core, system, audit]
source_prompt: prompts/audit_pipeline.md
contract_id: cid-audit-pipeline-v1
---

# audit-pipeline

Skill para conducir la meta-auditoria final de un pipeline ya ejecutado por
`orchestrate-pipeline` sobre un `repo_destino`.

No es un tercer Review por ticket. Review 1 y Review 2 son intra-ticket y
sincronicos. Esta skill es post-pipeline, retrospectiva y transversal: audita el
cuerpo completo de trabajo cerrado y produce un informe consolidado.

Es **read-only sobre el sistema auditado**: no reabre tickets, no toca backlog,
codigo ni estado operativo. Solo escribe sus propios artefactos de auditoria y
propone follow-ups.

## Cuando usarla

Usar cuando el usuario pida:

- auditar un pipeline ya cerrado de tickets en `repo_destino`;
- una revision final transversal de implementacion, codigo, docs y alineacion
  con objetivos del backlog;
- detectar objetivos huerfanos, deuda no retomada o contradicciones entre
  tickets cerrados.

No usar para:

- revisar un unico ticket en curso (usar `manager-review-implementation`);
- conducir el bucle de implantacion (usar `orchestrate-pipeline`);
- corregir o reabrir trabajo (esta skill no escribe estado operativo).

## Prompt canonico

Leer y aplicar:

- `prompts/audit_pipeline.md`

Ese prompt es la fuente de verdad. Hereda filosofia de
`prompts/audit_agent_output.md` y mecanica de `prompts/manager_review.md`. Si
algo diverge, prevalece `prompts/audit_pipeline.md`.

## Topologia obligatoria

Igual que `orchestrate-pipeline`:

- `repo_destino`: cwd del proyecto auditado.
- `MOTOR_ROOT`: desde `.agent/config/motor_destination_link.json`.
- `AGENT_PROJECT_ROOT`: apunta al `repo_destino`.
- El motor es read-only; `scripts/check_motor_pristine.py` es evidencia de
  integridad, nunca restauracion.
- El informe debe declarar `AGENT_PROJECT_ROOT`, `MOTOR_ROOT`, `repo_destino` y
  el resultado del self-integrity check.

## Flujo

1. **Fase 0 - Vision global:** leer `backlog.md` completo, seleccionar el
   `pipeline_closeout_*.md` mas reciente de forma deterministica y leer todos
   los `closeout_*.md`. Si hay multiples closeouts de un ticket, usar el mas
   reciente y registrar descartados. Construir la matriz objetivo -> ticket ->
   evidencia -> estado. Si falta un closeout, marcar `NO_VERIFICABLE` salvo
   evidencia de fallo; si el artefacto era obligatorio, registrar
   `EVIDENCIA_AUSENTE`. Para la regla de emision de `APROBADO` cuando falta
   el cierre global (distincion cierre manual vs artefacto esperado ausente),
   aplicar el contrato de `prompts/audit_pipeline.md` (cid-audit-pipeline-v1),
   Fase 0 paso 2.
2. **Fase 1 - Doble pasada por ticket:**
   - Pasada A (verificacion): plan, `deliverable_type`, implementacion, logs,
     tests/gates proporcionales, docs, closeout en cuatro ejes. Para bugs o
     regresiones, buscar evidencia de fallo previo; para `code`/`mixed` con
     mocks, revisar mock-drift contra codigo real.
   - Pasada B (refutacion): falso verde, scope creep, claims sin evidencia,
     fixtures irreales, estado canonico incoherente.
3. **Fase 2 - Transversal:** dependencias, objetivos huerfanos, deuda no
   retomada, contradicciones, drift de motor acumulado e integridad
   (`INTEGRITY_VIOLATION_DETECTED` / `MOTOR_WRITE_DENIED`). Cada hallazgo
   transversal declara Clase CEM.
4. **Veredicto global:** `APROBADO` / `APROBADO CON NITS` /
   `CAMBIOS NECESARIOS` / `NO ACEPTAR TODAVIA`.
5. **Emitir informe + JSON** en el mismo turno.

## Herramientas por fase

| Fase | Rol | Prompts | Scripts / comandos |
|---|---|---|---|
| Vision global | Auditor | `<MOTOR_ROOT>/prompts/audit_pipeline.md` | leer `backlog.md`, `orchestrator_pipeline/reports/*.md` |
| Por ticket A/B | Auditor | `<MOTOR_ROOT>/prompts/audit_agent_output.md`, `<MOTOR_ROOT>/prompts/manager_review.md` | `git show --stat`, `git log --oneline`, `ruff check`, tests focales, `<MOTOR_ROOT>/scripts/check_encoding_guard.py` |
| Transversal | Auditor | `<MOTOR_ROOT>/prompts/audit_pipeline.md` | `<MOTOR_ROOT>/scripts/check_motor_pristine.py --check`, leer `motor_after_*.json` |
| Informe | Auditor | `<MOTOR_ROOT>/prompts/audit_pipeline.md` | `<MOTOR_ROOT>/scripts/check_encoding_guard.py` sobre el informe |

## Contrato de evidencia

- Cada claim relevante lleva etiqueta de evidencia con artefacto concreto
  (`path:`, `commit:`, `command:`+`exit_code:`, `event_seq:` o `bytes:`).
- Separar siempre `[EVIDENCIA: <fuente>]` de `[RELATO: agente_explicacion]`.
- Etiqueta sin artefacto = relato, no permite afirmar cumplimiento.
- Los closeouts son relato del pipeline: re-derivar desde git, plan y logs.

## Salidas

- `repo_destino/orchestrator_pipeline/reports/pipeline_audit_<timestamp>.md`
- `repo_destino/orchestrator_pipeline/reports/pipeline_audit_<timestamp>.json`

Estructura detallada de ambos en `prompts/audit_pipeline.md`. El Markdown debe
incluir el alcance auditado y el JSON debe incluir `audit_scope`,
`audit_scope_patterns`, `audit_scope_description`, `source_reports` con `path`,
`exists` y `role`, `missing_evidence`, `integrity_events`,
`motor_integrity.per_ticket`, `runtime_topology`, `source_snapshot` e
`improvements[].severity`.

## Restriccion dura

- No reabre tickets ni modifica `backlog.md`.
- No escribe codigo ni estado operativo.
- No restaura motor ni destino.
- Mejoras del motor van como follow-up, nunca como edicion del motor.

La reapertura de tickets o adopcion de mejoras la decide el humano leyendo el
informe.
