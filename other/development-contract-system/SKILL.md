---
name: development-contract-system
description: Build a portable change-contract system for any repository. Use when creating or porting a repository workflow based on tracked feature records, lifecycle directories, a policy file, a checker, a lifecycle transition helper, and aligned docs/tests.
---

# Development Contract System

Use this skill when a repository needs a deterministic, reviewable workflow for
tracking substantive work through repo-owned feature records instead of ad hoc
notes.

This skill is self-contained on purpose so it can be moved into another repo or
skill collection without depending on the smaller contract skills from this
frame at runtime.
When the target repo uses local skills, generate a thin overlay with its concrete
policy and helper commands. Reference `development-contract-process` only when
the target agent has that skill; otherwise include the minimum operator flow.

Build or port the system only within the requested scope. Review and design
requests return findings or a draft without creating policy, records, helpers,
or new enforcement. Preserve an existing system until its migration is explicit.

## What this skill builds

A complete repository-local contract system with these parts:

- a repo-owned policy file
- a `feature_records/` directory with lifecycle subdirectories
- a Markdown template for new records
- a root `feature_records/README.md`
- a checker script that validates record structure and changed-path coverage
- a lifecycle transition helper script
- direct shell tests for the checker and lifecycle helper
- repo docs that explain how maintainers should use the system
- optionally, a repo-local process overlay skill that points at the concrete
  policy file, checker command, helper command, and validation profiles

Recommended default layout:

```text
config/change-contract-policy.sh
feature_records/
  README.md
  TEMPLATE.md
  planned/
  active/
  done/
  superseded/
scripts/check-change-contracts.sh
scripts/set-feature-record-lifecycle.sh
scripts/test-change-contracts.sh
scripts/test-feature-record-lifecycle.sh
```

Detailed policy fields, feature-record template sections, checker behavior,
helper behavior, test cases, and docs examples live in
[references/contract-system-implementation-details.md](references/contract-system-implementation-details.md).

## Use this skill when

- a repo needs tracked change contracts for substantive work
- maintainers need to see what is active, planned, done, or superseded at a glance
- the team wants explicit implementation and verification evidence
- the repo should remain deterministic even if agent-specific folders disappear
- you are porting this workflow from one repo to another

## Do not use this skill when

- the repo only needs a simple issue tracker or TODO list
- the team does not want repo-tracked process artifacts
- there is no appetite for maintaining a checker and template contract

## Core outcome

After this skill is applied, the repository should support this flow:

1. Substantive work requires a feature record update.
2. Feature records live under lifecycle folders:
   `planned/`, `active/`, `done/`, `superseded/`.
3. The record's folder must match its `## Lifecycle` `State`.
4. A checker validates structure, ownership, evidence, and lifecycle placement.
5. A helper script moves records between lifecycle folders and updates the
   lifecycle fields deterministically.
6. Repo docs explain the system clearly enough for maintainers who never use an
   AI assistant.

## Build order

Implement in this order to avoid drift:

1. Discover the repo's real substantive-change surface.
2. Create the repo-owned policy file.
3. Create the `feature_records/` tree and template.
4. Implement the checker against the policy file.
5. Add isolated lifecycle fixtures or migrate real records.
6. Add the lifecycle transition helper.
7. Add shell tests for the checker and helper.
8. If the repo uses local skills, add a thin overlay with concrete policy and
   commands, referencing the portable process skill only when it is available.
9. Update README, AGENTS-style docs, and release/hygiene docs.
10. Run the checker and hygiene lanes and fix drift.

## Phase 1: Ground in the repo

Before adding anything:

- read the repo's main README and agent or maintainer guidance if present
- identify the directories and top-level files that count as substantive
- identify existing validation commands
- identify whether the repo already has a tracked plans folder or release
  checklist
- identify whether the repo is CMake-first, Makefile-based, Cargo-based, npm,
  or another ecosystem so command examples fit the repo

Do not guess substantive paths if the repo already has clear boundaries in docs,
workflows, or layout.

## Phases 2-7: Build the contract mechanics

Use
[references/contract-system-implementation-details.md](references/contract-system-implementation-details.md)
for the detailed policy surface, feature-record tree, template sections,
checker checks, lifecycle helper behavior, fixture guidance, and direct
test cases.

Keep these invariants in the main workflow:

- put the policy in a neutral repo-owned path such as `config/`, not under
  `.agents/`, when scripts, CI, or humans depend on it
- make the policy the single source of truth for substantive paths, lifecycle
  values, required sections, evidence lanes, checker command, and validation
  profiles
- keep feature records in lifecycle subdirectories whose names match each
  record's `Lifecycle` `State`
- make the checker validate both changed-path coverage and record structure
- make the lifecycle helper update fields and move files deterministically
- add direct tests for checker and helper behavior before calling the system
  complete

## Phase 8: Add a repo-local process overlay when the repo uses skills

If the target repository keeps project-local skills, generate a thin overlay
that:

- names the concrete policy file path
- applies `development-contract-process` when installed, or includes a concise
  operator flow when that skill is unavailable
- names the checker command and lifecycle helper command
- points at the repo policy's validation profiles
- avoids restating schema details already enforced by policy and checker

Do not generate this overlay when the repo does not use local skills. The repo
must remain usable for humans and scripts without any skill dependency.

## Phase 9: Update docs

Update the repo docs so a human maintainer can use the system without the skill:

- main README
- AGENTS-style maintainer guidance
- release checklist or hygiene docs
- feature-records README

Use the lifecycle diagram example in the implementation-details reference when
the README needs a concrete visual. Always document the lifecycle helper
command explicitly.

## Decision rules

- Prefer repo-owned files under `config/`, `scripts/`, and `feature_records/`
  over agent-specific locations.
- Keep the policy file as the single source of truth for checker behavior.
- Keep the checker and lifecycle helper deterministic and local-first.
- Prefer a small explicit schema over a flexible but vague document format.
- Keep feature records as Markdown so they are easy to review in git.
- Keep lifecycle visibility obvious from the directory tree.
- Keep synthetic lifecycle examples in clearly labeled test fixtures or docs,
  excluded from live changed-path coverage. Only real records belong in active
  or completed work inventories; do not invent verifier evidence to seed them.
- When the repo uses local skills, keep the repo-local process overlay thin and aligned
  with the policy, checker, template, and docs.
- If the repo has a release checklist, point it at the checker and lifecycle
  docs.

## Final acceptance criteria

The system is complete when:

- the repo has a neutral policy file
- `feature_records/` exists with root docs/template and lifecycle subdirectories
- the checker enforces lifecycle and evidence rules
- the helper script performs lifecycle transitions deterministically
- direct tests exist for checker and helper
- if the repo uses local skills, the repo-local process overlay points at the concrete
  policy/checker/helper without duplicating schema literals
- repo docs explain the lifecycle model and helper commands
- the repo's hygiene or validation path includes the checker

## Output expectations

When using this skill, leave behind:

- the full repo-owned contract system
- isolated lifecycle examples or migrated real records
- tests that prove checker and helper behavior
- docs aligned with the system
- a concise summary of what was validated and what remains manual
