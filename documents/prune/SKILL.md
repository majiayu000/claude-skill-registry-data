---
name: prune
description: Condense the repo's markdown docs back to convention and sweep the skill registry for dead entries. Trigger on:- prune, housekeeping, the docs have crept, review the skill registry, audit a skill, why isn't my skill triggering.
disable-model-invocation: true
allowed-tools: Read, Edit, Bash
model: claude-sonnet-4-6
---

# Prune

Condenses the markdown docs and puts them back on convention, and sweeps the skill
registry. Git is the real archive — nothing here is lost by being cut.

## When to use this

- Periodic housekeeping; not gated on any other skill finishing.
- Skip if the docs are already within the thresholds below — the checks are cheap, the
  rewrites are not.

## Each doc's job

| File | Holds |
|---|---|
| `README.md` | how to run it |
| `CLAUDE.md` | invariants |
| `docs/COMPLETE_ACTIONS.md` | append-only log |
| `docs/plans/*` | `NNN-short-slug.md`, zero-padded, never reused — `NNN` is the chronological id |

Content in the wrong file gets moved to the right one, not deleted.

## Steps

1. **Survey before proposing.** Line counts, plan count, and any file that doesn't match
   the naming convention.

   ```bash
   wc -l README.md CLAUDE.md docs/COMPLETE_ACTIONS.md
   ls docs/plans/
   ```

2. **Apply the thresholds.**
   - `docs/COMPLETE_ACTIONS.md` over 300 lines → compress everything older than the last
     3 entries to one line per entry. Never drop an entry entirely.
   - More than 10 plans in `docs/plans/` → move the oldest to `docs/plans/archive/`,
     leaving open and unstarted plans where they are. The index row stays in
     `docs/plans/README.md`; archiving is not a status change.
   - Any plan not named `NNN-short-slug.md` → rename it and update every reference in the
     other markdown files.

3. **Remove what's redundant or outdated** — content the code now contradicts, or that a
   later entry supersedes.

4. **Remove closed reviews** — `specs/*/review.md` with `status: closed` whose plan is
   already `implemented`.

5. **Sweep the skill registry** (`skills/README.md`). This is the tooling **as
   written** — file-level checks only. For the tooling **as used** (which skills
   actually fired, where sessions stalled), that is `/observer`, which reads
   transcripts; don't duplicate it here. Read every row and flag any skill or
   agent that is:
   - not referenced in `docs/skill-workflow.md`'s pipeline map **and** not tagged
     `overlay` or `utility` — an orphan;
   - `last-reviewed` older than 90 days — stale, needs a look;
   - over the ~120-line size smell in its `SKILL.md` (`wc -l`);
   - overlapping another `core` skill per the Overlap check in `skills/README.md` — flag
     the pair for consolidation.

   Present the flags. On a confirm-keep, bump that row's `last-reviewed` to today. Delete
   a skill only on explicit confirmation.

6. **Deep-audit a single skill** — when the run names one `skills/<name>/SKILL.md` rather
   than the whole registry, additionally check, citing `SKILL.md` line numbers with a
   severity on each finding:
   - **Safety** — `allowed-tools` / `tools` wider than the Procedure uses; a destructive
     or outward-facing action (delete, force-push, send, deploy) with no confirmation
     step.
   - **Triggering** — if the complaint is "it doesn't fire", compare its `description`
     trigger phrases against the request that failed *and* against sibling skills'
     triggers for a collision that routes elsewhere.
   - **Standard** — section order, constitution restatement, size smell, per the
     authoring standard in `skills/README.md`.
   Report findings; apply fixes only on confirmation, same as the registry sweep.

7. **Present the proposed actions as a list and get confirmation before touching
   anything.** This skill rewrites history-shaped files; it doesn't do that unasked.
  

## What not to do

- Don't delete a `COMPLETE_ACTIONS` entry or a plan file — compress and archive instead.
- Don't renumber a plan, ever, including an abandoned one.
- Don't move content into `CLAUDE.md` that isn't an invariant; it is not a changelog.
