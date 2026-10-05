---
name: go-style-guide
description: Use when writing, reviewing, or committing ANY Go code in this project — enforces the three Google Go Style Guides (guide, decisions, best-practices) item by item.
---

# Google Go Style Guide

This project follows the three Google Go style documents. This skill enforces them
item by item, in two layers:

- **Deterministic layer** — `golangci-lint` + `gofmt`, run by the git `pre-commit`
  hook (`.githooks/pre-commit` → `scripts/lint.sh`). Covers objective items.
- **AI-review layer** — when you (Claude) are about to `git commit`, the
  PreToolUse hook injects `scripts/style-checklist.md` and you MUST confront the
  staged diff against EVERY item before committing. Covers subjective items
  (naming quality, comment usefulness, simplicity).

## The five principles (priority order)

From `references/guide.md`. When principles conflict, earlier wins:

1. **Clarity** — the code's purpose and rationale are clear to the reader.
2. **Simplicity** — simplest way to accomplish the goal; least mechanism.
3. **Concision** — high signal-to-noise ratio; no repetition or noise.
4. **Maintainability** — code is edited far more than written; design for change.
5. **Consistency** — looks/behaves like the surrounding codebase (tie-breaker).

## How to use this skill

- **Writing code** → keep the principles above in mind; consult the relevant
  `references/*.md` when unsure about a specific decision (naming, errors, tests…).
- **Reviewing a diff / before committing** → walk `scripts/style-checklist.md`
  top to bottom against the diff. It is the single source of truth for the AI layer.

## Reference files (load on demand)

- `references/guide.md` — core principles & formatting rules (the "why").
- `references/decisions.md` — itemized normative decisions: naming, commentary,
  imports, errors, language constructs, common libraries, test failures.
- `references/best-practices.md` — itemized patterns: naming, errors (`%w` vs `%v`,
  structured/sentinel errors), documentation, variable declarations, option
  patterns, and testing.

## Most-checked items (quick reference)

- `MixedCaps`, never `under_scores`; initialisms keep case (`URL`, `ID`, `userID`).
- Exported symbols have doc comments starting with the symbol name, full sentences
  ending in a period.
- **GoDoc / pkg.go.dev**: write exported docs to render well on pkg.go.dev, not just
  to exist. Document every exported struct field / interface method / const-var
  individually; give the package doc a real overview (what + approach + how to use,
  with a usage snippet); state contracts (zero-value/default behavior, channel/resource
  ownership, nil handling, which error when); add a runnable `Example` (in `pkg_test`)
  for public packages so usage shows on pkg.go.dev. Sanity-check with `go doc ./<pkg>`.
- Error strings: lowercase, no trailing punctuation. Wrap with `%w` (at the end)
  when callers need `errors.Is`/`errors.As`; `%v` at system boundaries.
- Handle errors immediately; indent the error path, keep the happy path un-indented;
  avoid `else` after a returning `if`.
- No `Get` prefix on getters. Receiver names are 1–2 letters, consistent per type.
- No `util`/`helper`/`common` package names. Don't shadow stdlib package names.
- Tests: `got` before `want`; identify function + inputs in failures; `t.Error`
  to keep going, `t.Fatal` only when continuing is meaningless; field names in
  table-driven struct literals; never `t.Fatal` from a spawned goroutine.
