---
name: pd-routing
description: "Use when the operator names a project or a {slug}-pd (\"work on <project>\", \"have <project>-pd do X\"), asks for parallel work on a project, a background PD emits RESPAWN_REQUEST, or a PENDING PD RESPAWNS block appears. Forward to a running PD or spawn one PD per project. On-demand; moved out of CLAUDE.md."
---
# PD routing

1. **Running PD for that project?** Forward the message with SendMessage; do not do the work yourself. Unclear which PD → ask the operator.
2. **None running (or it finished)?** `/pd-spawn {slug}` or `/pd-resume {slug}`. Both spawn the project's own `{slug}-pd` definition (pd-coordinator only when none exists).
3. **Parallel work on one project** ("do X, Y, Z in parallel") → spawn that project's PD ONCE with the full list; the PD fans out (N_global = 5: max 5 Execs running per PD tree). Never one PD per task, never parallelize in the main session.
4. Act directly only when the message is addressed to you ("you do this", "not the PD") or is about a project with no PD.
5. **RESPAWN_REQUEST {slug}** from a background PD → in the same turn run `/pd-resume {slug}`, then `rm {agency-root}/state/respawn-queue/{slug}`. Durable flag and drain points: `{agency-root}/runbooks/respawn-contract.md`.
6. A `PENDING PD RESPAWNS` block at session start is handled before anything else.
