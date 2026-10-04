---
name: contributing
description: The project's contribution mechanics — formatting, linting, type-checking, testing, the source-policy gate, the opt-in pre-commit hook, and how to commit. Use when setting up the repo, before committing, or when asked how to run checks/tests here.
---

# Contributing

Mechanics for contributing to kerala-gov-mission-control. Full prose is in
[`CONTRIBUTING.md`](../../../CONTRIBUTING.md).

## Commands

```bash
deno task dev            # dev server at http://localhost:8000 (hot reload)
deno task check          # deno fmt --check + deno lint + deno check  ← run before every commit
deno task check:sources  # government-source policy on data fixtures
deno task build          # production build → _fresh/
deno task seed           # wipe + reseed local KV from fixtures
deno task translate:test # pytest for scripts/translate.py
deno task review         # advisory headless Claude review of staged changes
```

`deno fmt` (no `--check`) auto-formats. The PostToolUse hook already runs
`deno fmt` + `deno lint` on each edited `.ts`/`.tsx`.

## Before you commit — checklist

1. `deno task check` is green (formatting, lint, types).
2. `deno task check:sources` is green (every figure government-sourced).
3. `SEED_VERSION` bumped if any `data/*.ts` fixture changed.
4. Bilingual parity for new strings (or `dataStatus: "tbd"`) — `/bilingual-audit`.
5. A spec note in `docs/specs/` for non-trivial features.

## Pre-commit hook (opt-in)

A version-controlled hook lives in `.githooks/`. Enable it once per clone:

```bash
git config core.hooksPath .githooks
```

It **blocks** on `deno task check` + `deno task check:sources` and runs an
**advisory** (non-blocking) headless Claude review. Bypass a single commit with
`git commit --no-verify`; skip just the review with `SKIP_REVIEW=1 git commit`.

## Testing

- Type-checking (`deno check`) is the primary safety net — it's part of
  `deno task check`.
- Python (`scripts/translate.py`): `deno task translate:test` (pytest via uv).
- Manual: `deno task dev` + a screenshot for any visual change.

## Commit conventions

Branch off `main`; never commit straight to `main`. Conventional-style messages
(`feat:`, `fix:`, `chore:`, `docs:`). CI (`.github/workflows/ci.yml`) runs
`check` + `build` on every PR — keep it green.
