---
name: sflow-hook
description: Diagnose or explicitly invoke a Singularity Flow lifecycle hook using its exact host-supplied payload.
disable-model-invocation: true
argument-hint: "turn-intent|turn-end|agent-start|session-start|agent-guard"
---
# Inspect or invoke lifecycle hooks

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

Hooks are host integration points, not shortcuts for lifecycle commands.

1. Prefer `/sf-logs` when the user only wants to understand a hook decision.
2. Invoke `singularity-flow hook <HOOK>` only when the user explicitly requests the hook and provides the exact payload or environment required by that host contract.
3. Preserve allow/deny, reason, selected work, session, agent, and exit status exactly.
4. Never fabricate host identifiers, bypass a guard, or translate a denied hook into a direct mutation.

