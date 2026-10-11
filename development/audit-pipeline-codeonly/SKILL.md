---
name: audit-pipeline-codeonly
description: Meta-auditoria de una cadena de tickets del motor cerrada en CODE-ONLY MODE (worktree _dev, cierre commit-directo sin bus), con evidencia por commits y bloques de cierre del workspace, aterrizaje en origin/main y costuras entre tickets. Usar cuando termina una cadena ejecutada con orchestrate-pipeline-codeonly, sin destino externo ni bus vivo. No usar para un repo_destino con bus vivo (ver audit-pipeline); no reabre tickets ni toca backlog ni codigo.
---

Lee `skills/audit-pipeline-codeonly/SKILL.md`.
