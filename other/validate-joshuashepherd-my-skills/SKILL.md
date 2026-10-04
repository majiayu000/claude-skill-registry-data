---
name: validate
description: Run bottom-up type-chain validation (db → hooks) and fix errors at the failing layer. Use for project health checks before large changes.
---

# Validate (Cursor)

## Canonical source

**`.claude/skills/validate/SKILL.md`** — full command table and error-fix protocol.

## Quick reference

- `pnpm validate:all` — layers 1–5
- `pnpm validate:all:with-ui` — include Layer 6 when UI exists
- `pnpm build:check` — `tsc -p tsconfig.build.json`; set `RUN_LAYER_VALIDATION=true` to run `validate:all` first

Human-readable docs: **`_docs/_build/type/TYPE_SAFETY.md`**, **`_docs/_build/architecture/type-safety-chain.md`**.
