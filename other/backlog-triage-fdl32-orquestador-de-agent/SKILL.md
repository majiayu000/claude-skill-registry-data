---
name: backlog-triage
version: 1.0.0
description: Planificador pre-pipeline de solo lectura que reconcilia el backlog con git, clasifica la aptitud de cada ticket, propone un DAG de grupos y recomienda por cual empezar; solo escribe su informe y su JSON. Usar cuando hay que decidir que pipeline o batch autonomo lanzar sobre el backlog vivo. No usar para ejecutar el pipeline ni mutar el backlog (ver orchestrate-pipeline), para auditar un pipeline cerrado (ver audit-pipeline) ni para dar de alta tickets (ver backlog-admit).
triggers: [/backlog-triage, backlog-triage]
author: agent
role: manager
stage: plan
writes_memory: false
quality_gate: false
tags: [core, system, backlog]
source_prompt: prompts/backlog_triage.md
contract_id: cid-backlog-triage-v1
---

# backlog-triage

Skill para conducir el analisis pre-pipeline del backlog, antes de lanzar
`orchestrate-pipeline` sobre un `repo_destino` o el backlog del motor.

Es meta-planificacion (decide que pipeline lanzar), analoga a
`manager-create-work-plan`, no una auditoria retrospectiva. No ejecuta el
pipeline y no lo audita despues de cerrado.

Es **read-only sobre el backlog**: no reabre tickets, no modifica
`backlog.md`, no toca codigo ni estado operativo. Solo escribe sus propios
artefactos de triage y propone.

## Cuando usarla

Usar cuando el usuario pida:

- decidir que tickets del backlog lanzar antes de arrancar un pipeline;
- reconciliar el backlog contra git para detectar tickets ya hechos;
- agrupar tickets pendientes en pipelines ordenados por valor y riesgo.

No usar para:

- ejecutar el pipeline (usar `orchestrate-pipeline`);
- auditar un pipeline ya cerrado (usar `audit-pipeline`);
- revisar un unico ticket en curso (usar `manager-review-implementation`).

## Prompt canonico

Leer y aplicar:

- `prompts/backlog_triage.md`

Ese prompt es la fuente de verdad. Hereda el contrato de evidencia de
`prompts/audit_agent_output.md`. Si algo diverge, prevalece
`prompts/backlog_triage.md`.

## Topologia obligatoria

- Para tickets WOT del motor, el backlog vive en el workspace, localizado via
  `.agent/config/motor_destination_link.json` (`destination_root`), NO en el
  checkout de codigo.
- Para un `repo_destino` generico, el backlog vive en
  `DESTINO_ROOT/.agent/collaboration/backlog.md`.
- Ver la nota de topologia completa en `prompts/backlog_triage.md`.

## Flujo

1. **Fase 0.pre - Gate de formato:** `check_backlog_contract.py` en exit 0
   antes de analizar.
2. **Fase 0 - Reconciliacion:** recolector mas juicio contra git; ver el
   prompt para el detalle de senales y clasificaciones.
3. **Fase 1 - Clasificacion de aptitud:** ver el prompt para las categorias y
   sus criterios.
4. **Fase 2 - Agrupacion en pipelines:** ver el prompt para los criterios de
   afinidad y dependencia.
5. **Fase 3 - Sintesis y recomendacion:** ver el prompt para el orden y el
   contenido obligatorio de la recomendacion.
6. **Emitir informe + JSON** en el mismo turno.

## Herramientas por fase

| Fase | Rol | Prompts | Scripts / comandos |
|---|---|---|---|
| 0.pre Gate | Manager | `<MOTOR_ROOT>/prompts/backlog_triage.md` | `<MOTOR_ROOT>/scripts/check_backlog_contract.py --project-root <destino>` |
| 0 Reconciliacion | Manager | `<MOTOR_ROOT>/prompts/backlog_triage.md` | `<MOTOR_ROOT>/scripts/backlog_reconcile.py --motor-root <motor> --project-root <destino>` (Paso 0.1); fallback manual `git log --grep`, `git ls-files`, greps de DoD |
| 1 Clasificacion | Manager | `<MOTOR_ROOT>/prompts/audit_agent_output.md` | lectura de `backlog.md` y planes archivados |
| 2 Agrupacion | Manager | `<MOTOR_ROOT>/prompts/backlog_triage.md` | ninguno adicional |
| 3 Sintesis | Manager | `<MOTOR_ROOT>/prompts/backlog_triage.md` | ninguno adicional |

## Contrato de evidencia

- Cada clasificacion lleva etiqueta de evidencia (`VERIFICADO` / `INFERIDO` /
  `REQUIERE_HUMANO`), heredada de `prompts/audit_agent_output.md`.
- Separar siempre `[EVIDENCIA: <fuente>]` de `[RELATO: agente_explicacion]`.
- Etiqueta sin artefacto concreto (`commit:`, `path:`) no permite afirmar
  `LIKELY_DONE`.

## Salidas

Esquema completo del JSON y estructura del informe en
`prompts/backlog_triage.md`.

## Restriccion dura

- No reabre tickets ni modifica `backlog.md`.
- No escribe codigo ni estado operativo.
- No ejecuta el pipeline ni lo audita.
- El prompt es la fuente de verdad; si algo diverge, prevalece
  `prompts/backlog_triage.md`.

La decision de archivar tickets propuestos como ya-hechos o de lanzar el
pipeline recomendado la toma el humano o el Manager leyendo el informe.
