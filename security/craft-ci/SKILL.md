---
name: craft-ci
description: Crafting a CI pipeline. Five workflows, zero manual gates.
---

# Skill: Craft CI

> "If a human has to approve a style fix, the pipeline has already failed."

## The Standard

1. **Five standard workflows**:
   - `run-tests.yml` -- Matrix testing across PHP/Laravel versions. Triggered on push to PHP files.
   - `phpstan.yml` -- Static analysis at level 5 with Larastan. `--error-format=github` for PR annotations.
   - `fix-php-code-style-issues.yml` -- Laravel Pint auto-fix + auto-commit. No manual style reviews.
   - `update-changelog.yml` -- Auto-update CHANGELOG.md on release publish.
   - `dependabot-auto-merge.yml` -- Auto-merge minor/patch dependency updates.
2. **Matrix strategy**: PHP versions x Laravel versions x stability (`prefer-lowest`, `prefer-stable`). Map Testbench versions via `include`. `fail-fast: false`. `timeout-minutes: 5`.
3. **PHPStan level 5**: With Larastan, baseline file, `checkOctaneCompatibility: true`, `checkModelProperties: true`. The baseline file means existing codebases can adopt PHPStan without fixing everything first. Level 5 is the sweet spot -- strict enough to catch real bugs, lenient enough not to fight you on every line.
4. **Laravel Pint auto-fix**: CI fixes style and commits directly. No developer ever sees a failing style check. No PR review for formatting.
5. **Dependabot**: Weekly Composer + GitHub Actions updates. Auto-merge minor and patch versions.
6. **Concurrency**: `cancel-in-progress: true` on every workflow. New pushes kill stale CI runs. No wasted compute.
7. **Single branch**: `main` only. No `develop`, no release branches. Feature branches merge to `main`. Major version branches only for legacy backports.
8. **Dependency audit**: `composer audit` in CI. Free security scanning -- exits non-zero when vulnerabilities exist. Use `--locked` to audit without installing. Add as a standalone step in `run-tests.yml` or a dedicated workflow.
9. **Coverage thresholds**: Enforce minimum test coverage with `--coverage --min=80` (or your team's threshold). Enforce type coverage with `--type-coverage --min=100`. CI fails when coverage drops. No regressions.

## The Anti-Patterns

| Don't                          | Do                                      | Why                                          |
|--------------------------------|-----------------------------------------|----------------------------------------------|
| No `fail-fast: false`          | `fail-fast: false`                      | See all failures, not just the first         |
| Manual style fixing            | Pint auto-fix + auto-commit             | Humans should not review whitespace          |
| Skip `prefer-lowest` in matrix | Always include `prefer-lowest`          | Catches minimum-version compatibility issues |
| No concurrency control         | `cancel-in-progress: true`              | Stale runs waste compute and delay feedback  |
| PHP-CS-Fixer on new packages   | Laravel Pint                            | Pint is the standard. CS-Fixer is legacy     |
| PHPStan without baseline       | Baseline file from day one              | Adopt incrementally, fix progressively       |
| `develop` + `main` branches    | `main` only                             | One branch. One truth. Less ceremony         |
| Missing PR template            | Ship `.github/PULL_REQUEST_TEMPLATE.md` | Structure the conversation around changes    |
| No dependency auditing         | `composer audit` in CI                  | Free vulnerability scanning, zero effort     |
| No coverage enforcement        | `--coverage --min=80` in CI             | Coverage only matters if it can't regress    |

## Real-World Examples

See [examples.md](examples.md).
