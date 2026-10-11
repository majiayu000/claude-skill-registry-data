---
name: system-health-audit
version: 0.1.0
description: Auditoria periodica de salud de las tres capas (repo_motor, repo_destino e integracion) tras cambios, con un recolector determinista que junta la evidencia y el agente que la audita en solo lectura. Usar cuando hubo cambios en el motor o en un repo_destino y hay que saber si el sistema sigue sano de extremo a extremo. No usar para meta-auditar un pipeline cerrado (ver audit-pipeline), para el listo-para-publicar de un repo (ver audit-git-publication) ni como snapshot rapido (ver local-audit); el reporte del recolector no es el veredicto.
triggers: [/audit-system-health, system-health-audit, auditar-salud-sistema]
author: agent
role: auditor
stage: review
writes_memory: false
quality_gate: false
tags: [core, audit, health, system]
source_prompt: prompts/audit_post_change_system_health.md
contract_id: cid-system-health-audit-v0
---

# system-health-audit

Skill para auditar periodicamente la salud de TODO el sistema multi-agente tras
hacer cambios en el motor y/o en un repo destino. Cubre tres capas: `repo_motor`,
`repo_destino` e integracion motor+destino.

## Mapa de nombres

- **Prompt:** `prompts/audit_post_change_system_health.md` (instruccion
  detallada para el agente auditor).
- **Skill:** `skills/system-health-audit/` (paquete operativo estable).
- **Trigger:** `/audit-system-health` (API humana corta y estable).
- **Salida:** `.agent/audits/system_health/` en el repo destino (categoria
  persistente de evidencia, no nombre de prompt).

## Fuente canonica

Leer y aplicar:

- `<MOTOR_ROOT>/prompts/audit_post_change_system_health.md`

Ese prompt prevalece si esta skill diverge.

## Contrato duro

- **Script = recolector, agente = auditor.** `scripts/collect_system_health.py`
  recolecta evidencia determinista y escribe artefactos; NO emite veredicto. El
  juicio adversarial (Pasada B) lo hace el agente.
- **Read-only (v0).** Por defecto el recolector no muta ningun fichero TRACKED
  (escribe solo dentro de su carpeta de salida) y no tiene `--apply-fixes` en v0
  (reservado a v1, solo drift doc/CLI con evidencia). Archivado y saneo SALEN como
  tickets, nunca se ejecutan en la misma pasada.
- **El motor ejecuta; el destino conserva.** Salida canonica en el destino:
  `.agent/audits/system_health/general_audit_YYYYMMDD[_HHMM]/`, carpeta INMUTABLE.
- **Indice estable:** `.agent/audits/system_health/INDEX.md` (fichero TRACKED);
  solo se actualiza con `--publish-index` (opt-in, OFF por defecto: WOT-2026-023x).
- **No vender verde global** si `run_pytest_safe` corre un allowlist parcial.
- **Exit code real**, nunca medido con `cmd | tail` (mide el pipe, no el runner).
- **`raw/` no publicable** por defecto (filtra rutas personales/PII); `findings.json`
  con rutas relativizadas; pasar artefactos por `classify_publication` antes de publicar.
- **No debilitar `guard_paths`**: escribir con cwd en el destino o allowlist
  ultra-acotado a `.agent/audits/system_health/**`.
- **Suite roja bloquea saneo ejecutable**, no la documentacion de la auditoria.
- **Integracion host-extends (Fase 5):** cuando el cambio toca hooks, CI, install o
  retirada de copias, exigir tabla de Resolver integrity (consumidores vivos hacia
  `agent_system/`/`scripts/`/`skills/`/`.agent/hooks/` locales), revisar
  `.claude/settings.json` + `.agent/hooks/claude_guard_entry.py` +
  `scripts/check_claude_settings_portability.py`, y prueba de comportamiento del hook
  de escritura (externo bloquea, interno benigno permite, link/motor ausente falla
  cerrado). `install --sync` no es poda host-extends segura hasta cerrar WOT-2026-003d.

## Distincion con skills hermanas

- `audit-pipeline`: meta-auditoria post-pipeline TRANSVERSAL del backlog completo (TODOS los tickets cerrados, no uno solo).
- `audit-git-publication`: listo-para-publicar de un repo.
- `local-audit`: snapshot rapido de estado (lo orquesta esta skill, no lo sustituye).
- `system-health-audit` (esta): salud periodica de las 3 capas tras cambios.

## Flujo

1. Confirmar topologia: `repo_motor`, `repo_destino`, `AGENT_PROJECT_ROOT`,
   `motor_destination_link.json`. Elegir `--mode full|motor-only|auto`.
2. Ejecutar el recolector:
   `python <MOTOR_ROOT>/scripts/collect_system_health.py --motor-root <MOTOR> --project-root <DESTINO> --mode auto`
3. Pasada A (relato): revisar `findings.json` + `raw/` + esqueletos `.md` generados.
4. Pasada B (juicio adversarial): triangular intencion/codigo/operacion, clasificar
   claims VERIFICADO/INFERIDO/NO VERIFICADO, detectar falso verde, root equivocado,
   fixture drift, scope creep. Re-derivar por bytes/codigo lo marcado relevante.
5. Rellenar `00_scope` .. `07_adversarial_review` + `auditoria_general_resumen.md`.
6. Emitir `05_archive_plan.md` (KEEP/ARCHIVE/DELETE por ruta + rollback) y
   `06_tickets.md` (un ticket por familia). Reflejar tickets ejecutables en
   `.agent/collaboration/`, no dentro de la auditoria.
7. Actualizar `INDEX.md`.

## Exit codes del recolector

- `0`: recoleccion OK, sin criticos automaticos.
- `1`: recoleccion OK, criticos automaticos (suite roja, secreto, DECIDE pendiente).
- `2`: error de ejecucion/recoleccion.
- `3`: topologia incompleta/degradada cuando se exige `--mode full`.

## Herramientas orquestadas (no reimplementar)

`local_audit.py`, `agent_controller.py --validate`, `discover_skills.py
--check-contract`, `run_gates_dispatch.py` / `run_pytest_safe.py` + `ruff`,
`check_encoding_guard.py`, `check_motor_pristine.py`, `classify_publication.py`,
`git ls-files` vs `MANIFEST.distribute`/`MANIFEST.workspace`.

## Plantilla de referencia v0

Los artefactos de `general_audit_20260613` son la plantilla dorada v0.
