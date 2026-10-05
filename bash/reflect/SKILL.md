---
name: reflect
description: Per-project self-improvement - reads the .harness ledger and feedback memories, then proposes gated rule/threshold/ADR changes so the project stops repeating mistakes. Run periodically.
user_invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Reflect: Per-Project Self-Improvement

You are performing a reflection - turning the signal this project has captured
into durable improvements. Nothing is applied without the developer's approval.

## Phase 1 - Orient (gather signal)

- Run the stats script over the ledger:
  `~/.claude/hooks/harness-ledger-stats.sh --ledger .harness/ledger.jsonl --min-recurr 3`
  If that path doesn't exist, the hooks aren't installed at `~/.claude/hooks/` - run the
  copy from wherever this project keeps them. If the script prints all zeros there is no
  ledger yet (no signal captured) - stop; there is nothing to reflect on.
- Read the current project rules in `CLAUDE.md` so you improve them rather than duplicate.
- Read recent `feedback`-type memory files - these are the developer's explicit
  corrections and are the highest-value signal. Locate the memory directory first
  (it sits next to `MEMORY.md`; `find . -name MEMORY.md` if unsure), then
  `grep -l 'type: feedback' <memory-dir>/*.md`.
- Read the most recent `.harness/reflections/*.md` report (if any) to recall the last
  metric snapshot and what was already changed.

## Phase 2 - Cluster

From the stats output and feedback memories, identify recurring problems:
- Each `recurring <rule> <prefix> <count>` line is a friction cluster - the same check
  keeps firing in the same area.
- Group related feedback corrections by theme.
- Ignore one-off events; focus on what repeats.

## Phase 3 - Propose (one candidate per cluster)

For each cluster, draft exactly one proposed change, choosing the fitting type:

| Type | When | Where it lands |
|------|------|----------------|
| **Project rule** | a convention would stop the repeat | append to `CLAUDE.md` project-specific section |
| **Threshold change** | a guardrail is too strict/loose | a diff to `.claude/settings.json` or the hook - **shown, never auto-applied** |
| **Lint rule** | the mistake is mechanically catchable | a diff to `eslint.config.mjs` / `biome.jsonc` |
| **ADR / knowledge** | durable "why" worth keeping | a new memory file or `docs/adr/` note |

Present all proposals together as a numbered list with the concrete change for each.

## Phase 4 - Gate & Record

- Ask the developer to approve, edit, or reject each proposal (like `/remember`).
- Apply only the approved ones, then commit them (use `/commit`).
- Create `.harness/reflections/` if needed (`mkdir -p .harness/reflections`), then write a
  reflection report to `.harness/reflections/YYYY-MM-DD.md` containing:
  - the full stats output (the **metric snapshot**, so the next reflection can compare),
  - the clusters you found,
  - which proposals were approved / rejected and why.

The report is committed; the raw `.harness/ledger.jsonl` stays gitignored. Signal is
private; wisdom is shared.

## Measuring success

The headline metric is `recurring_events` from the stats output. Compare it to the value
in the previous reflection report. If a rule you promoted last time worked, the cluster it
targeted should have shrunk. Note the trend explicitly in the new report.
