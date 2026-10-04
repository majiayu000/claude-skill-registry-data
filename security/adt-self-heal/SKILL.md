---
name: self-heal
description: Autonomous error recovery — detect failures, diagnose root cause, apply fixes, and resume without stopping
triggers:
  - self-heal
  - self heal
  - auto-recover
  - recover from error
  - retry
  - agent stuck
  - loop failure
---

# Self-Heal

Recover autonomously from failures. Diagnose before retrying — blind retries waste tokens and amplify mistakes.

## Recovery Decision Tree

```
Error detected
├── Transient? (network, rate limit, timeout)
│   └── → Retry with exponential backoff (max 3×)
├── Tool failure? (bad args, wrong schema)
│   └── → Fix args, retry once; if still fails → escalate
├── Logic error? (wrong output, assertion failure)
│   └── → Diagnose root cause → apply fix → verify → continue
├── Context overflow?
│   └── → Compress context → resume from last checkpoint
└── Unknown?
    └── → Log state, pause, surface to human
```

## Retry Rules

- **Transient** (HTTP 5xx, rate limit 429, network timeout): retry after 1s, 4s, 16s — then fail
- **Deterministic** (validation error, type mismatch): fix the root cause first — retrying without a fix wastes budget
- **Max retries**: 3 per error type per phase; consecutive failures in same phase → escalate tier or stop

## Checkpoint Pattern

Before any risky operation, save state so recovery can resume:

```text
.agents/plans/.loop-state.json
{
  "phase": "implement",
  "step": 3,
  "lastSuccess": "tests green on auth module",
  "pendingFiles": ["src/api/users.ts"],
  "checkpoint": "<ISO timestamp>"
}
```

On failure, reload checkpoint and skip completed steps — do not repeat work.

## Diagnose Before Fixing

Never patch without understanding:

1. Read the full error — stack trace, exit code, stderr
2. Reproduce in isolation (smallest failing case)
3. Form one hypothesis — what is wrong and why?
4. Test the hypothesis with a targeted check (log, assertion, type check)
5. Fix exactly what the evidence shows
6. Verify the fix resolves the error AND does not break adjacent tests

## Context Overflow Recovery

When context is exhausted mid-task:

1. Summarize completed work → 3–5 bullet points
2. Save summary + checkpoint to `.agents/plans/recovery-<timestamp>.md`
3. Start a fresh context with the summary as preamble
4. Resume from the last saved checkpoint

## Escalation Ladder

| Attempt | Action                                             |
| ------- | -------------------------------------------------- |
| 1       | Retry same tier                                    |
| 2       | Switch model within tier                           |
| 3       | Escalate to next tier (haiku → sonnet → opus)      |
| 4       | Pause — surface blocker to human with full context |

## What NOT to Auto-Heal

- Hard blocks: `rm -rf`, schema drops, force push to main
- Security failures: don't lower validation to make tests pass
- Ambiguous requirements: if the spec is unclear, ask — don't guess and continue

## Output

```text
Self-Heal Report
────────────────
Error:     <original failure>
Diagnosis: <root cause>
Action:    <what was done>
Attempts:  <N>
Outcome:   RESOLVED | ESCALATED | BLOCKED
Resumed:   <from checkpoint / from scratch>
```
