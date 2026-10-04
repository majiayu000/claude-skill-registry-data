---
name: plan
description: Harmonia plan stage - design how to build within the pinned scope. Use ONLY when explicitly invoked as /harmonia:plan.
---

Your working contract is the rules; their digest is injected at session start - read `${CLAUDE_PLUGIN_ROOT}/core/RULES.md` in full only if that digest is not in your context.
Read the `plan` stage from `${CLAUDE_PLUGIN_ROOT}/core/lifecycle.yaml` (already in context if the flow runner loaded it - do not re-read) - agents and artifacts are authoritative; do not hardcode them.

1. Workspace: `bash ${CLAUDE_PLUGIN_ROOT}/bin/workspace.sh resolve --repo .` to continue the active task; if there is none, this becomes the entry stage - `mint` a workspace (on refusal, surface the message and stop).
2. Scope first: if `scope.md` is absent from the workspace, dispatch the scoper to mint it; if present, the scoper consumes and refines - never re-mints. Then dispatch the planner to write `design.md` strictly inside that boundary.
3. Recall context for the planner: it may run `bash ${CLAUDE_PLUGIN_ROOT}/bin/memory/recall.sh` directly; forward relevant summaries in its dispatch prompt.

Pass workspace paths, not prose recaps. Orchestrate only.
