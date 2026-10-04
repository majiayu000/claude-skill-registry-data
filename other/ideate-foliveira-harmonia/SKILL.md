---
name: ideate
description: Harmonia ideate stage - generate and evaluate divergent directions before committing to one. Use ONLY when explicitly invoked as /harmonia:ideate.
disable-model-invocation: true
---

Your working contract is the rules; their digest is injected at session start - read `${CLAUDE_PLUGIN_ROOT}/core/RULES.md` in full only if that digest is not in your context.
Read the `ideate` stage from `${CLAUDE_PLUGIN_ROOT}/core/lifecycle.yaml` - its agent sequence and artifact contract are authoritative; do not hardcode them.

1. Workspace: run `bash ${CLAUDE_PLUGIN_ROOT}/bin/workspace.sh mint --repo . --slug <short-task-slug>` (entry stage). If it refuses because an incomplete workspace exists, surface its message verbatim and stop - the user either continues that task (`--task <id>`) or forces `--new`.
2. Dispatch the stage's agents in order (the ideator may run the panel primitive at `${CLAUDE_PLUGIN_ROOT}/core/patterns/panel.md` for divergence). Pass the task ask and the workspace path - agents write `ideas.md` into the workspace, not into conversation.
3. Confirm the out-artifacts named by the stage exist in the workspace before finishing.

You orchestrate only: no stage logic beyond dispatch, sequencing, and artifact checks.
