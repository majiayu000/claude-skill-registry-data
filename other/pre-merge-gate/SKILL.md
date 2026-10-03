---
name: pre-merge-gate
description: Self-check a change against loaded standards before handoff or commit — diff scoped to files actually touched. Trigger before "done," "ready for review," a commit, or a role-session handoff.
---

# Pre-Merge Gate — Check Your Own Diff Before Handing It Off

A change that violates a standard it was written under is cheaper to catch now than after a dev's review cycle finds it. This is the author's own check, not a substitute for that review.

## Self-improvement (do this first and last)
1. **At start:** read `learnings.md` in this skill's folder if it exists. Apply relevant lessons.
2. **At end of every use:** append one dated bullet — a violation this caught before handoff, or a rule that produced a false flag. Merge instead of duplicating; delete disproven bullets.

## Rules
1. **Scope is exactly the files edited this task** — in `role-session` parallel mode, exactly the files in your own lock rows in `handover/locks.md`. Never a whole-tree `git diff`, never another role's rows.
2. **Re-open the applicable standard for each changed file and check the diff against it directly** — not from memory of having followed it while writing. For application code, that's the `coding-standards` skill's layer resolution; for a skill/`SKILL.md` file itself, that's `skill-writer.md`'s review checklist.
3. **Flag violations as a numbered `file:line` list.** Do not silently fix anything outside the task's stated scope — surface it and ask (per AI-12: don't invent rules; the same discipline applies to inventing scope).
4. **Output is pass/fail per rule, not prose.** "3 checked, 1 flagged: `card.css:42` — hardcoded color, standard requires a token" beats a paragraph saying the same thing.
5. **This gate is a self-check, not the review.** In `role-session` mode it runs before flipping your lock rows to `awaiting-review` — it never replaces the dev's actual approval step.

## When it applies
Before any of: a commit, saying the task is done, a `role-session` handoff to `awaiting-review`. Skip it only when nothing was changed against a standard the project actually enforces (e.g. a pure prose answer, no edits).

## Failure mode this prevents
A standards violation surviving to review or merge because the author's own pass over the diff never happened — caught late, it costs a review round-trip; caught here, it costs one pass over a diff already open.
