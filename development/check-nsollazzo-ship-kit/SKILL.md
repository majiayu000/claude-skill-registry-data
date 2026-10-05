---
name: check
description: |
  ALWAYS use this skill when the user says "check", "/check", "check my code", "run the
  checks", "lint and fix", "typecheck", or "make it green locally before I commit".
  Detects the repo's own toolchain
  (package.json scripts, Turbo, Makefile, pyproject.toml, Cargo.toml, go.mod) and runs it —
  never hardcodes a stack. This is the fast LOCAL loop — it fixes mechanical failures (types,
  lint, format, build, test), it does not hunt correctness bugs (use `code-review`) and does
  not exercise runtime behavior (use `verify`).
license: MIT
metadata:
  author: Nicholas Sollazzo
  version: "3.0.0"
argument-hint: "[slop|types|lint|build|test|security|branch|all] [--commit] [--fix-only]"
---

# Check — fast local self-healing quality loop

Detect the project's toolchain, run static checks + build + tests, auto-fix what's safe,
and report pass/fail with evidence. Never claim green on something skipped or timed out.

## Invoking sibling skills (portability)

For `--commit`, this skill calls `smart-commit`. If your harness has a skill-invocation
tool (e.g. Claude Code's `Skill` tool), call it by name. Otherwise, load that skill's
`SKILL.md` from this kit and follow its procedure directly.

## Detect the toolchain — never hardcode it

Before running anything, read, in order of preference:

1. The repo's own instruction file (`CLAUDE.md` / `AGENTS.md`) — if it names a check
   recipe (a specific command or script), use that verbatim and skip the steps below.
2. `turbo.json` — if present, prefer the repo's Turbo pipeline for cache + native
   parallelism (e.g. `turbo run typecheck lint build test`), scoped to changed packages.
3. `package.json` `scripts` — look for `typecheck`/`tsc`, `lint`, `build`, `test` entries
   and use them as-is; don't invent flags they don't already use.
4. `Makefile` — targets like `check`, `lint`, `test`, `build`.
5. `pyproject.toml` — tool sections (`ruff`, `mypy`, `pytest`) or a `[tool.poe]`/`nox`/`tox`
   task.
6. `Cargo.toml` — `cargo check`, `cargo clippy --fix`, `cargo test`, `cargo build`.
7. `go.mod` — `go vet ./...`, `go build ./...`, `go test ./...`.

If multiple signals exist, the instruction file wins, then the task runner (Turbo), then
raw package-manager scripts. State which recipe you're using before running it.

## Scope

- *(no argument)* — **uncommitted changes only**: `git diff --name-only` / `git diff`. This
  is the fast path and covers most real invocations.
- `branch` / `all` — full diff vs the repo's base branch (`git diff <base>...HEAD`).
- `slop` | `types` | `lint` | `build` | `test` | `security` — run only that phase, directly,
  no background agents; overhead isn't worth it for a single phase.

## Band 0 — background dependency/security audit

Independent of everything else; never blocks Band 1/2. Only for `branch`/`all` scope or
explicit `security` scope (skip by default — dependency changes are rare mid-iteration).

Use the repo's own audit command (e.g. `npm audit`, `pip-audit`, `cargo audit`,
`govulncheck`). For each finding with a non-breaking fix available, apply it and re-run to
verify. Flag major-version bumps or transitive findings with no direct fix for human review
— never auto-install a major version.

## Band 1 — sequential, self-healing (max 5 iterations)

Runs in the main context because it edits source files.

```
deslop (once, over the scoped diff — see below)
codegen (once, if the repo has a generated-types step — not self-healed)
iteration = 0, MAX = 5
while iteration < MAX:
    static analysis: types, then lint/format (repo's own commands)
    all clean? → break
    categorize failures → auto-fixable vs needs-human-review
    no auto-fixable remaining? → break
    apply auto-fixable fixes → iteration++
STOP at MAX and report remaining failures — do not loop forever
```

**Deslop** — scan the scoped diff for residue that compiles and lints clean but shouldn't ship.
Only in code *this change touched*; never sweep the whole repo. Language-agnostic list:

- Debug output left behind: `console.log`/`debugger`, `print`/`pp`, `dbg!`, `fmt.Println`
- Commented-out code (>2 consecutive commented lines) and dead/unreachable branches
- Suppressions with no documented reason: `@ts-ignore`, `eslint-disable`, `# noqa`,
  `#[allow(...)]`, `//nolint`
- Escape-hatch types where a real one exists: `any`, `interface{}`, bare `except:`
- Magic numbers and hardcoded strings that the repo elsewhere names as constants
- Comments that restate the code, and generated attribution/authorship comments

Match the repo's existing conventions — if the codebase already does something, that's the
pattern, not a finding. Anything ambiguous goes to needs-human-review, not auto-fix.

**Auto-fixable**: missing/unused imports, simple type mismatches, missing return-type
annotations, the deslop items above, anything the repo's own `lint --fix`/formatter handles.

**Needs human review** (flag, don't touch): complex generic/inference errors, errors in
generated-code directories, public API/contract changes, circular dependencies, security
concerns (`eval`, `dangerouslySetInnerHTML`-equivalents, hardcoded secrets).

Never edit generated-code directories directly — re-run codegen instead. Record every fix:
file, line, finding, action.

## Band 2 — parallel, read-only

After Band 1 converges, run build and tests. Use sub-agents/background jobs to run them
concurrently if your harness supports it; otherwise run sequentially. Both are report-only
— do not modify files here. If a failure overlaps a Band 1 auto-fixable category, fix it in
the main context and re-run the single failed command directly to verify (not via agent) —
**at most once per failing command**, then report whatever still fails.

Skip Band 2 when `--fix-only` is passed.

## Converge or fail loud

Report pass/fail per phase. On any failure, include the verbatim first failure (command +
error). Never report a phase as passing if it was skipped, timed out, or you didn't
actually run it — name it as skipped with the reason instead.

## `--commit`

On green only (all run phases pass, zero needs-human-review items blocking), invoke
`smart-commit`. If anything failed or is pending human review, do not commit — report why.

## Final report

```
## Check Results

**Scope**: Uncommitted | Branch (vs <base>) | <phase>
**Status**: PASS | FAIL (N remaining)
**Iterations**: X of 5

| Band | Phase   | Status | Issues | Fixed | Remaining |
|------|---------|--------|--------|-------|-----------|
| 0    | Security| ...    | N      | M     | K         |
| 1    | Static  | ...    | N      | M     | K         |
| 2    | Build   | ...    | N      | M     | K         |
| 2    | Tests   | ...    | N      | M     | K         |

### Needs human review
For each: what, why not auto-fixed, suggested approach.
```

Clean run → **"All checks passed. No issues found."**
