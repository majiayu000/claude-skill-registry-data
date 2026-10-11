---
name: orchestrate-pipeline-codeonly
description: Pipeline multi-ticket del motor en CODE-ONLY MODE que muta codigo en la worktree _dev, con work_plan, STRATEGY y AUDIT por ticket, dos revisiones (la segunda en contexto fresco) y cierre por commit directo sin bus. Usar cuando el ticket tiene delivery_authority repo_motor, se trabaja en la worktree _dev y el motor esta en CODE-ONLY MODE; el push va agrupado al final y con autorizacion explicita. No usar para el pipeline canonico con bus vivo (ver orchestrate-pipeline), para decidir que pipeline lanzar (ver backlog-triage) ni para auditar la cadena cerrada (ver audit-pipeline-codeonly).
---

Lee `skills/orchestrate-pipeline-codeonly/SKILL.md`.
