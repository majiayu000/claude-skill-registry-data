---
name: pr-splitter
description: Analyse an oversized pull request or proposed branch changeset and decompose it into smaller, dependency-aware, independently reviewable pull requests. Use when a PR is too large for effective review or when the user asks to split, stack, or repackage a feature branch without changing its final behaviour. Do not use for ordinary PR review or simple branch cleanup.
---

# PR Splitter

## Purpose

Turn one oversized PR into a coherent review series whose combined result is equivalent to the original changeset. Choose boundaries from product behaviour, architecture, data dependencies, and validation needs—not file counts or arbitrary line limits.

## Authorization Boundary

Treat analysis and execution as separate modes.

- A request to analyse, assess, plan, or propose a split is read-only. Do not create or push branches, open PRs, post comments, change the original PR, or rewrite commits.
- Create branches or PRs only when the user explicitly asks to perform the split. Confirm the repository, original PR or head branch, base branch, fork/canonical remotes, and whether the original PR should remain open as an umbrella.
- Never merge or close the original or child PRs unless separately authorized.
- Recheck authorization immediately before pushing branches, creating PRs, or editing the original PR description/comments.

## Establish the Changeset

1. Read repository instructions and inspect the clean/dirty state before changing anything.
2. Fetch the relevant remotes and resolve the exact base, PR head, merge base, and current remote commit IDs. Detect a head update before any later mutation.
3. Inspect PR title/body, reviews, linked issues, CI, commit history, diff statistics, changed paths, and repository ownership boundaries when available.
4. Define the canonical changeset as the base-to-head diff. Do not assume the commit sequence already represents good review boundaries.
5. Inventory behaviour, schema/migrations, generated output, configuration, tests, documentation, operational scripts, and every changelog or release-note entry. Map each entry to the behaviour it describes and identify cross-repository or unpublished-package dependencies.

## Design the Split

Read [references/decomposition-playbook.md](references/decomposition-playbook.md) when choosing boundaries or executing a split.

Build a dependency graph before proposing branches. Prefer slices that each have one clear purpose, a bounded blast radius, meaningful validation, and a reviewer who can understand the change without reconstructing later PRs.

Choose one topology:

- **Sibling PRs:** each branch targets the original base and is independently mergeable. Prefer this when slices are genuinely independent.
- **Stacked PRs:** each branch targets the preceding slice. Use this when schema, shared contracts, generated models, or foundational refactors must land first.
- **Hybrid:** independent sibling groups containing short internal stacks. Use only when it makes the dependency graph materially clearer.

Do not force independence by duplicating code, weakening tests, introducing temporary compatibility paths, or splitting generated output from its source definition. Avoid PRs that are only mechanical leftovers unless they are a legitimate prerequisite with their own validation.

## Analysis Deliverable

Before execution, present a decomposition plan containing:

- original PR/head/base and pinned commit IDs;
- recommended topology and why;
- ordered slice names and concise purposes;
- base branch and dependency for every slice;
- principal paths/behaviours included;
- migrations, generated artifacts, configuration, tests, docs, and a changelog allocation/reconciliation plan;
- validation required per slice;
- cross-slice risks and reviewer notes;
- coverage proof that every original change is assigned exactly once or intentionally superseded.

Flag slices that cannot safely be reviewed or merged independently. Prefer fewer coherent PRs over many tiny PRs.

## Changelog Allocation and Reconciliation

Treat changelog and release-note entries as semantic artifacts, not generic documentation. Allocate each entry to exactly one slice: the earliest child PR that fully delivers the behaviour described. A foundation slice must not claim behaviour that only becomes available in a later slice.

- For sibling PRs, each branch contains only entries for its independently delivered behaviour.
- For stacked PRs, each child diff against its immediate parent adds only that child's entries; merging the stack in order must produce every intended entry exactly once.
- Preserve the repository's release layout and conventions. Do not place new work in a historical released section.
- Consolidate incremental or duplicate wording into concise outcome-focused entries, without broadening claims beyond the slice.
- If a slice needs no changelog entry, record why in the plan or PR description rather than silently omitting it.

Before execution is complete, reconcile the aggregate changelog against the original changeset. Document any intentional wording, placement, deduplication, or omission as an approved metadata difference in the equivalence proof.

## Execute an Approved Split

1. Record all starting refs and verify the remote PR head has not moved.
2. Preserve tracked and untracked user work. Use isolated worktrees when practical.
3. Create predictably named branches from the exact approved base or parent slice. A useful pattern is `split/<ticket-or-pr>/<nn>-<purpose>`.
4. Reuse whole commits only when they already match a slice. For tangled commits, repartition the diff semantically; do not preserve poor commit boundaries at the cost of poor PR boundaries.
5. Keep migrations with the first code that requires them, generated artifacts with their source/schema change, tests with the behaviour they prove, and changelog entries with the slice that fully delivers the described outcome.
6. Validate each slice against its declared base before pushing. A stacked child must be tested with its parent applied, not against the ultimate base alone.
7. Compare the final reconstructed stack/group against the original head. The aggregate tree and intended behaviour must match, except for explicitly documented cleanup approved by the user. Reconcile the aggregate changelog so intended entries appear once, in the correct release section, with no split-induced duplicates or contradictory wording.
8. Push only approved split branches. Use leases for any rewritten remote branch and never overwrite the original PR head unless explicitly requested.
9. Create child PRs with concise descriptions that state purpose, dependency/base, scope, validation, and `Part N of M` linkage to the original PR.
10. Link every child from the original umbrella PR and every child back to the umbrella. For stacked PRs, also link the immediate predecessor/successor and state the required merge order.

## Completion Gate

Do not call the split complete until:

- every original changed path and semantic change is accounted for;
- every original changelog/release-note entry is assigned exactly once, or its supersession, consolidation, or omission is explicitly justified;
- each child changelog describes only behaviour delivered by that child, and the aggregate contains the intended entries exactly once in the correct release section;
- each child diff is reviewable against its actual base;
- required tests and repository checks pass or failures are precisely documented;
- branch targets and PR dependencies are correct;
- no temporary files or unrelated working-tree content entered a branch;
- remote child refs match local heads;
- all PR links are reciprocal and the original PR clearly acts as the umbrella;
- the original PR remains unmerged/open unless the user explicitly requested otherwise.

Report created branches/PRs, topology, validation, equivalence evidence, CI state, preserved local files, and remaining merge-order or rollout risks.
