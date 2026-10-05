---
name: harness-ralph-loop
description: "Runs iterate-until-pass loops with ralph-worker agents in a worktree. Use when running [ralph]-marked tasks or looping until verify passes."
when_to_use: "ralph task, loop until pass, iterate until tests pass, ralph mode, run ralph loop, [ralph] task"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Task", "Skill"]
argument-hint: "[task-id|help|--max-iter N|--verify CMD]"
model: sonnet
effort: high
user-invocable: false
---

# Harness Ralph Loop

Iterative-loop orchestrator for `[ralph]`-marked Plans.md tasks.
Spawns a fresh `harness:ralph-worker` subagent per attempt inside a single persistent worktree,
runs the Verify command authoritatively, and loops until both the `<promise>` text tag and verify exit 0 agree.

## Quick Reference

| Subcommand / Argument | Behavior |
|---|---|
| `help` | Print usage, philosophy, and link to prompt-best-practices.md |
| `<task-id>` | Run the loop for a Plans.md task that has `[ralph]` marker |
| `--max-iter N` | Override MaxIter (default: 10) |
| `--verify CMD` | Override the Verify command from the task |

## Execution Flow

See [`references/loop-flow.md`](${CLAUDE_SKILL_DIR}/references/loop-flow.md) for the complete orchestrator pseudocode.

Summary: On iteration 0 the orchestrator spawns a `ralph-worker` with `isolation="worktree"` to create the persistent worktree, capturing `RALPH_WORKTREE` from `result.worktreePath`. For iterations 1..N it fetches the `EnterWorktree` deferred-tool schema via `ToolSearch`, calls `EnterWorktree(path=RALPH_WORKTREE)`, then spawns the next worker without the isolation param. After each iteration the orchestrator runs the Verify command itself (anti-tamper), compares the exit code against `ralph-worker-report.v1.verify.exit_code`, scans the final assistant message for `<promise>…</promise>`, and diffs the worktree to detect stuck iterations. The loop terminates on success or on any of the three hard-stop failure modes (FT-RALPH-01 STUCK, FT-RALPH-02 VERIFY-MISMATCH, FT-RALPH-03 MAX-ITER).

## Help Subcommand

Running `harness-ralph-loop help` prints the following:

1. **Overview** — harness-ralph-loop is an iterative-loop orchestrator that spawns a fresh
   `ralph-worker` subagent per attempt inside a single persistent worktree, runs the Verify
   command authoritatively, and loops until both the `<promise>` text tag and verify exit 0 agree.

2. **Philosophy bullets:**
   - **Iteration > Perfection** — let the loop refine; don't aim for perfect on the first try
   - **Failures Are Data** — deterministically bad means tunable; each failure leaves context
   - **Operator Skill Matters** — prompt quality is the primary lever, not model strength
   - **Persistence Wins** — keep trying; the loop handles retry logic automatically

3. **Prompt guidance pointer:**
   For full prompt-writing guidance see [`prompt-best-practices.md`](${CLAUDE_SKILL_DIR}/references/prompt-best-practices.md)

4. **Task-pattern fit pointer:**
   For task-pattern fit see [`when-to-ralph.md`](${CLAUDE_SKILL_DIR}/references/when-to-ralph.md)

## When to Use Ralph

See [`references/when-to-ralph.md`](${CLAUDE_SKILL_DIR}/references/when-to-ralph.md) for guidance on which tasks are Ralph-suitable and which are not.

## Reference Files

| File | Purpose |
|------|---------|
| [`references/loop-flow.md`](${CLAUDE_SKILL_DIR}/references/loop-flow.md) | Full orchestrator pseudocode, prompt template, decision matrix, terminal-state handling |
| [`references/when-to-ralph.md`](${CLAUDE_SKILL_DIR}/references/when-to-ralph.md) | When to use Ralph (task patterns, DoD quality checks) |
| [`references/prompt-best-practices.md`](${CLAUDE_SKILL_DIR}/references/prompt-best-practices.md) | Prompt writing best practices (A1–A4), philosophy bullets, learn-more links |

## Related Skills and Agents

- `harness-plan` — Emits `[ralph]` marker + `Verify:` line for suitable tasks
- `harness-work` — Detects `[ralph]` marker and routes to this skill
- `harness:ralph-worker` — The per-iteration worker agent this skill dispatches
