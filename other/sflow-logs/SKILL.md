---
name: sflow-logs
description: Explain what a Singularity Flow command actually did.
argument-hint: "[--level error|warn|info|debug|all] [--event PATTERN] [--tail N] [--since WHEN]"

---
# Read the activity log

<!-- sflow-output-contract: concise-relay -->
**Output contract:** Relay requested CLI fields or output faithfully; preserve warnings/errors and only the explanations required below.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

Run `singularity-flow logs $ARGUMENTS`. This command is read-only: it never
changes repository, workflow, or lifecycle state, and it works even while a
session is gated — a blocked session is exactly when the log matters.

Start narrow and widen only if needed:

```bash
singularity-flow logs --level error          # what failed
singularity-flow logs --level warn           # failures and refusals
singularity-flow logs --event hook           # why a tool call was refused
singularity-flow logs --event copilot        # what a native Copilot handoff did
singularity-flow logs --tail 200             # more history
singularity-flow logs --since 2026-07-25     # from a point in time
singularity-flow logs level                  # effective levels and the log path
```

When the log is empty or too sparse to explain the problem, ask the contributor
to re-run the failing command with a raised level rather than guessing:

```bash
SINGULARITY_FLOW_LOG_LEVEL=all singularity-flow <the failing command>
```

## How to read what you find

- `command.failed` carries the exact message, exit code, duration, and stack. Report the message and the failing command, not a paraphrase.
- `hook.guard.deny` means Singularity Flow refused a tool call. The `reason` field says which selection was missing. Fix the cause — usually `/sf-session` — rather than retrying the same call.
- `hook.session.initiative` means the branch is a governed initiative, where no work/Jira selection applies.
- `copilot.turn-complete` carries the stop reason. A turn that completed with no proposal is a real outcome, not a pending one; say so and look for a nearby `copilot.permission-denied` or `copilot.error` that explains it.
- `log.unreadable` is a truncated final line, normal when a process died mid-write. Treat it as evidence of a crash.

## Reporting rules

Quote the `event`, the timestamp, and the message verbatim for the entries that
matter, and summarize the rest. Never invent an entry, never describe a log you
did not read, and never claim a cause the log does not support — say what is
missing and how to capture it instead.

The log is machine-local under `.git/singularity-flow/logs/` and is never
committed, so it is safe to read but it is not shared evidence: do not cite it as
governance or approval evidence for a phase.

Secrets are already redacted before anything is written. If a value still looks
like a credential, report the field name only and never repeat the value.
