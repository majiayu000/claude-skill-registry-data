---
name: audit-toolchain
description: Use when asked whether a repo's tooling is current, before a toolchain migration, or when a dependency or build step feels dated. Compares the repo to tech-radar.md and the stack profile and reports gaps with cost; changes nothing unless asked.
---

# Audit Toolchain

Read-only report: where the repo differs from the Adopt rows of [tech-radar.md](../_shared/tech-radar.md) and from its own [stack profile](../_shared/stack-profile.md). Migration cost scale and skill mapping: [migration-map.md](migration-map.md).

## 1. Audit (change nothing)

```bash
cat .claude/stack-profile.md 2>/dev/null
ls pnpm-lock.yaml package-lock.json bun.lock bun.lockb yarn.lock uv.lock go.mod Cargo.toml mise.toml .tool-versions .nvmrc justfile Makefile 2>/dev/null
cat package.json 2>/dev/null | head -80
grep -E '^(go|toolchain) ' go.mod 2>/dev/null; grep -E 'requires-python|\[tool\.(ruff|uv|mypy|pyright)' pyproject.toml 2>/dev/null; grep -E '^(edition|rust-version)' Cargo.toml 2>/dev/null
ls .github/workflows 2>/dev/null; grep -hE 'uses:|node-version|go-version|python-version' .github/workflows/*.y*ml 2>/dev/null | head -40
ls biome.json* eslint.config.* .eslintrc* .prettierrc* .oxlintrc.json .golangci.y*ml ruff.toml 2>/dev/null
```

Profile present: use it as the *intended* stack and report drift from it. Absent: detect per the table in [stack-profile.md](../_shared/stack-profile.md); if the answer is ambiguous and changes the report, ask one question and suggest `set-up-stack-profile`.

## 2. Decide

- Everything matches Adopt rows → print "already in place" with the checked date and stop.
- Else continue.

## 3. Verify the radar is fresh

The radar carries a date. If it is older than 90 days, or any row you will cite is `unverified`, re-check that row live per [version-protocol.md](../_shared/version-protocol.md) first (`npm view <pkg> version`, `curl` PyPI JSON, `gh api repos/<o>/<r>/releases/latest`). Report the real latest, not the radar's copy.

## 4. Compare

For each tool the repo uses, find its row and classify:

| Finding | Meaning |
|---|---|
| **Adopt-gap** | The repo lacks the Adopt choice for a concern (no formatter; Node pinned two LTS lines behind; no runtime manager file). |
| **Hold-in-use** | The repo uses a Hold item (ESLint+Prettier in a new repo, Terraform BUSL, an end-of-life Node). |
| **Behind** | Right tool, old major (versions from step 3). |
| **Drift** | The repo differs from its own profile (profile says Biome; repo runs ESLint). |
| **Fine** | Matches. Not listed. |
| **Unlisted** | Tool not on the radar: report it with no ring; do not guess. |

Check these concerns, in order: runtime (Node/Go/Python/Rust line), runtime manager, package manager, bundler, linter/formatter, type checker, test runner, CI pins (actions by SHA), task runner, observability seam, IaC.

## 5. Report

One table, highest value first:

| # | Finding | Evidence (`path:line`) | Radar ring | Cost S/M/L | Fixed by | Risk |
|---|---|---|---|---|---|---|

- **Cost**: S under half a day, M one to three days, L more than three days or touching many files (scale in [migration-map.md](migration-map.md)).
- **Fixed by**: the skill that performs the migration, from the map. If no skill covers it, write "no skill" and offer `extend-skillset`.
- **Risk**: what could break and how to roll back.

Then a short "Do first" list (at most three) chosen by value over cost, and a "Leave alone" list for Hold items where migration cost outweighs the benefit (with the reason). Respect the principle "consistency beats local optimum" from [engineering-principles.md](../_shared/engineering-principles.md): a half-migrated repo is worse than an old one.

## 6. Act only when asked

Changing anything needs a go-ahead from the user per item. When approved, run the mapped skill; one migration per PR. Never upgrade a user-pinned version unasked.

## 7. Verify

The report ran only read commands: `git status --porcelain` is unchanged. Every cited line number exists (`sed -n '<n>p' <file>`). Every "latest" has a command and a date behind it.
