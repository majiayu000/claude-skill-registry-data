---
name: verification-loop
description: Runs the full quality gate loop (build, types, lint, tests, secrets scan, diff review) for Node, Python, and Flutter projects and produces a pass/fail report. Use after finishing a feature or refactor, before opening a PR, or whenever a session is about to claim that code is complete.
---

# Verification Loop

Six gates, run in order, each one blocking the next. The output is a report with real numbers,
not a feeling that things are probably fine. `opm:verification-before-completion` decides *whether*
you may claim done; this skill is *how* you gather the evidence.

## When to use

- After completing a feature, bug fix, or refactor.
- Before creating or updating a PR.
- After a long session, every major task boundary.
- When a plan task's `verify` step says "full verification".

## Step 0: Detect the stack

| Signal | Stack | Package manager / runner |
|---|---|---|
| `pnpm-lock.yaml` | Node | pnpm |
| `yarn.lock` | Node | yarn |
| `bun.lock` or `bun.lockb` | Node | bun |
| `package-lock.json` or plain `package.json` | Node | npm |
| `pyproject.toml` + `uv.lock` | Python | uv (`uv run <tool>`) |
| `pyproject.toml` / `requirements.txt` without uv | Python | venv / plain tools |
| `pubspec.yaml` | Flutter or Dart | `flutter` / `dart` |

A repo can hold more than one stack (monorepo, Flutter app with a Python backend). Run the loop per stack.

## Command table

| Gate | Node (npm / pnpm / yarn / bun) | Python (uv) | Flutter / Dart |
|---|---|---|---|
| Build | `<pm> run build` | `uv build` (packages) or skip | `flutter build <target> --debug` or skip for libraries |
| Types | `npx tsc --noEmit` | `uv run pyright` or `uv run mypy .` | covered by `dart analyze` |
| Lint | `<pm> run lint` | `uv run ruff check .` and `uv run ruff format --check .` | `dart analyze` (fails on errors; treat warnings as failures if `analysis_options.yaml` says so) |
| Tests | `<pm> test` (`bun test` for native runner) | `uv run pytest` | `flutter test` (`dart test` for pure Dart) |
| Coverage | `<pm> test -- --coverage` / `bun test --coverage` | `uv run pytest --cov=<pkg> --cov-report=term-missing` | `flutter test --coverage` |

`<pm>` is `npm`, `pnpm`, `yarn`, or `bun`. Without uv, drop the `uv run` prefix and use the active venv.

## The six gates

### 1. Build
Run the build command and read the tail of the output. A failed build stops the loop: fix it first.
Libraries without a build step pass this gate by default; say so in the report.

### 2. Types
Run the type checker. Zero errors is the bar for code you touched. Pre-existing errors elsewhere
are reported with a count, not silently accepted.

### 3. Lint
Run the linter and formatter check. Fix what you introduced. Do not disable rules to get green;
if a rule is wrong for the project, that is a separate change with its own justification.

### 4. Tests
Run the full suite for the affected stack, not just the tests you wrote. Record totals:
passed, failed, skipped, and coverage percentage if the project measures it. Any new `skip` or
`only` markers must be explained.

### 5. Secrets and debug residue
Scan the diff, not the whole repo, so pre-existing noise does not hide new problems:

```bash
git diff --cached --name-only | xargs grep -nE \
  '(sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY|api[_-]?key\s*[:=]\s*["'\''][^"'\'']{8,})' 2>/dev/null
git diff --cached | grep -nE '^\+.*(console\.log|debugPrint\(|print\(|breakpoint\(\)|pdb\.set_trace)' 
git diff --cached --name-only | grep -E '(^|/)\.env($|\.)' 
```

Any hit is a finding. A real secret means: stop, remove it, treat it as exposed, rotate it.

### 6. Diff review
```bash
git diff --stat
git diff
```
Read every changed hunk once, as a reviewer would. Look for: files you did not mean to touch,
missing error handling on new paths, unhandled edge cases, leftover TODOs that should be issues,
and changes that widen scope beyond the task.

## Report format

```
VERIFICATION REPORT
===================
Stack:     node (pnpm) | python (uv) | flutter
Build:     PASS | FAIL | N/A
Types:     PASS | FAIL  (N errors, M pre-existing)
Lint:      PASS | FAIL  (N errors, M warnings)
Tests:     PASS | FAIL  (X passed, Y failed, Z skipped, C% coverage)
Secrets:   PASS | FAIL  (N findings)
Diff:      N files, +A/-D lines, reviewed

Overall:   READY | NOT READY

Findings:
1. <gate>: <what>, <where>, <planned fix or why accepted>
```

Every line must come from a command that was actually run in this session. If a gate could not
be run (tool missing, no network), write `NOT RUN: <reason>` rather than PASS.

## Continuous mode

On long sessions, run gates 2-4 at each natural checkpoint (function done, component done, task
done) and the full loop at task boundaries. Fast feedback keeps the fix small.

## Related skills

- `opm:verification-before-completion` - the rule that no completion claim is made without this evidence.
- `opm:tdd-workflow` - produces the tests that gate 4 runs.
- `opm:executing-plans` - calls this loop at the end of each plan.

<!-- Adapted from affaan-m/ecc (MIT) -->
