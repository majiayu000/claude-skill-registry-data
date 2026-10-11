---
name: audit-git-publication
version: 1.0.0
description: Auditoria dry-run de si un repo_destino puede publicarse en Git sin secretos, PII, artefactos privados ni deuda sin decision, con classify_publication.py y doble pasada de verificacion y refutacion. Usar cuando se prepara la primera publicacion de un repo_destino o una revision de su exposicion. No usar para instalar el destino (ver setup-agent-system) ni como gate pre-push de estado vivo (ver check_destino_publish_ready.py); no publica, no commitea ni borra nada.
triggers: [/audit-git-publication, audit-git-publication, auditar-publicacion-git, publicar-git]
author: agent
role: auditor
stage: review
writes_memory: false
quality_gate: false
tags: [core, git, audit, publication]
source_prompt: prompts/audit_git_publication.md
contract_id: cid-audit-git-publication-v1
---

# audit-git-publication

Skill para auditar si un `repo_destino` esta listo para publicacion Git sin
exponer secretos, estado privado o artefactos internos.

## Fuente canonica

Leer y aplicar:

- `<MOTOR_ROOT>/prompts/audit_git_publication.md`

Ese prompt prevalece si esta skill diverge.

## Contrato duro

- Dry-run only: no `git add`, `git rm`, `git commit`, `git push`, ni edicion de
  `.gitignore`.
- El script es ayuda determinista, no evidencia final. La pasada adversarial
  reabre archivos clasificados como `PUBLISH`, `PUBLISH_WITH_REDACTIONS` y
  `DECIDE`.
- Escanear tree e historia Git para primera publicacion.
- `--quick` / `--no-history` no pueden devolver `LISTO_PARA_PUBLICAR`; son modo
  de intervencion humana.
- Separar `EXCLUDE_UNTRACKED` de `EXCLUDE_TRACKED`: `.gitignore` no destrackea
  archivos ya commiteados.
- Detectar `dirty_during_scan`; si el arbol cambia durante el scan, no hay verde.
- Detectar `head_changed_during_scan`; si HEAD cambia durante el scan, no hay
  verde.
- Bloquear `repo_motor` por defecto cuando existe `MANIFEST.distribute`; usar
  `--allow-motor-root` solo para auditorias explicitas del motor.
- Excluir dinamicamente la ruta `--out` para no auto-publicar el reporte.
- `.env.example` es publicable como plantilla, pero sigue escaneado con patrones
  criticos reales.

## Flujo

1. Confirmar `repo_destino`, `MOTOR_ROOT` y `AGENT_PROJECT_ROOT`.
2. Ejecutar:
   `python <MOTOR_ROOT>/scripts/classify_publication.py --repo-root <REPO_DESTINO> --out <REPO_DESTINO>/orchestrator_pipeline/reports/publication_manifest.json`
3. Pasada A: revisar resumen, `tree_secret_scan`, `history_secret_scan`,
   `EXCLUDE_TRACKED`, `DECIDE`, redacciones obligatorias, `redaction_targets`,
   `dirty_during_scan`, `head_changed_during_scan`, `is_motor_root` y acciones
   manuales.
4. Pasada B: abrir archivos candidatos y refutar la clasificacion del script.
5. Emitir informe Markdown + JSON bajo `orchestrator_pipeline/reports/`.

## Veredictos

- `LISTO_PARA_PUBLICAR`
- `LISTO_CON_REDACTIONS`
- `DECIDE_PENDING`
- `BLOQUEADO_POR_SECRETO`
- `NO_ACEPTAR_TODAVIA`

Exit codes del script:

- `0`: solo `LISTO_PARA_PUBLICAR`.
- `1`: `BLOQUEADO_POR_SECRETO`.
- `2`: error real de herramienta o excepcion no controlada.
- `3`: intervencion humana (`DECIDE_PENDING`, `LISTO_CON_REDACTIONS`,
  `NO_ACEPTAR_TODAVIA`, quick mode o dirty durante scan).
