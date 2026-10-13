---
name: preflight
description: >
  Run the right lint/format/type/test gates BEFORE committing or pushing. Sniffs
  the current repo's stack (poetry/uv/yarn/pnpm/go/rust) and runs the correct
  commands. Blocks commit if any gate is red.

  Trigger this skill when:
  - User says "commit", "ready to push", "prep for PR", "preflight", or invokes
    `/preflight`.
  - After a batch of edits before the user asks for a commit.
  - Before running `git commit`.
---

## Why

Nimbus feedback rule: **always run repo lint + format locally before every
commit. CI rubber-stamps, doesn't discover.** A CI failure on style is a wasted
round-trip.

## Stack detection (top-down at repo root)

Look for these markers, run the matching gates. If multiple, run all.

### Python

- `pyproject.toml` with `[tool.poetry]` → poetry
- `pyproject.toml` with `[tool.uv]` or `uv.lock` → uv
- Fallback: `pip` / raw `python -m …`

Commands:
- `ruff check` + `ruff format --check` if `ruff` in deps.
- `flake8` if configured (transitional in cidca-services).
- `mypy` — INFORMATIONAL, never blocks (horus convention).
- `pytest -m "not integration"` if `tests/` exists — blocking.

### Node/TS

- `yarn.lock` → yarn (yarn 4 in cidca-platform ecg-ui).
- `pnpm-lock.yaml` → pnpm (horus, zotea).
- `package-lock.json` → npm.

Commands (per project.json scripts, if present):
- `yarn format:check && yarn lint && npx tsc --noEmit` (cidca-platform ecg-ui convention).
- `pnpm format:check && pnpm lint && pnpm build` (zotea convention — build IS the pre-push gate).
- Monorepo: `pnpm turbo lint type-check format` (horus).
- If `e2e/tsconfig.json` exists → also `npx tsc --noEmit -p e2e/tsconfig.json`.

### Go

- `go.mod` at path.

Commands:
- `gofmt -l .` (should output nothing).
- `go vet ./...`.
- `golangci-lint run ./...` if config present.
- `go test ./...` if tests exist.

### Migration files touched

If staged diff includes `**/migrations/*.py`, `**/drizzle/**`, `**/alembic/**`
→ also invoke the `db-migration-safety` skill.

## Behavior

1. Detect stack(s).
2. Print the exact commands you're about to run.
3. Run them, tail last 20 lines of output.
4. If any fail: report `❌ <gate>` with the failing line, offer to fix common
   issues (`ruff format` for format failures, `yarn format` for prettier, etc.).
5. If all pass: `✅ preflight clean` and proceed to the requested commit.

## Special cases

- **cidca-platform ecg-ui**: `yarn install --immutable` is flaky locally. Use
  `yarn install` for local dev. Only CI uses `--immutable`.
- **cidca-platform ecg_auto**: also runs `python manage.py makemigrations --dry-run --check` if migrations touched.
- **zotea**: NEVER run `pnpm db:migrate` from preflight. Migrations are CI-only
  (see `db-migration-safety` skill for the load-bearing gotcha).
- **horus**: `make lint format type-check` covers everything if `Makefile` targets exist.

## Do not

- Run tests longer than 60s during preflight — they're for a separate `test`
  invocation.
- Auto-fix without user consent when the fix changes semantics (e.g. suppression
  comments, disabled rules).
- Preflight on a dirty working tree the user hasn't staged — ask first.
