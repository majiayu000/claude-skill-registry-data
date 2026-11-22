---
name: ts-complexity
description: Report cyclomatic complexity of TypeScript code — changed files by default. Prefers the project's ESLint complexity rule and falls back to npx ts-complex. Optional, model-invoked only.
user-invocable: false
disable-model-invocation: false
argument-hint: "[path or glob — defaults to changed .ts/.tsx files vs the base branch]"
---

# TypeScript cyclomatic complexity

Read-only report — writes no files. Ranks functions by cyclomatic complexity so
hotspots surface before review. **OPTIONAL: lives in `.agentic/optional-skills/`;
onboarding copies it into `.claude/skills/` only when the repo is TypeScript and
carries a `cyclomatic_complexity_max` gate in `.agentic/quality-gates.yaml`.** This
is the measuring tool that `/execute-plan` step 4 runs to produce the actual value
for that gate.

## Step 1 — Resolve scope

- **Argument given** (path or glob): analyze exactly that. Done.
- **No argument**: analyze the changed `.ts`/`.tsx` files vs the base branch.
  Build the set from committed, staged, and unstaged changes; drop `.d.ts` and
  anything under `node_modules`:

  ```sh
  BASE="${BASE_BRANCH:-main}"                 # the branch this work merges into
  MERGE_BASE=$(git merge-base HEAD "$BASE")
  { git diff --name-only --diff-filter=ACMR "$MERGE_BASE"...HEAD
    git diff --name-only --diff-filter=ACMR
    git diff --name-only --diff-filter=ACMR --cached
  } | sort -u | grep -E '\.tsx?$' | grep -vE '\.d\.ts$'
  ```

  If the set is empty, say so and stop — there is nothing to measure.

## Step 2 — Pick the tool (prefer ESLint, fall back to ts-complex)

- **ESLint path** — use it only if BOTH hold: an ESLint config exists
  (`eslint.config.*` or an `.eslintrc*`) AND eslint resolves (`npx eslint --version`
  succeeds without installing). Then run the built-in `complexity` rule at
  threshold 0 so every function reports its number:

  ```sh
  npx eslint --rule '{"complexity":["warn",0]}' <files>
  ```

  (Keep the project's own config active; the inline `--rule` only forces the
  complexity report. If the flat config rejects `--rule`, disable the project's
  own complexity setting for the run rather than dropping its config.)

- **Fallback path** — otherwise run the dedicated package with no install:

  ```sh
  npx --yes ts-complex <file>          # one invocation per file
  ```

  `ts-complex` reports cyclomatic complexity per function plus a maintainability
  index; collect the cyclomatic numbers.

State which path you took and why (one line) so the numbers are interpretable.

## Step 3 — Report

- A table ranked worst-first: file · function/line · cyclomatic complexity.
- **Threshold** comes from config, never memory (hard rule 3). Read
  `gates.cyclomatic_complexity_max` from `.agentic/quality-gates.yaml`.
  - If it exists: flag every function at or over it, and state the source. This is
    the row `/execute-plan` step 4 renders for the gate.
  - If it does not exist: report raw numbers, state plainly that no cyclomatic gate
    is configured, and offer to add one to `quality-gates.yaml` (do not invent a
    pass/fail line from a hardcoded number).
- Keep it to the report. Refactoring is a separate, explicit ask.
