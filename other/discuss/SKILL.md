---
name: discuss
description: Harmonia discuss stage - turn a direction into pinned scope with checkable success criteria. Use ONLY when explicitly invoked as /harmonia:discuss.
disable-model-invocation: true
---

Your working contract is the rules; their digest is injected at session start - read `${CLAUDE_PLUGIN_ROOT}/core/RULES.md` in full only if that digest is not in your context.
Read the `discuss` stage from `${CLAUDE_PLUGIN_ROOT}/core/lifecycle.yaml` - agents and artifacts are authoritative; do not hardcode them.

1. Workspace: `bash ${CLAUDE_PLUGIN_ROOT}/bin/workspace.sh mint --repo . --slug <short-task-slug>` (entry stage; on refusal, surface the message and stop; continue an existing task with `--task <id>` via `resolve`).
2. This is the earliest scope-bearing stage: dispatch the scoper to mint `scope.md` in the workspace - one scope declaration per task; if `scope.md` already exists, the scoper refines it in place, never re-mints. The rubber duck joins per the stage sequence for thinking-partner dialogue.
3. The scope declaration must carry a `## Success Criteria` section of `- run:` command lines - that is what the criteria gate validates before implement may start.

Pass workspace paths, not prose recaps. Orchestrate only.
