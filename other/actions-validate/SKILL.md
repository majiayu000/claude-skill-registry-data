---
name: actions-validate
description: Validate GitHub Actions workflow files locally with the actionlint then zizmor loop — actionlint for syntax, expression typing, and shellcheck of run steps; zizmor for security audits (expression injection, pull_request_target risks, unpinned actions, over-broad permissions). Use after editing any .github/workflows/*.yaml or action.yml, before committing workflow changes, when asked to lint, validate, or security-audit GitHub Actions workflows, when a workflow fails in CI, or when setting up actionlint/zizmor for a repository.
license: MIT
---

# GitHub Actions validation workflow

Run this loop after editing any workflow and before every commit. Two tools, cheapest-first:
`actionlint` for correctness, then `zizmor` for security. Fix findings and repeat until both are
clean — never commit with failures.

This is the **local** complement to the server-side CodeQL `actions` scan that the
`actions-reusable-workflows` skill wires (the reusable `security.yaml`); run both. zizmor enforces
the `actions-security` rules mechanically, and authoring conventions live in `actions-style`.

## 1. Lint (actionlint)

`actionlint` checks workflow syntax, the validity of events/contexts, expression typing, and runs
`shellcheck` over `run:` steps. From the repository root it auto-discovers `.github/workflows/`:

```sh
actionlint
```

Install via `brew install actionlint`, `go install github.com/rhysd/actionlint/cmd/actionlint@latest`,
or a pinned release binary. Install `shellcheck` (and `pyflakes` for `python` steps) on `PATH` so
the embedded-script checks run; without them actionlint still validates the YAML and expressions.

## 2. Audit security (zizmor)

`zizmor` statically audits workflows and composite actions for the security issues the
`actions-security` skill warns about — template/expression injection, dangerous `pull_request_target`
checkout of PR head, unpinned (mutable-tag) actions, over-broad `permissions`, and more:

```sh
zizmor .github/workflows/
```

Install via `uvx zizmor`, `pipx install zizmor`, `brew install zizmor`, or `cargo install zizmor`.
zizmor runs every audit by default; record only *reviewed* exceptions in a config file rather than
disabling an audit. If the repo has none, offer to seed one from this skill's bundled
[zizmor.yml](zizmor.yml) (place it at the repo root or `.github/zizmor.yml`). zizmor performs some
online checks (e.g. that a pinned action ref exists); pass `--offline` (or set `GH_TOKEN` for
higher rate limits) in sandboxed environments.

## 3. Fix and repeat

Re-run both after fixing. The order matters: `actionlint` first, because `zizmor` assumes parseable,
well-formed YAML. A workflow is done when `actionlint` reports nothing and `zizmor` is clean (or
every remaining finding has a justified ignore entry).

Notes:

- Treat a `zizmor` finding as a security violation, not a suggestion — most map directly to an
  `actions-security` rule (unpinned action → SHA-pin; injectable expression → `env:` indirection;
  over-broad token → least-privilege `permissions:`).
- Wire `actionlint` and `zizmor` into the repo's `lint` mise task so CI re-runs them; the reusable
  `ci.yaml` already calls `mise run lint` (see `actions-reusable-workflows`).
