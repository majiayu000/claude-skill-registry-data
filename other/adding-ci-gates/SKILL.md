---
name: adding-ci-gates
description: Use when adding new CI checks or gates to a repository — batching several gate tickets onto one branch, deciding whether a gate ships now or is deferred, re-checking a gate design against the live main branch instead of a stale ticket snapshot, giving a new gate script a must-fail fixture, or handling bot-review findings on workflow files.
---

# Adding CI Gates

## Profile keys consumed

- `ci.provider`
- `ci.workflows`
- `ci.required_checks`
- `make.lint`
- `make.format`
- `framework.package_manager`

## Overview

A batch of new CI gates lands cleanly only when each gate is independent, is designed against the
live `main` branch rather than the ticket that requested it, and carries its own coverage. The
failure mode is a batch where two gates edit the same workflow, or where a gate was specified
against a make target that has since been split or renamed.

## When to use

- Several CI-gap tickets are being implemented onto one branch.
- A new workflow, a new CI gate script, or a new lint target is being added.
- A gate needs new infrastructure — a new image, cloud credentials, a new external tool.
- Bot reviewers (CodeRabbit, cubic) have commented on a workflow or Makefile change.
- Not for: diagnosing a gate that is already red — that is the
  [ci-infrastructure-failure-diagnosis skill](../ci-infrastructure-failure-diagnosis/SKILL.md), and
  for a refactor that only moves an existing gate between execution contexts, use the
  [ci-infrastructure-refactoring skill](../ci-infrastructure-refactoring/SKILL.md).

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — workflows in the paths listed by `ci.workflows`, gate scripts in the CI scripts
  directory, validated by dedicated workflow-syntax, workflow-security, and compose-validation
  lint targets that ride the aggregate mapped by `make.lint`.
- **Next.js app shape** (routed pages, no aggregate duplication gate): partial — same workflow and
  CI-script layout, but the only workflow-lint target is a workflow-security one; nothing lints
  workflow syntax or the compose files.
- **Component-library shape** (Storybook-first, no bootable app, published package): partial —
  same workflow and Bats-suite layout, but no workflow-lint make target, so workflow-syntax errors
  surface only on the runner.

## Procedure

1. **One gate, one ticket, one commit.** Split the batch so no two gates edit the same file. If two
   gates must touch the same workflow, merge them into a single ticket instead of interleaving
   commits. Isolation is what makes a bad gate revertable without unpicking the others.
2. **Re-verify against the live branch, not the ticket.** Read the current file before designing:

   ```bash # profile-example
   git fetch origin main
   git show origin/main:Makefile | grep -n '^test-unit'
   git show origin/main:.github/workflows/static-testing.yml
   ```

   Targets get split (a single test target becoming dev-side and prod-side phases), thresholds get
   tuned, and workflows get refactored between the ticket being filed and being worked. Read the
   workflows named by `ci.workflows`, the Makefile, and the CI scripts directory for a gate that
   already covers the space before adding a second one.

3. **Assess burn-down risk before committing to the batch.** A gate built on an existing pattern
   (one more target in the aggregate mapped by `make.lint`, one more Bats file) is low risk. A gate
   that needs a new Docker image, new cloud credentials, or a new threshold to be calibrated is
   high risk — land the cheap gates first and re-file the rest, rather than holding the batch open.
4. **Give the gate its own coverage.** A new make target needs a row in the repository's
   make-target coverage manifest and a Bats case that drives it; a new gate script needs a
   must-fail fixture proving the gate really fires. A gate with no failing fixture can pass
   vacuously forever.
5. **Apply the workflow hygiene the security lint already enforces**: actions pinned to a commit
   SHA, top-level `permissions: {}` with the minimum scope granted per job,
   `persist-credentials: false` on checkout, `concurrency` with `cancel-in-progress: true` on
   pull-request workflows and `false` on deploy and release workflows, and a same-repo guard on any
   job that reaches a privileged account.
6. **Triage bot findings, do not batch-apply them.** Apply findings about permissions, race
   conditions, and token scoping. Reject findings that assume a toolchain the repository does not
   use — always check the installer declared by `framework.package_manager` before accepting a
   finding that names a different one — and record the reason on the thread so it stands as
   evidence. Resolve each thread as its change lands.

## Verification

- Every new gate is green, and every pre-existing gate is still green on the same run.
- The workflow-lint target passes locally where the repository shape has one.
- The aggregate mapped by `make.lint` passes after the formatter mapped by `make.format`; skip
  either with a recorded note when it maps to `null`.
- A gate that is intended to become blocking is added to `ci.required_checks` only after it has
  been green on a full run.
- Reverting a single gate's commit leaves the rest of the batch buildable.

## Common mistakes

- Designing from the ticket text — re-read the file on `main` first; snapshots go stale fast.
- Two gates editing one workflow in one batch — re-split, or merge them into one ticket.
- Adding a make target with no coverage row — the Bats target-coverage contract fails the build.
- Landing a high-risk gate to "see what happens" — it burns runner time on every unrelated pull
  request until it is fixed.
- Making a new gate green by relaxing an existing threshold or narrowing another gate's scope — fix
  the cause the gate reports instead.
- Writing a gate a bot-authored commit cannot satisfy — a commit-message gate needs a bot-guarded
  relaxed config beside the strict human contract, keyed on an identity only the forge (`ci.provider`)
  can write.
