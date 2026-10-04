---
name: make-target-maintenance
description: >-
  Use when a Makefile target and its coverage manifest have drifted apart — the `bats` check failing
  with a `diff` between the Makefile target list and the target column of
  `tests/bats/make-target-coverage.tsv`, a manifest row whose `evidence` file does not exist or
  never names the target as a whole token, a row left behind by a renamed or deleted target, or a
  linter added to the `lint` aggregate but missing from `CI_LINT_TARGETS`.
---

# Make target coverage maintenance

## Profile keys consumed

- `make.lint`
- `make.ci`

The Bats suite itself has no logical key in the profile: invoke the repository's own Bats target,
and record a note when the repository ships none.

## Overview

Every repository pins its Makefile against a coverage manifest and a Bats suite: a target that
exists but is not declared, or declared but not evidenced, fails the `bats` check. Adding or
renaming a target is therefore a three-file change, not a one-file change.

## When to use

- Adding, renaming, or deleting a target in the `Makefile`.
- The `bats` CI check fails with a diff between expected targets and manifest targets.
- A Bats run reports a missing evidence file or a target name not found in its evidence.
- Adding a linter to the `lint:` aggregate (the target mapped by `make.lint`).
- Not for: editing the recipe of an existing target without changing its name.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — `tests/bats/make-target-coverage.tsv`, `tests/bats/makefile_targets.bats`,
  `tests/bats/issue_78_contract.bats`, `tests/bats/test_helper.bash`; run the repository's Bats
  target.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — same layout and
  manifest; the contract file is `tests/bats/issue_175_contract.bats`.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes — same
  layout and manifest; the contract file is `tests/bats/target_coverage_contract.bats`, and there
  is no `CI_LINT_TARGETS` variable.

## Procedure

1. **Add the manifest row.** `tests/bats/make-target-coverage.tsv` is tab-separated with four
   columns and one row per non-`.PHONY` target:

   ```bash
   # columns, tab-separated: target | coverage | evidence | details
   check-env-sync  bats  tests/bats/makefile_targets.bats  Validated in the sandboxed run.
   ```

   `coverage` is one of `bats`, `ci`, or `coverage`. The header row is skipped; the contract test
   diffs the manifest's target column against every non-`.`-prefixed `^name:` rule in the
   `Makefile`, so a missing or extra row fails.

2. **Make the evidence real.** The path in column three must exist. When `coverage` is `bats`, the
   target name must appear as a whole token somewhere in that file — an assertion that names it, not
   just a comment mentioning it.

3. **Add the test and the stub.** In `tests/bats/makefile_targets.bats`, assert the target's
   observable behaviour; in `tests/bats/test_helper.bash`, add whatever stub the recipe needs
   (`create_generic_stub <binary>`, a docker stub entry) so the sandboxed run never executes the
   real command.

4. **Sync the aggregate lists.** The React SPA and Next.js shapes both carry a `CI_LINT_TARGETS`
   variable that a new linter in the `lint:` prerequisite list must also join. In the React SPA
   shape a Bats test asserts the two mirror each other exactly, in both directions; the Next.js
   shape only spot-checks a single entry, so treat the mirror there as a convention the test will
   not catch. The component-library shape has no such variable.

5. **Verify locally before pushing:** run the target mapped by `make.lint` (skip with a recorded
   note when it maps to `null`), then the repository's Bats target.

   ```bash # profile-example
   make lint
   make test-bats
   ```

## Quick reference

| Artifact                                  | What it pins                              |
| ----------------------------------------- | ----------------------------------------- |
| `make-target-coverage.tsv`                | Every target is declared exactly once     |
| `makefile_targets.bats`                   | Behaviour, help output, aggregate lists   |
| the repository's target-coverage contract | Manifest matches the Makefile, both ways  |
| `test_helper.bash`                        | Sandbox stubs so recipes never really run |

## Common mistakes

- Using spaces instead of tabs in the TSV — the column split silently misreads and the diff fails.
- Pointing `evidence` at a file that does not name the target, so the whole-token assertion fails.
- Forgetting that the React SPA shape pins its docs too: its Bats suite asserts `README.md` mentions
  the Bats target and `CONTRIBUTING.md` mentions the manifest filename.
- Declaring a target in the manifest but never adding the rule, or vice versa after a rename — the
  contract diffs both directions.
- Letting a recipe run for real in the sandbox because its binary has no stub.
