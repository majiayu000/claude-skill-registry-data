---
name: diff-driven-docs
description: Treat documentation as a first-class deliverable of every BUILD phase. Classify the diff's doc impact across 3 layers (business/technical/audit) and write only the updates genuinely needed. Use after BUILD completes, before a commit/PR, or when asked "are docs up to date".
---

# Diff-Driven Docs

Stale documentation is worse than no documentation — it actively misleads. This skill treats docs as a deliverable of every code change, not an afterthought. Just as TDD enforces tests accompany code, diff-driven-docs enforces doc updates accompany changes before the workflow closes.

## Step 1: Run the impact classifier (BEFORE any doc work)

Read the diff. Classify impact across 3 layers:

| Diff characteristic | Business | Technical | Audit |
| --------------------- | -------- | --------- | ----- |
| Internal utility / helper / type only | SKIP | CHECK | SKIP |
| Test addition, no new pattern | SKIP | SKIP | SKIP |
| Style / formatting change | SKIP | SKIP | SKIP |
| Dependency version bump (no API change) | SKIP | SKIP | SKIP |
| Routine bug fix (existing behavior corrected) | SKIP | CHECK | SKIP |
| Simple refactor (behavior unchanged) | SKIP | CHECK if signatures changed | SKIP |
| New exported function / hook / component | SKIP | CHECK | CHECK |
| New page or route | CHECK | CHECK | CHECK |
| Architectural pattern introduced | SKIP | CHECK | CREATE |
| Technology choice made | SKIP | CHECK | CREATE |
| Breaking change to public API | CHECK | CHECK | CREATE |
| Permission or role change | CHECK | CHECK | CHECK |
| Security or compliance impact | CHECK | CHECK | CREATE or UPDATE |

**SKIP business docs if:** no user-facing surface changed; only internal utils/types/tests modified.
**SKIP audit docs if:** routine bug fix, style change, test addition, or simple refactor with no new pattern.
**ALWAYS check technical docs** when hooks/components/migrations/schema/routes/exported APIs changed.
**CREATE an audit doc if:** an architectural decision was made, a new pattern introduced, a non-obvious tradeoff accepted, or a dev six months from now would ask "why did we do it this way?"

**If all three layers are SKIP:** set `IMPACT_LEVEL: none` and emit a SKIPPED note immediately without opening any doc files.

## Step 2: Write only the needed updates

### Business layer

User-facing docs (README, user guide, changelog). Only when the user experience changed.

### Technical layer

API references, architecture docs, code comments, CONTRIBUTING. Update when signatures, exports, patterns, or integration points changed.

### Audit layer

ADRs (`docs/adr/`), decision records, postmortems. Create when a decision was made or a tradeoff accepted — the "why" that isn't obvious from the code.

## Step 3: Verify the docs match the code

After writing, re-read the changed doc section against the actual diff. A doc that says "X now does Y" when X still does Z is worse than no doc. If you can't verify, flag it rather than guess.

## Don't

- Don't write docs for SKIP-classified diffs — that's noise.
- Don't update docs that didn't change — you'll create drift.
- Don't skip the classifier and "just check everything" — that's how docs rot from over-touching.
- Don't leave a `## TODO` in the doc — either write it or don't.
