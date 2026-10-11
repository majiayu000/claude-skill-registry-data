---
name: audit-pipeline
description: Meta-auditoria retrospectiva de un pipeline multi-ticket ya cerrado en un repo_destino con bus, que re-deriva cada closeout desde git, tests y bus en doble pasada A/B y emite informe y decision artifact. Usar cuando el pipeline de un repo_destino ha cerrado y ya no quedan tickets ejecutables. No usar para revisar un ticket concreto (ver manager-review-implementation) ni para el motor en CODE-ONLY MODE (ver audit-pipeline-codeonly); no reabre tickets ni toca backlog.
---

Lee `skills/audit-pipeline/SKILL.md`.
