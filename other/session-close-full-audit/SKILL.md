---
name: session-close-full-audit
version: 0.1.0
description: Auditoria adversarial previa al cierre canonico de una sesion, que encadena tres auditorias de salud y una pasada adversarial sobre el codigo generado; el cierre lo ejecuta agent_controller.py --session-close y en modo FINAL tambien registra follow-ups y propone memoria. Usar cuando se cierra una sesion que toco codigo del motor o del destino, antes de --session-close; a mitad de vuelo solo los Bloques 1, 2 y 2.5 sin 2.5.f ni 2.5.g, y nunca los Bloques 3 a 5. No usar para el cierre operativo (ver orchestrator_session_close_chat), para arrancar una sesion (ver orchestrator_session_bootstrap) ni para dejar continuidad medida a la sesion siguiente (ver session-hop); nunca corre el Bloque 3 con un ticket IN_PROGRESS.
triggers: [/close-full-audit, /session-close-full-audit, auditar-cierre-completo-sesion]
author: agent
role: auditor
stage: review
writes_memory: false
quality_gate: false
tags: [core, audit, session, close]
source_prompt: prompts/orchestrator_session_close_full_audit.md
contract_id: cid-session-close-full-audit-v0
---

# session-close-full-audit

Skill para auditar adversarialmente el cierre de una sesion ANTES del cierre
canonico. Encadena las tres auditorias estructurales de salud, anade la pasada
que el flujo anterior omitia (auditoria esceptica del CODIGO GENERADO en la
sesion), y deja proceder al cierre operativo y a la promocion de memoria solo
sobre una sesion verde y reconciliada.

## Mapa de nombres

- **Prompt:** `prompts/orchestrator_session_close_full_audit.md` (instruccion detallada
  para el agente auditor; bloques 1, 2, 2.5, 3, 4 y 5).
  - **Cierre del ESTADO del backlog:** Bloque 5, paso `8.ter`. Cerrar un ticket es un
    TRASPASO de `backlog.md` a `_archive/backlog_done.md`, no un cambio de etiqueta
    (WOT-2026-026t). El criterio vive en el prompt; esta skill no lo redeclara.
- **Skill:** `skills/session-close-full-audit/` (paquete operativo estable).
- **Trigger:** `/close-full-audit` (API humana corta y estable).
- **Salida:** reporte adversarial por bloque (conclusiones etiquetadas +
  evidencia citada); no es una categoria de artefacto persistente propia.

## Fuente canonica

Leer y aplicar:

- `<MOTOR_ROOT>/prompts/orchestrator_session_close_full_audit.md`

Ese prompt prevalece si esta skill diverge.

## Contrato duro

- **Wrapper, no reimplementacion.** Esta skill ORQUESTA otras; no duplica su
  logica. La salud la posee `system-health-audit`; el cierre operativo lo posee
  `orchestrator_session_close_chat.md` (`agent_controller.py --session-close`);
  la memoria la gobierna `memory_upload.md`.
- **Read-only por defecto.** Audita y propone el cambio minimo; no parchea salvo
  instruccion explicita (hereda `prompts/audit_agent_output.md`).
- **Evidencia antes que relato.** Ningun auto-reporte cuenta como evidencia; solo
  diff, exit code, salida real de test, evento de bus, commit/SHA, bytes, git.
  Etiqueta cada hallazgo VERIFICADO/INFERIDO/NO VERIFICADO.
- **Regla de parada.** Si un gate sale en rojo o un hallazgo contradice un claim
  previo del Builder/Manager, DETENTE: no avances a la promocion de memoria.
- **Barrera mutation-verified.** Un guard/test nuevo solo cuenta como barrera si
  se demuestra que FALLA sin el fix.
- **Memoria como gate.** El Bloque 4 es propose-before-write con destino (tier)
  declarado; promocion a `repo_motor` exige confirmacion humana explicita.

## Distincion con skills hermanas

- `system-health-audit`: salud de las 3 capas (es el Bloque 1 de esta pasada).
- `audit-pipeline`: meta-auditoria post-pipeline TRANSVERSAL del backlog completo (TODOS los tickets cerrados, no uno solo).
- `code-audit` / `builder-self-audit`: herramientas de evidencia del Bloque 2,
  no veredictos por si solas.
- `manager-session-closeout` / `session-close-observations`: cierre operativo y
  memoria (Bloques 3-4), que esta skill precede pero no sustituye.

## Flujo

1. **Bloque 1 - salud:** `audit_post_change_system_health` (via
   `system-health-audit`), `audit_complete_motor_destination`,
   `audit_portability_legacy_surface`. Read-only.
2. **Bloque 2 - codigo de la sesion:** `audit_agent_output` SOBRE LOS DIFFS de la
   sesion (`git log`/`git diff --stat`, cwd=repo_motor). Cazar false-green, root
   equivocado, fixture drift, scope creep, mock drift, floor assertion. Barreras
   mutation-verified. Herramientas de evidencia: `builder-self-audit`,
   `builder-run-quality-gates`, `code-audit`, `systematic-debugging`,
   `manager_review`.
3. **Punto de control:** la sesion debe estar VERDE y RECONCILIADA. Si el Bloque 2
   destapa false-green o contradiccion, vuelve al Builder; NO continues.
4. **Bloque 3 - cierre canonico:** comando unico
   `agent_controller.py --session-close` (dry-run, luego real; `--force` si STATE
   ya COMPLETED). Validar `0 errors / 0 warnings` post-archive; `reconcile_ticket`
   si hay `bus_drift`.
5. **Bloque 4 - memoria:** `memory_upload` como gate propose-before-write; tier
   declarado; sin evidencia no hay entrada portable; schema-drift bloquea nuevas
   entradas portables.

## Herramientas orquestadas (no reimplementar)

`scripts/collect_system_health.py`, `agent_controller.py --session-close` /
`--validate`, `scripts/reconcile_ticket.py`, `discover_skills.py
--check-contract`, `run_gates_dispatch.py`, `scripts/run_pytest_safe.py`, y los
prompts `audit_agent_output`, `manager_review`, `memory_upload`.
