---
name: hooks
description: Use when automating agent behavior with lifecycle hooks. Covers hook events, deterministic enforcement of rules the model should not be trusted to remember, and avoiding hooks that make an agent unusable.
metadata:
  category: agent-tooling
  version: 1.0.0
  tags: [hooks, automation, lifecycle, enforcement]
---

# Hooks

## Purpose

Enforce a rule deterministically rather than asking the model to remember it. A hook runs every time, regardless of the model's attention, its context, or its mood — which is exactly what a rule requires.

## When to Use

- A rule must hold every time: formatting, a forbidden command, a required check.
- The agent keeps forgetting an instruction despite it being in the instructions.
- Automating a step that should happen around every edit or command.
- Blocking a dangerous action before it executes.

## Capabilities

- Lifecycle events: before and after a tool call, on session start, on stop.
- Deterministic enforcement: formatting, linting, blocking.
- Injecting context at the right moment.
- Notification and logging.

## Inputs

- The rule and when it must apply.
- The event that should trigger it.
- What should happen when it fails: block, warn, or fix.

## Outputs

- Hook configuration that runs reliably.
- Rules enforced without depending on the model's memory.
- A fast hook — one that does not make the agent unpleasant to use.

## Workflow

1. **Identify the rule that keeps being broken** — If an instruction is in the instruction file and is still violated, it is a hook, not an instruction. Instructions are guidance; hooks are enforcement.
2. **Choose the event** — Before a tool call to block or validate; after one to format or verify; on session start to inject context.
3. **Make it fast** — A hook runs on every matching event. Two seconds on every file edit is a hostile environment. Under 500ms, or run it asynchronously.
4. **Fail informatively** — A hook that blocks must say why and what to do instead. A silent block is maddening and the model cannot recover from it.
5. **Prefer fixing over blocking** — A hook that formats the file is better than one that rejects the edit and demands the model format it.
6. **Test the hook itself** — A broken hook blocks everything, and the failure mode is confusing.

## Best Practices

- A rule the model must remember is a rule the model will eventually forget. If it matters, enforce it in a hook.
- Do not put slow operations in a synchronous hook. A full test suite on every edit is a way to make the agent unusable.
- Blocking hooks must explain themselves. `exit 2` with an explanatory message on stderr is what lets the model correct course.
- Match narrowly. A hook that fires on every tool call, including reads, wastes time on operations it does not care about.
- Auto-formatting after an edit is the single most valuable hook: it removes an entire class of diff noise and lint failures for free.
- Guard against the destructive command (`rm -rf`, a force push, a production deploy) in a pre-tool hook. This is cheap insurance.

## Examples

**Format on write — the highest-value hook:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$CLAUDE_FILE_PATHS\" | grep -qE '\\.(ts|tsx)$'; then pnpm prettier --write $CLAUDE_FILE_PATHS 2>/dev/null; fi"
          }
        ]
      }
    ]
  }
}
```

Every file the agent writes is formatted. The model never has to think about it, the diff is always clean, and the lint step never fails on formatting.

**Blocking a destructive command, with an explanation the model can act on:**

```bash
#!/usr/bin/env bash
# PreToolUse hook on Bash. Exit 2 blocks the call; stderr is shown to the model.
set -euo pipefail

command=$(jq -r '.tool_input.command' <<<"$(cat)")

if [[ "$command" =~ (^|[[:space:]])rm[[:space:]]+(-[a-zA-Z]*f[a-zA-Z]*[[:space:]]+)*/ ]]; then
  echo "Blocked: 'rm -rf' targeting an absolute path is not permitted." >&2
  echo "If you need to remove build artifacts, use 'pnpm clean'." >&2
  exit 2
fi

if [[ "$command" =~ git[[:space:]]+push.*--force([[:space:]]|$) ]]; then
  echo "Blocked: force-push is not permitted on this repository." >&2
  echo "Use 'git push --force-with-lease' if you must rewrite a branch you own." >&2
  exit 2
fi

exit 0
```

The model receives the message, understands why it was blocked, and uses the suggested alternative — rather than retrying the same command.

## Notes

- Exit code 2 from a `PreToolUse` hook blocks the tool call and returns stderr to the model. Any other non-zero code is treated as a hook error, which is a different and less useful outcome.
- Hooks run with your credentials and permissions. A hook is arbitrary code executing on every matching event — review them as carefully as any other code with that reach.
- The instinct to add many hooks should be resisted. Each one is latency on every operation. Add the ones that prevent real, observed failures.
