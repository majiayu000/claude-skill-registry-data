---
name: day-start
description: Use when starting a work day or choosing the next repository task.
---

# Day Start

Start with `ai-dlc next` for an offline summary derived from local tracker, PR and specification artifacts. It does not consult the tracker or prove completion; run `ai-dlc work finish <id>` after merge for the completion gate. `--all` includes unpublished records and `--json` exposes the same summary data.

Return a short ordered focus list with evidence links, blockers, and the next concrete action. Consult the tracker role for priorities/status, repository documents for durable context, and knowledge role only for personal continuity. Reconcile stale handoffs against current work and SCM evidence. A plan does not authorize publishing, sending messages, or changing status.

Resolve provider-specific commands from the configured role provider’s instructions. The agent supplies judgment; services store, validate, and link artifacts.

When a linked project workspace is available, use its project association and unresolved questions to retrieve only relevant personal context. Follow source links back to current repository or selected team authority; private interpretations and old daily logs do not override current specifications.

Read relevant learning notes recalled by `work start` or the session-start hook.
The returned paths and first lines are bounded personal context; inspect useful
notes and reconcile them against current specifications and evidence before acting.
A missing vault or no matching notes requires no setup and does not block work.
