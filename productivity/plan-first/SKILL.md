---
name: plan-first
description: For tasks touching 3+ files or ambiguous scope — enumerate files, ≤5-line plan, confirm, execute without pausing. Trigger before multi-file features, refactors, redesigns, or tasks with two plausible interpretations.
---

# Plan First — Cheap Insurance Before Expensive Runs

A wrong interpretation on a big run wastes the whole run. Five lines of plan costs ~100 tokens and catches it before execution.

## Self-improvement (do this first and last)
1. **At start:** read `learnings.md` in this skill's folder if it exists. Apply relevant lessons.
2. **At end of every use:** append one dated bullet — did the plan catch a misinterpretation? Was planning overhead wasted on a task too small for it? Merge instead of duplicating; delete disproven bullets.

## When it applies
- Task will touch **3+ files**, OR
- The request has **two plausible interpretations**, OR
- The work is **destructive/hard to reverse** (schema changes, deletions, rewrites).

Below that threshold: just do the work. Planning a one-file edit is its own waste.

For genuinely ambiguous intent specifically (two+ readings, no stated success condition), run `intent-capture` first — its Goal/Constraints/Done-when feed this plan's Approach line.

## The format (hard cap: 5 lines + file list)

```
Plan: <one-sentence goal as I understand it>
Approach: <the how, 1–3 lines — the decision points, not the obvious steps>
Files: <path> (new|edit|delete) — <one clause each>
Won't do: <adjacent things deliberately out of scope, if any>
Verify by: <how I'll prove it works>
```

Then: "Proceeding unless you redirect" for routine work, or an explicit question when a genuine fork exists (present the fork as 2 options with a recommendation, not an open question).

## Rules
- **Enumerate files by actually checking** (glob/grep), not from memory — the plan's value is that it's grounded.
- **One plan, then execute without pausing.** No re-asking permission at each step; the plan WAS the permission. Stop mid-run only for scope changes or destructive surprises.
- **"Won't do" is load-bearing** — it's where scope creep and over-engineering get declined in advance.
- If execution reveals the plan was wrong, say so in one line and state the correction — don't silently diverge.
- Plans are not deliverables: no headers, no prose padding, no restating the user's request back at length.
