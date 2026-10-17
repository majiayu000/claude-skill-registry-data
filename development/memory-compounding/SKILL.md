---
name: memory-compounding
description: Review and sharpen persistent memory so it compounds instead of accumulating. Use when pruning pi-hermes-memory entries, doing monthly memory hygiene, or when the same lesson has been recorded multiple times.
---

# Memory Compounding

Memory is an index, not a transcript. Without review it accumulates stale entries that mislead future work. This skill is the discipline for keeping memory **sharp**, not just large.

## When to use

- Monthly memory hygiene (AGENTS.md: "review both, prune stale entries").
- You notice the same gotcha recorded 3+ times.
- A memory entry contradicts the current code (trust the code).
- After a non-trivial debug/build cycle that produced a reusable learning.

## The 5-outcome review rubric

For each entry in `~/.pi/agent/pi-hermes-memory/MEMORY.md`, `USER.md`, `failures.md`, and the SQLite `memories` table (via `memory_search`), apply exactly one outcome:

| Outcome | When | Action |
| -------- | ---- | ------ |
| **Keep** | Accurate + useful | Leave as-is |
| **Update** | Correct but incomplete | Add the missing detail |
| **Consolidate** | Same lesson appears multiple times | Merge into one entry, remove duplicates |
| **Replace** | Outdated or superseded by current code | Replace with the current truth |
| **Delete** | No longer applies (framework changed, code removed) | Remove |

## The promotion rule

When the **same gotcha appears 3+ times** in `failures.md` or across memory entries, promote it: write a dedicated reference file or a new skill section. A lesson that keeps recurring is a pattern, not a one-off — it earns a permanent home.

## Solution docs (durable cross-project learnings)

After any non-trivial debug/build cycle, evaluate whether to write a solution doc to `docs/solutions/`:

- **Write** if: the problem took 3+ hypotheses to solve, OR the bug pattern appears in 3+ files, OR the solution contradicts a common assumption.
- **Skip** if: the fix was mechanical (typo, import error, one-line change).

Solution doc format:

```
# [Problem Title]
Category: debugging | architecture | testing | workflow | conventions
Tags: [comma-separated]
Date: YYYY-MM-DD
## Problem
[symptoms, not just the error message]
## What Didn't Work
[failed hypotheses and why]
## Solution
[what worked — with code example]
## Why
[the underlying principle]
## Prevention
[how to prevent this class of problem]
```

Ensure `AGENTS.md` or `CLAUDE.md` points to `docs/solutions/` so agents can find it. This closes the loop: every solved problem makes the next one easier.

## Don't

- Don't persist: whole diffs, verbose logs, celebratory narration, "looked correct" without evidence, duplicate notes, raw secrets/PII.
- Don't delete a memory just because it's old — delete it because it's **wrong now**.
- Don't skip the review when memory contradicts the code — trust the code, fix the memory.
