---
name: ci-verify
description: Run and interpret pnpm lint, pnpm typecheck, pnpm build, and pnpm format in a Turborepo monorepo; diagnose CI-style failures; propose minimal diffs; and deliver a fix plan, files touched, and validation commands checklist. Use when verifying CI readiness or fixing lint/typecheck/build/format failures in Turborepo repositories.
---

# CI Verify

Act as a CI-focused fixer for Turborepo monorepos using pnpm. Keep diffs minimal and follow repository rules (AGENTS.md, README, and package-specific docs). CI is the source of truth.

## Workflow

1. Read repo guidance and constraints before running commands.
2. Run the CI-aligned commands in this order at the repo root:
   - `pnpm lint`
   - `pnpm typecheck`
   - `pnpm build`
   - `pnpm format`
3. Interpret failures. Identify the first failing package and root cause.
4. Propose the smallest, safest change that fixes the failure. Avoid refactors and repo reshuffles.
5. Apply the minimal diff. Do not add new dependencies unless clearly necessary. If necessary, ask first.
6. Re-run the failing command(s) locally. Re-run the full set before final response when feasible.

## Failure Diagnosis Heuristics

- Lint failures: fix rule violations with the smallest change. Prefer local suppression only when justified.
- Typecheck failures: fix incorrect types at the source. Avoid `any`. Use `unknown` with narrowing when needed.
- Build failures: check config mismatches, missing exports, or invalid imports. Favor small fixes over config changes.
- Format failures: prefer targeted formatting when possible (package-scoped or file-scoped) to avoid unrelated diffs.
- If a command fails due to environment issues (Node/pnpm mismatch), call it out and align with repo versions.

## Output Requirements

Always finish with a checklist that includes:

- Fix plan: brief numbered steps.
- Files touched: list of files changed (or "none").
- Validation commands: list the commands that were run or should be run.

Keep the response concise and CI-focused. If no changes are needed, state that explicitly and still include the checklist.
