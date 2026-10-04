---
name: aa-commit-clarity
description: Decide whether a mixed diff is one commit or several. Use when the user asks how to commit a change, whether it's one commit or many, or to split a diff up — and before `commit-me` on a large or multi-concern change.
---

# Commit Clarity

Advisory only — recommends commit boundaries, then hands off to `commit-me`. Reach for it when a diff spans more than one obvious concern.

## 1. Read the actual diff

`git status`, then `git diff` — for large diffs, `git diff --stat` for the shape, then read the concerning hunks in full. Ground the verdict in hunks, not file names: files can look related and hide unrelated edits, or look unrelated and be one cohesive change. **Done when** you've read every hunk that could carry an independent concern — not just the file list.

## 2. The "and also" test

**Can the whole diff be honestly described in one imperative sentence with no "and also"?**

- Yes → one commit.
- No → the "and also" marks the seam; split there.

"Honestly" is load-bearing — don't let an awkward conjunction pass as a single sentence. This decides most diffs on its own. The lenses below are only for when the sentence is genuinely ambiguous.

## 3. Lenses (only when the "and also" test is unclear)

- **Separability** — independent concerns (refactor + feature, behavior + formatting, infra + product)? Could a subset revert on its own without breaking intent?
- **Narrative** — would the history tell a future reader *why* each change exists? Does splitting clarify the story, or shatter one that reads better whole?
- **Hygiene** — mechanical noise (renames, formatting, generated output) mixed with semantic change? A preparatory refactor that would be clearer alone?
- **Coupling guard** — changes meaningless in isolation belong together. **Don't split unless it improves understanding or safety**; splitting coupled changes only manufactures broken intermediate commits and harder bisects.

## Calibration

- Refactor across 30 files **+ an unrelated one-line bugfix** → split; the bugfix reverts on its own.
- Rename a function across all its call sites → single; the call sites are meaningless without the rename.
- Feature **+ the refactor that enabled it** → judgment call. Split if the refactor stands on its own merits; single if it only makes sense in service of the feature.
- Whole-file formatting **+ one semantic change** → split; the change drowns in the noise.
- Feature **+ its tests** → single; the tests are part of the feature.
- One feature across migration + types + API + UI + tests → single; every file serves "add X to Y." Per-file splits manufacture broken commits.

## Output

Lead with the verdict: **"Single commit"** or **"Split into N commits"**, then a short rationale.

If splitting, give each commit the files (or hunks) it owns and a one-line conventional-commit title.

Stay on commit strategy — don't propose code changes unless the structure depends on it (e.g. formatting noise must be reverted before `foo.ts` is a clean refactor commit).

## Handoff

Wait for the user to decide. On a split, hand each chunk to `commit-me` in turn, staging only that chunk's files — never `git add -A` — until the tree is clean. On a single commit, hand off once.
