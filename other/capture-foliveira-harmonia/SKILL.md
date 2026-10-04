---
name: capture
description: Harmonia capture stage - record learnings into the right memory tier, then ship structured commits. Use ONLY when explicitly invoked as /harmonia:capture.
disable-model-invocation: true
---

Your working contract is the rules; their digest is injected at session start - read `${CLAUDE_PLUGIN_ROOT}/core/RULES.md` in full only if that digest is not in your context.
Read the `capture` stage from `${CLAUDE_PLUGIN_ROOT}/core/lifecycle.yaml` - its agent sequence ends with the committer by contract; do not hardcode.

1. Workspace: `bash ${CLAUDE_PLUGIN_ROOT}/bin/workspace.sh resolve --repo .` (later stage: never mints; surface ambiguity or no-active-task and stop).
2. Acceptance gate: capture requires the `acceptance` in-artifact (`workspace:accepted`), written only by the developer after they exercised the built behavior and it matches intent. Verify it: `bash ${CLAUDE_PLUGIN_ROOT}/bin/workspace.sh verify-acceptance --repo .`. Gate on the exit: any non-zero exit means refuse - surface the script's own message verbatim and stop, do not dispatch the curator; only a zero exit proceeds. The message states the remedy: no marker means the developer records acceptance via `/harmonia:accept`; a stale digest mismatch means the diff moved after acceptance, so the developer exercises the current behavior and re-accepts via `/harmonia:accept` (the marker must digest the diff it attests); a live rejection clears via `/harmonia:accept` or `/harmonia:abandon`. Never run accept on the developer's behalf - acceptance is a human act.
3. Dispatch the knowledge curator with the verdict, scope, and diff-summary paths. It drafts learnings and writes each through `bash ${CLAUDE_PLUGIN_ROOT}/bin/memory/capture.sh` with an explicit `--tier` decision and `--client` flag where applicable - client content never reaches the global tier.
4. Dispatch the committer with `boundary.md`, `diff-summary.md`, and the verdict: structured, single-concern commits whose messages communicate intent; nothing outside the boundary, never workspace files.
5. Close the task: `bash ${CLAUDE_PLUGIN_ROOT}/bin/workspace.sh complete --repo .` (writes the completion marker so resolution skips this workspace).

Pass workspace paths, not prose recaps. Orchestrate only.
