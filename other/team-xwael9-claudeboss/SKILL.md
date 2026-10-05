---
name: team
description: Delegate a task to a free opencode agent, wait for its output, then review and implement it together with the user. Use when the user says "team mode", "/claudeboss:team", or wants Claude Code and opencode working as a pair on a task.
metadata:
  origin: ClaudeBoss
---

# ClaudeBoss — Team Mode

You (Claude Code) and a free opencode agent work as a pair on one task. Opencode does the first pass; you review it like a second engineer would, then implement/finish it yourself.

> **Drift-prone.** Free model catalogs (OpenCode Zen, OpenRouter) change without notice. Model selection happens live via `opencode models` every run — never assume a specific model id still exists.

## Prerequisites

Run once per machine: `claudeboss install` — checks/installs the `opencode` CLI, verifies a free model is reachable, and prints manual OpenRouter fallback steps if not (no automated account creation, by design).

## Workflow

1. **Classify the task** into one of: `code`, `write`, `research`, `general` (use `/claudeboss:plan` instead, first, if the task itself is "figure out the right approach"). Coding tasks (features, fixes, refactors) → `code`. Prose/docs/copy → `write`. Fact-finding/comparison → `research`. Anything else → `general`.

2. **Delegate.** Run:
   ```bash
   claudeboss run <task-type> "<precise task description — same detail you'd give a human contractor>"
   ```
   This is a blocking call — wait for it to return, don't poll.

3. **Review the output like a code review, not a rubber stamp.** Check:
   - Does it actually satisfy the request, not just look plausible?
   - Correctness — run tests/typecheck/lint if applicable, read the actual diff, don't trust a summary of it.
   - Fit with the existing codebase's conventions.

4. **Implement.** You apply the result yourself — edit files with Edit/Write, run verification (tests, the `run` skill, a browser check for UI), and fix anything opencode got wrong or left incomplete. Treat its output as a first draft from a teammate, not a final answer.

5. **If opencode's draft is unusable** (wrong approach, missed the point), don't loop forever — after 2 failed delegations, tell the user directly and offer to just do the task yourself. Free models are weaker than you; don't over-trust them on hard problems.

## What this mode is NOT

Not autonomous. You still show your work and changes to the user like any other task. Team mode changes *who writes the first draft*, not the review/verification bar.
