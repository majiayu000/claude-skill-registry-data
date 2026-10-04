---
name: dev-workflow
description: Run the project's validation pipeline (lint → format → typecheck → unit tests) with auto-fixes, then optionally stage and write a Conventional Commit. Use before committing, when asked to "check", "validate", "run the workflow", or "get this commit-ready".
argument-hint: "[quick|full|commit] [commit message]"
allowed-tools: Bash(pnpm lint:fix) Bash(pnpm format) Bash(pnpm typecheck) Bash(pnpm test) Bash(pnpm test *) Bash(pnpm vitest *) Bash(git status *) Bash(git diff *) Bash(git log *)
---

# Dev workflow

Mode: `$0` (default `full`). Optional commit message: the remaining arguments.

## Current state

!`git status --short`

!`git diff --stat HEAD`

## Steps

Run in order and stop at the first step that still fails after auto-fixing. Report each step as `✓` or `✗` with `file:line` references.

1. **Lint**: `pnpm lint:fix`. If errors remain, fix them in code (don't disable rules without a comment explaining why) and re-run.
2. **Format**: `pnpm format` (Prettier: JSON/MD/YAML/CSS only; TS/Vue have no formatter, so match surrounding style).
3. **Typecheck**: `pnpm typecheck`. Fix type errors properly: no `any`, `as unknown as`, or `@ts-ignore` unless an existing pattern requires it.
4. **Unit tests**: skip in `quick` mode. Otherwise run `pnpm vitest run <files>` for the test files that mirror changed sources first (fast feedback), then `pnpm test`.
5. **E2E**: only if the change touches editor flows, layouts, iframe sync, or persistence, and a server can run. Use `/run-app` for local verification or `pnpm test:e2e:smoke`.
6. **Commit** (`commit` mode only):
   - Review `git diff` and stage only files that belong to this change (`git add <paths>`, not `git add -A` blindly).
   - Message: `<type>(<scope>): <lowercase subject>`, header ≤ 100 chars, types `feat fix docs style refactor perf test build ci chore revert`, scopes such as `editor preview ai tools learn store api types test seo deps ci`. Use `!` for breaking changes. Explain _why_ in the body when it isn't obvious.
   - Let husky run lint-staged and commitlint. Never pass `--no-verify`.
   - Don't push unless asked. When pushing, push a feature branch, never `master`.

## Report

End with a short summary: which steps ran, what was auto-fixed, anything still failing, and the commit hash if one was created.
