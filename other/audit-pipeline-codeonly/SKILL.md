---
name: audit-pipeline-codeonly
version: 1.0.0
description: Meta-auditoria de una cadena de tickets del motor cerrada en CODE-ONLY MODE (worktree _dev, cierre commit-directo sin bus), con evidencia por commits y bloques de cierre del workspace, aterrizaje en origin/main y costuras entre tickets. Usar cuando termina una cadena ejecutada con orchestrate-pipeline-codeonly, sin destino externo ni bus vivo. No usar para un repo_destino con bus vivo (ver audit-pipeline); no reabre tickets ni toca backlog ni codigo.
triggers: [/audit-pipeline-codeonly, audit-pipeline-codeonly, auditar-pipeline-codeonly]
author: agent
role: auditor
stage: review
writes_memory: false
quality_gate: false
tags: [core, system, audit, codeonly, dogfooding]
source_prompt: prompts/audit_pipeline_codeonly.md
contract_id: cid-audit-pipeline-codeonly-v1
---

# audit-pipeline-codeonly

Skill para conducir la meta-auditoria final de una CADENA de tickets del MOTOR
ejecutada por `orchestrate-pipeline-codeonly` en **CODE-ONLY MODE**: worktree
`_dev`, cierre commit-directo, sin bus ni destino externo.

Es la variante especializada de `audit-pipeline` para el dogfooding del propio
motor. NO reimplementa el metodo: el flujo completo (topologia code-only,
Fase 0 con cierre manual como caso por defecto, doble pasada A/B por ticket,
Fase 2 transversal de SEAMS, veredicto, salidas) vive en
`prompts/audit_pipeline_codeonly.md`, que a su vez hereda de la base
`prompts/audit_pipeline.md`. **El prompt es la fuente de verdad; si algo diverge,
prevalece el prompt.**

No es un tercer Review por ticket. Review 1 y Review 2 son intra-ticket y
sincronicos. Esta skill es post-cadena, retrospectiva y transversal: audita el
cuerpo completo de la cadena cerrada y busca los SEAMS que ningun Review 2
por-ticket puede ver.

Es **read-only sobre el sistema auditado**: no reabre tickets, no toca backlog
(`_archive/backlog_done.md`), codigo ni estado operativo (ni en `_dev` ni en el
workspace). Solo escribe sus propios artefactos de auditoria y propone
follow-ups.

## Cuando usarla

Las TRES condiciones de CODE-ONLY MODE a la vez (si falta una, usar
`audit-pipeline` canonico):

- la cadena auditada entrego CODIGO del motor (`delivery_authority: repo_motor`);
- se ejecuto en la worktree **`_dev`** (rama `main`), no en un `repo_destino`
  generico con bus;
- **CODE-ONLY MODE**: sin destino externo -> bus bloqueado, cierre
  commit-directo, sin `pipeline_closeout_*.md`.

## Cuando NO usarla

- Si la cadena corrio sobre un `repo_destino` con bus vivo (existe
  `pipeline_closeout_*.md`): usar `audit-pipeline` canonico
  (`prompts/audit_pipeline.md`).
- Para revisar un unico ticket en curso (usar `manager-review-implementation`).
- Para conducir el bucle de implantacion (usar `orchestrate-pipeline-codeonly`).
- Para decidir QUE pipeline lanzar (usar `backlog-triage`, read-only).

## Prompt canonico

Leer y aplicar:

- `prompts/audit_pipeline_codeonly.md`

Ese prompt es la fuente de verdad. Hereda estructura y filosofia de la base
`prompts/audit_pipeline.md`, filosofia CEM de `prompts/audit_agent_output.md` y
mecanica de doble pasada de `prompts/manager_review.md`. Si algo diverge,
prevalece `prompts/audit_pipeline_codeonly.md`.

## Topologia obligatoria (code-only)

- `_dev` (motor, worktree `main`): donde vive el CODIGO auditado.
- `workspace`: donde vive el BACKLOG y los cierres (`_archive/backlog_done.md`);
  el informe se escribe aqui.
- `principal` (motor, detached): consumo; no se audita ni se toca.
- El motor es read-only; `scripts/check_motor_pristine.py` es evidencia de
  integridad, nunca restauracion.

## Diferencias clave con `audit-pipeline` canonico

- **Cierre manual = caso por defecto:** la ausencia de `pipeline_closeout_*.md` /
  `closeout_<TICKET>.md` es ESPERADA y NO bloquea `APROBADO`.
- **Evidencia sustituta:** commits git con el ID + bloque de cierre del workspace
  (`_archive/backlog_done.md`), no closeouts.
- **Integridad sin bus:** `git status` de `_dev` + `check_motor_pristine.py` +
  aterrizaje de cada `commit:<sha>` en `origin/main` via
  `scripts/check_backlog_commits_landed.py`. Un cierre no aterrizado
  (`CLOSURE_NOT_LANDED`) BLOQUEA el veredicto.
- **Warnings de `--validate` como accepted_advisories (021u):** los warnings
  estructurales de code-only NO son hallazgos; solo cuenta un `actionable > 0`.
- **Mutation-verify con aislamiento de rama (021u):** al refutar una barrera,
  exigir que el fixture AISLE la rama mutada; un fixture con 2 rutas redundantes
  da falso-verde.

## Herramientas por fase

| Fase | Rol | Prompts | Scripts / comandos |
|---|---|---|---|
| Vision global | Auditor | `<_dev>/prompts/audit_pipeline_codeonly.md` | leer `backlog.md` y `_archive/backlog_done.md` del workspace |
| Por ticket A/B | Auditor | `<_dev>/prompts/audit_agent_output.md`, `<_dev>/prompts/manager_review.md` | `git show --stat`, `git log origin/main --grep <ID>`, `ruff check`, tests focales, `<_dev>/scripts/check_encoding_guard.py` |
| Transversal | Auditor | `<_dev>/prompts/audit_pipeline_codeonly.md` | `<_dev>/scripts/check_motor_pristine.py`, `<_dev>/scripts/check_backlog_commits_landed.py` |
| Informe | Auditor | `<_dev>/prompts/audit_pipeline_codeonly.md` | `<_dev>/scripts/check_encoding_guard.py` sobre el informe |

## Salidas

- `<workspace>/orchestrator_pipeline/reports/pipeline_audit_codeonly_<timestamp>.md`
- `<workspace>/orchestrator_pipeline/reports/pipeline_audit_codeonly_<timestamp>.json`

Estructura detallada de ambos en `prompts/audit_pipeline_codeonly.md`.

## Restriccion dura

- No reabre tickets ni modifica `backlog.md` / `_archive/backlog_done.md`.
- No escribe codigo ni estado operativo (ni en `_dev` ni en el workspace).
- No restaura el motor ni sincroniza el principal.
- Mejoras del motor van como follow-up, nunca como edicion del motor.
- La skill es puntero: no redeclara el metodo. Remite al prompt.

La reapertura de tickets o adopcion de mejoras la decide el humano leyendo el
informe.
