---
name: "refactoring"
description: >-
  v1.0.0 — Use when the user asks to refactor, restructure, or modularize an existing codebase.
  Extracts monolithic files into well-organized modules following single-responsibility principles,
  audits multi-repository workspaces, creates tests first (TDD), and ensures extracted code is
  documented, logged, and verified. Always analyze and plan module boundaries before touching code.
---

# Refactoring Architect

Refactor existing code into maintainable modules without changing behavior.
Use tests as the safety rail: characterize first, extract, integrate, verify.

## Absolute Rules

- Analyze before moving code. Understand behavior, deployment, tests, and public
  contracts first.
- Write or identify focused tests before extraction. If no useful harness exists,
  create the smallest one that protects the behavior being moved.
- Never change behavior during refactoring unless the user explicitly requested a
  behavior fix. Keep signatures, errors, output, config, and deployment contracts
  stable.
- Extract one cohesive module at a time by default. Multiple modules or multiple
  repositories are allowed only when requested; still verify each change
  independently.
- Do not mechanically split files by line count. Generated files, static content,
  single-concern string constants, and standalone scripts deployed as one file may
  be correct as-is.
- If the audit finds a repo already compliant, make only the specific fixes found;
  do not invent refactors or infrastructure.
- If the user asks whether the project follows guidelines, asks you to finish a
  previously narrow refactor, or challenges completeness, continue with a
  concrete compliance audit and fixes. Do not merely answer that compliance is
  unproven, and do not treat one small extraction as sufficient unless the audit
  shows there are no other in-scope gaps.
- Never leave real dead code, unused imports, duplicate helpers, or orphaned
  internal functions. Keep external compatibility surfaces until proven unused.
- Update documentation comments when moving public or non-obvious code.
- Always verify tests pass after each extraction step.
- Commit your finished work by default, in the worktree you are working on;
  keep each extraction in its own commit.
- Do not refactor generated outputs, dependency folders, caches, vendored
  packages, or build artifacts unless explicitly asked.

## Step 1: Full Analysis

Prefer `rg`/`rg --files` and prune generated directories:

```bash
git status --short
rg --files -g '*.py' -g '*.sh' -g '*.js' -g '*.ts' -g '!**/.git/**' -g '!**/.venv/**' -g '!**/node_modules/**' -g '!**/__pycache__/**' -g '!**/build/**' -g '!**/dist/**' | xargs wc -l | sort -nr
rg -n '(^def |^class |^function |^[a-zA-Z_][a-zA-Z0-9_]*\(\))' -g '*.py' -g '*.sh' -g '*.js' -g '*.ts'
```

Identify:
1. Monolith candidates: large files with multiple responsibilities, not merely
   files over 200 lines.
2. Cohesive groups that belong together by feature or boundary.
3. Missing tests for behavior you will move or fix.
4. Real dead code: unused imports, orphaned internals, obsolete tests, duplicate
   helpers, and legacy paths proven unreachable.
5. Compatibility surfaces: exported functions, CLI flags, aliases, wrappers,
   generated entrypoints, and external contracts that must be kept or documented.
6. Logging gaps on action paths, state transitions, boundary failures, external
   calls, and meaningful decisions.
7. Deployment risks: install copy lists, package data, service units, APT source
   filenames, desktop entries, shell helper names, and required env/config.
   For installed Python entrypoints, compare project-local imports against copied
   helper modules or package manifests and add a regression test when gaps could
   break clean installs.
8. Static content where code rules should not be applied, such as prompt files,
   generated data, string constants, docs, or vendored code.
9. Misleading formatting or illogical code shape: stray indentation, duplicated
   branches, dense expressions, silent broad exception swallowing, and tests
   asserting obsolete paths.

For multi-repository workspaces:
1. Inventory every repository first: git state, language/tooling, source count,
   test count, largest source files, deployment path, and log sink.
2. Do not mix unrelated repositories in one extraction. Finish and verify one
   repo-level change before editing the next.
3. Prioritize missing tests, behavior bugs, logging/deployment policy gaps, then
   production monoliths with focused tests, then lower-risk cleanup.
4. Run a second audit after edits using the same checks and compare against the
   first pass.

## Step 2: Plan the Structure

Write a numbered plan that names each extraction and its verification:

```text
1. Extract database connection logic from app.py -> src/database/manager.py (with tests)
2. Extract auth parsing from app.py -> src/auth/parser.py (with tests)
3. Update imports and installer/package manifests
4. Run focused tests, then the relevant full suite
```

Each new module should have one responsibility, clear integration back to the
caller, public documentation where useful, existing or centralized logging, and
tests for public behavior.

## Step 3: Test First

- For each function/class being extracted, create or identify tests before moving
  it.
- If tests already exist, run the relevant subset before and after risky moves.
- Cover normal behavior, error paths, edge cases, and dependency interactions.
- For GNOME extensions, installers, CLI hooks, services, and environment-bound
  code, extract pure helper logic first and test it locally. Keep platform calls
  behind small wrappers that can be mocked.
- When adding shared dependencies such as a `log` helper to sourced shell code,
  update test stubs so isolated tests reflect the real dependency shape.

Use the repository's configured commands, for example:

```bash
pytest tests/test_<module_name>.py -v
bash tests/test_<module_name>.sh
npm test
```

## Step 4: Extract One Module at a Time

For each extraction:
1. Create the new file with concise header documentation when it introduces a
   reusable module or script.
2. Move the cohesive code.
3. Update imports, call sites, install scripts, package manifests, copy lists,
   and existence checks.
4. Run focused tests.
5. Read the diff for accidental behavior, output, logging, or deployment changes
   before continuing.

## Step 5: Logging During Refactors

When refactoring touches runtime code:
1. Prefer the repository's existing centralized logger. Every project routes
   logging through one centralized logging module; for Python projects, use
   that module's standard call-tracing (`log_call`) decorator instead of
   inventing per-file helpers.
2. Bash and shell scripts use one sourced logging helper from the project or
   installer framework. During cleanup, remove old hardcoded log functions from
   feature scripts, route call sites through the shared helper, and update
   installer copy lists or package manifests whenever the helper must be present
   in an installed copy.
3. Repository-generated file logs belong under repo-root `.log/`, and `.log/`
   must be gitignored.
4. Preserve stdout/stderr contracts for status bars, command substitution, CLI
   filters, probes, TUIs, and installer-compatible formats.
5. Use environment-appropriate sinks: journald/systemd or GNOME Shell logging for
   services/extensions; stderr for installer contracts; file-only logging for
   TUIs when terminal output would corrupt the interface.
6. Logging coverage means action paths, state changes, external calls, boundary
   failures, and meaningful decisions are observable. Pure helpers, parsers,
   formatters, recursive generators, hot loops, logging primitives, and generated
   shims may be covered by caller-level logs.
7. Avoid high-frequency log spam. Log summaries and decisions around hot paths.
8. Logging in hooks and installers must be best-effort and never abort the user
   workflow.
9. API logging must capture lifecycle/failures without secrets or sensitive
   payloads.

## Step 6: Verify

Run focused tests first, then the relevant full suite when practical:

```bash
pytest tests/ -v --tb=short
ruff check .
npm run lint
npm run typecheck
rg -n '(^def |^class |^function |^[a-zA-Z_][a-zA-Z0-9_]*\(\))' -g '*.py' -g '*.sh' -g '*.js' -g '*.ts' -g '!**/__pycache__/**'
```

Run configured lint/type checks only if the repository already provides them.
Do not install new lint tools ad hoc to satisfy this step. For Python dependency
changes or new Python projects, follow the `init-project` skill and the
supply-chain policy instead of direct `pip install`.

Also verify:
- No broken imports or missing deployed modules remain.
- No real dead code, unused imports, duplicate helpers, or obsolete tests remain.
- Required config is validated before side effects.
- Output formats and externally documented behavior are unchanged.
- Installer and service changes still work in the repo's tested root/non-root or
  user/system modes.
- For broad compliance work, explicitly say which checks were run and which
  residual risks remain; avoid claiming certainty beyond the evidence.

## Step 7: Update Documentation

Update README/docs only when refactoring changes module layout, install behavior,
commands, logging, architecture, or usage. Keep docs proportional: project tree,
module responsibilities, import examples, and test commands are useful when they
help future maintainers.

## Example: Refactoring a Monolithic `install.sh`

1. Analyze: source count, function list, git state, tests, manifests, log sink.
2. Identify feature groups: packages, GNOME extensions, services, keybindings.
3. Plan `lib/packages.sh`, `lib/gnome_extensions.sh`, `lib/services.sh`, etc.
4. Write or run focused tests for the first group.
5. Extract one group, update `install.sh` and copy/check lists, then verify.
6. Repeat for the next group.
7. Run a second audit and relevant installer tests in a temporary home or
   sandbox when available.
