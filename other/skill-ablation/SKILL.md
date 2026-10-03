---
name: skill-ablation
description: Periodically archive CLAUDE.md/skills/hooks, run real work with none of it, restore only what proves missing. Trigger on "ablation", "delete protocol", "run bare", "prune skills", a major model upgrade, or ~6 months since last run.
---

# Skill Ablation — Prove the Scaffolding Still Earns Its Keep

`memory-gardener` prunes bloat inside instructions that stay. This skill tests whether an instruction should exist at all — a periodic ablation pass, not continuous pruning. A skill under the line cap can still be 100% obsolete; only removing it and watching for a real stumble proves that.

## Self-improvement (do this first and last)
1. **At start:** read `learnings.md` in this skill's folder if it exists. Apply relevant lessons.
2. **At end of every use:** append one dated bullet — which instruction turned out obsolete, which was proven load-bearing, any restore that took more than one stumble to justify. Merge instead of duplicating; delete disproven bullets.

## When to run
- The project's primary coding-agent model changed (new major version, new vendor default).
- ~6 months since the last ablation run, or never run.
- The user invokes it by name, or a `memory-gardener` pass finds the same instruction repeatedly untouched.
Never run mid-task — this needs a clean session boundary, not a mid-edit interruption.

## Procedure

### 1. Archive, don't delete
Move the project's `CLAUDE.md`, `.claude/skills/`, and any hooks config into a dated archive folder (e.g. `.ablation-archive/<date>/`), not the trash. State the archive path before continuing — this is the undo path if the bare run goes badly.

### 2. Run bare, for real work only
Start the next session with none of it loaded. Do **not** pre-guess which instruction the model will need back — that defeats the test. Work the actual backlog (real tasks, not synthetic ones) for a defined window: a handful of real sessions, or ~1 week of normal use, whichever the user prefers.

### 3. Log every stumble, don't fix it inline
Each time the model does something a deleted instruction would have prevented — wrong convention, skipped step, repeated question — log it in a scratch note: what happened, which archived file would have caught it. Do not restore yet. One stumble is noise.

### 4. Restore only on repeated evidence
After the window, scan the stumble log. Restore an instruction only if the **same** stumble appears **3+ times** across independent sessions/tasks. Everything else in the archive stays archived — it's confirmed dead weight, not "might need it later." State the count when restoring: "`X` stumbled on Y in 3 of 5 sessions → restoring."

### 5. Rewrite restored instructions lean
A restored instruction is a chance to fix it, not just copy it back verbatim — cut anything the stumble log shows the model didn't actually need, per the `skill-writer` quality bar (checkable rules, hard caps, no restated prose).

### 6. Report and archive the log
Summarize: kept archived (count), restored (count + evidence), any skill rewritten during restore. Fold the stumble log into this skill's `learnings.md` as dated bullets, then delete the scratch copy — the log itself is not worth keeping once distilled.

## Relationship to other skills
- **`memory-gardener`** prunes and merges what stays; this skill decides what stays at all. Run gardener first if a learnings/handover file is over its cap — no point ablating bloat that's about to be pruned anyway.
- **`skill-writer`**'s quality bar governs anything rewritten during restore (step 5).
- Tool-agnostic by design: "archive the skills folder / CLAUDE.md / hooks config" works the same in Claude Code, OpenCode, or any markdown-driven agent — no tool-specific ablation switches required.

## Hard rules
- Never restore on a single stumble — the 3+ threshold is not a suggestion.
- Never skip the archive step — deleting outright removes the undo path and the evidence trail.
- Never run the bare window on synthetic/toy tasks — it must be real backlog work or the result doesn't generalize.
