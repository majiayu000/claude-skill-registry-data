---
id: adept-code-style
description: "Go code style and conventions for the adept codebase — formatting, linters, error wrapping with sentinels, the composition-root/no-globals rule, and core invariants. Apply when writing or reviewing Go in this repo. (matches: **/*.go)"
activation: agent
allowed-tools:
  - "Read"
  - "Grep"
  - "Edit"
---

# adept code style

Conventions for Go in `github.com/itaywol/adeptability`. CI enforces formatting and lint;
the rest is reviewed.

## Formatting & lint (enforced)

- `gofmt` + `goimports` — tabs for indentation, grouped imports (stdlib / third-party /
  local). CI fails on any unformatted file.
- `golangci-lint run` (`.golangci.yml`): `errcheck` (incl. type assertions), `staticcheck`,
  `govet`, `gocritic`, `revive` (**every exported symbol needs a doc comment**), `errorlint`,
  `nilerr`, `bodyclose`, `prealloc`, `unconvert`, `misspell`, `unused`, `ineffassign`.

## Errors

- Always wrap with context and `%w`: `fmt.Errorf("clone %s: %w", url, err)`.
- Compare with `errors.Is` against the sentinels in `pkg/adept/errors.go`
  (`ErrSkillNotFound`, `ErrMergeConflict`, `ErrBudgetOverflow`, …). **Never** match on error
  strings. Need a new category? Add a sentinel there.
- `errcheck` is strict — handle or explicitly `_ =` an ignored error, and say why if it isn't
  obvious. Don't drop an error that loses data.

## Structure

- **Composition root, no globals.** Concrete implementations are wired behind interfaces into
  `*Deps` in `internal/cli/deps.go`. No package-level mutable state, no `init()` side effects.
  Take dependencies as parameters so code is testable with fakes/mocks.
- **`pkg/adept` is types-only.** Keep it dependency-light and stable; behavior lives in
  `internal/`. (Example: `SkillIDPattern` is a string in `pkg/adept`, compiled in
  `internal/canonical` — don't add a `regexp` import to `pkg/adept`.)
- Doc comments are full sentences starting with the symbol name (`// NewRoot builds …`).

## Readability

- Small, single-purpose functions; prefer **early returns** over deep nesting.
- Name things for what they are; avoid one-letter names outside tight loops/receivers.
- No magic numbers/strings — name on-disk paths and limits as constants (see
  `pkg/adept/constants.go`).
- Comments explain **why**, not what. Keep them in sync with the code — a stale comment is a
  bug.

## Invariants you must not break

1. Identity is `(id, content-hash)` — no version numbers as a sync signal.
2. Secrets never written to disk — API keys come from the environment at call time.
3. Harness models differ (per-skill / single-file / aggregator) — renderers and importers
   must respect each; aggregators parse their own section markers and honor byte budgets.
4. Canonical layout `<root>/skills/<id>/SKILL.md`; the directory name is the authoritative id.
