---
name: mk:verify
description: "Unified verification: build→lint→test→type-check→coverage. Use for 'is everything green', 'run all checks', 'verify build'. Auto-called by mk:cook. NOT for lint/format only (see mk:lint-and-validate); NOT for test-to-requirement coverage mapping (see mk:nyquist)."
version: 1.0.0
argument-hint: "[--full] [--coverage-threshold N] [--skip-build] [--skip-coverage]"
source: local
allowed-tools:
  - Bash
  - Read
  - Glob
keywords:
  - verify
  - build-check
  - lint-test-typecheck
  - coverage
  - unified-verification
  - pre-ship
when_to_use: Use for unified verification — build→lint→test→type-check→coverage. Auto-called by mk:cook. NOT for lint/format only (see mk:lint-and-validate) or coverage mapping (see mk:nyquist).
user-invocable: true
owner: lifecycle
criticality: high
status: active
runtime: claude-code
---

# Verify — Unified Verification Loop

Runs build → lint → type-check → tests → coverage in sequence. Fails fast on first failure.
Produces a single PASS/FAIL verdict with per-step results.

## When to Use

- After Phase 3 (Build GREEN) completes, before Phase 4 (Review)
- Before creating a PR (`mk:ship` pre-flight)
- Standalone: "is everything green?", "run all checks", "verify build"

## Phase Anchor

**Phase: 3→4 transition (Build → Review)**
**Handoff:** If PASS → proceed to `mk:review`. If FAIL → developer fixes, re-run verify.

## Project Detection

Detect project type by checking for marker files in this order:

| Marker File      | Language | Build                    | Lint                       | Type-check                            | Test                | Coverage                            |
| ---------------- | -------- | ------------------------ | -------------------------- | ------------------------------------- | ------------------- | ----------------------------------- |
| `package.json`   | JS/TS    | `npm run build`          | `npm run lint`             | `npm run typecheck` or `tsc --noEmit` | `npm test`          | `.nycrc` or `jest.config` threshold |
| `pyproject.toml` | Python   | `python -m build`        | `ruff check .` or `flake8` | `mypy .`                              | `pytest`            | `pyproject.toml` coverage threshold |
| `go.mod`         | Go       | `go build ./...`         | `golangci-lint run`        | (built-in to build)                   | `go test ./...`     | coverage report                     |
| `Gemfile`        | Ruby     | `bundle exec rake build` | `rubocop`                  | (N/A)                                 | `bundle exec rspec` | `.simplecov`                        |
| `Cargo.toml`     | Rust     | `cargo build`            | `cargo clippy`             | (built-in to build)                   | `cargo test`        | `cargo tarpaulin`                   |

**Multiple markers found:** Use the most specific one (e.g., `Cargo.toml` over `package.json` if both exist in a mixed repo).

**No marker found:** Ask user — "What build and test commands should I use for this project?"

See `references/project-detection.md` for detailed detection logic and edge cases.

## Scope: Changed Files (default)

By default this skill checks only what changed — it does NOT lint or test the whole
project. Post-change verification stays fast and focused on the current work; the
complete whole-project gate runs later at ship time (`pre-ship.sh`).

1. Collect the changed files from git — union of committed-since-base + staged +
   unstaged + untracked:

   ```bash
   BASE=$(git merge-base HEAD origin/HEAD 2>/dev/null \
       || git merge-base HEAD main 2>/dev/null \
       || git merge-base HEAD master 2>/dev/null)
   { [ -n "$BASE" ] && git diff --name-only "$BASE"...HEAD
     git diff --name-only
     git diff --name-only --cached
     git ls-files --others --exclude-standard
   } | sort -u
   ```

2. **Lint** runs on the changed files only (e.g. `npx eslint <files>`, `ruff check <files>`).
3. **Tests** run only those related to the changed files (e.g. `jest --findRelatedTests`,
   `vitest related`, the changed test files for pytest).
4. **Build** and **type-check** stay whole-program — a partial build or `tsc --noEmit`
   pass is unsound and would miss cross-file breakage.
5. **Coverage** is skipped in scoped mode (a related-tests run does not reflect global
   coverage) and reported as `SCOPED`.

**Fallbacks:** if git is unavailable, or no changed files are detected, run the whole
project (equivalent to `--full`). Pass `--full` to force a complete whole-project run —
use it for releases and CI.

See `references/project-detection.md` for per-language scoped command mappings.

## Process (Fail Fast)

Execute each step in order. **Stop immediately on first failure** — do not continue to the next step.

1. **Resolve scope** — collect changed files (above). Lint + tests run against the
   changed set; build + type-check run whole-program. `--full` runs every step across
   the whole project.
2. **Detect** project type from marker files
3. **Build** — compile/bundle the project (whole-program)
4. **Lint** — static analysis on the changed files (whole project under `--full`)
5. **Type-check** — static type validation, whole-program (if applicable to language)
6. **Test** — run tests related to the changed files (full suite under `--full`)
7. **Coverage** — `--full` only (a related-tests run does not reflect global coverage)

## Coverage Threshold

1. Check project config for threshold (`.nycrc`, `jest.config`, `pyproject.toml [tool.coverage]`, etc.)
2. If no project config: use default **80%**
3. If `--coverage-threshold N` flag provided: override with N%

## Output Format

```
## Verification Report

- Build:      PASS (npm run build, 4.2s)
- Lint:       PASS (0 errors, 2 warnings)
- Type-check: PASS (0 errors)
- Tests:      PASS (142 passed, 0 failed, 3 skipped)
- Coverage:   PASS (87% vs 80% threshold)

**Overall: PASS** — ready for review
```

In scoped (default) mode, Lint and Tests note the changed-file count and Coverage shows
`SCOPED`:

```
- Lint:       PASS (3 changed files, 0 errors)
- Tests:      PASS (related to 3 changed files — 18 passed, 0 failed)
- Coverage:   SCOPED (run with --full for global coverage)
```

Failure example (stops after lint):

```
## Verification Report

- Build:      PASS (npm run build, 3.8s)
- Lint:       FAIL (3 errors in src/auth.ts:12, src/user.ts:45)
- Type-check: SKIPPED (lint failed)
- Tests:      SKIPPED (lint failed)
- Coverage:   SKIPPED (lint failed)

**Overall: FAIL** — fix lint errors before proceeding

Errors:
  src/auth.ts:12  error  'password' is assigned but never used  no-unused-vars
  src/user.ts:45  error  Expected '===' but saw '=='            eqeqeq
```

## Flags

| Flag                     | Effect                                                                                                                   |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| `--full`                 | Check the whole project (build+lint+test+coverage across all files). Use for releases/CI. Default is changed-files scope |
| `--coverage-threshold N` | Override coverage threshold with N%                                                                                      |
| `--skip-build`           | Skip build step (use if build runs separately)                                                                           |
| `--skip-coverage`        | Skip coverage check (use for quick verification)                                                                         |

## Gotchas

- **Config changes escalate to `--full`:** when the changed set includes build/lint/type/test
  config or dependencies (`package.json`, lockfiles, `tsconfig*`, ESLint/Prettier config,
  `jest`/`vitest`/`pytest`/`ruff` config, CI workflows, oxlint), scoping is unsafe — those affect the
  whole project. Run the whole project instead.
- **Deleted-only changes:** if the changed set is only deletions/renames with no surviving
  source files, related-tests scoping finds nothing — fall back to `--full` to confirm nothing
  downstream broke.
- **Package manager detection:** For JS/TS, check for `pnpm-lock.yaml`, `yarn.lock`, or `bun.lockb` before defaulting to `npm`
- **Monorepo:** If multiple `package.json` found, ask user which workspace to verify or run from root
- **Type-check for Go/Rust:** Covered by the build step — mark as PASS if build passed
- **Coverage for Ruby:** `.simplecov` config may not exist; default to 80% threshold if missing
- **Flaky tests:** If tests fail intermittently, re-run once before reporting FAIL
