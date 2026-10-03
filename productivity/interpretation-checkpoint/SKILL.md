---
name: interpretation-checkpoint
description: For tasks touching 2+ files AND changing 2+ distinct parameters/aspects — show a structured Files/Changes/Assumptions/Non-goals breakdown for correction before editing. Skip when it's one change mechanically repeated across many files.
---

# Interpretation Checkpoint — Verify the Read Before Writing

`intent-capture` pins *what* was asked; `plan-first` decides *how*. Neither catches drift in the fine detail — the exact values, files, and parameters I inferred from a clear request. On wide-blast-radius tasks that drift is expensive to discover after the edit; this catches it before.

## Self-improvement (do this first and last)
1. **At start:** read `learnings.md` in this skill's folder if it exists. Apply relevant lessons.
2. **At end of every use:** append one dated bullet — did this catch real drift, or fire on a task that didn't need it? Merge instead of duplicating; delete disproven bullets.

## When it applies
Both must be true:
- **Files affected: 2+**
- **Distinct parameters/aspects changed: 2+** (not the same single change applied identically across files — e.g. a site-wide rename is 1 parameter regardless of file count)

Runs after `intent-capture`/`plan-first` (once goal and approach are settled), before the first Edit/Write. Below this threshold, the regular flow catches mistakes cheaply enough — skip straight to the work.

## The format
```
Files: <path> — <why it's touched>
Changes: <param/aspect> → <specific value or behavior intended>  (one line per distinct change)
Assumptions: <anything inferred rather than stated>
Non-goals: <adjacent things deliberately left alone>
```

Present this, then wait for correction or confirmation before editing — a single-turn round trip, not a full plan-mode detour.

## Rules
- **List real files** (checked via glob/grep), not a guess from memory.
- **One line per distinct change** — if there's only one after listing them out, this skill didn't need to fire; say so and proceed.
- **Assumptions must be visible**, not folded silently into Changes — that's the whole point of the checkpoint.
- Not a substitute for `plan-first`'s Approach/Verify-by — this only checks the parsed detail, not the strategy.

## Failure mode this prevents
A multi-file, multi-parameter change built correctly against a misread detail (wrong value, wrong file, wrong scope) — discovered only after generation, when the fix costs a redo instead of a one-line correction.
