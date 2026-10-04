---
model_tier: medium
name: quality-tools
description: "Use when PHPStan, Rector, or ECS output appears — \"phpstan says mixed\", type errors, \"fix code style\", \"run rector\" — even when Eloquent/Laravel/model code is also mentioned."
domain: quality
scope:
  write:
    - pattern: "**"
      access: "write"
  verification_reason: "the project's own formatters and fixers rewrite source in place, and WHICH paths is decided by the consumer's tool config rather than by this skill. A narrower glob would be a guess about a tree this package does not own."
execution:
  type: assisted
  handler: shell
  allowed_tools: []
recommended_for_user_types: [developer]
workspaces:
  - engineering
packs:
  - engineering-base
---

# quality-tools

## When to use

Use this skill whenever running or configuring code quality tools:

- **PHP**: PHPStan (static analysis), Rector (automated refactoring), ECS (coding standards)
- **JS/TS**: Biome (linting + formatting), TypeScript compiler (type checking), Jest/Vitest (tests)
- **Python**: Ruff (linting + formatting), mypy (type checking), pytest (tests)
- **Go**: `gofmt`, `go vet`, optionally golangci-lint, `go test`

## Modes

This skill is a router head. The cross-mode material — execution policy,
language detection, environment, output, gotchas — lives below. The per-tool
procedure bodies live in `references/`; load exactly the mode the detected
stack calls for.

| Detected stack | Mode body | Covers |
|---|---|---|
| PHP (`.php` changed) | [`references/php-tools.md`](references/php-tools.md) | Tool detection, PHPStan / ECS / Rector commands and flags, combined pipeline, config files, baseline policy, PHPStan error handling, testing framework, git-aware execution |
| JS/TS (`.js` / `.ts` / `.tsx` changed) | [`references/js-ts-tools.md`](references/js-ts-tools.md) | Detection, Biome, TypeScript type checking, Jest / Vitest, the JS/TS workflow sequence |
| Python (`.py` changed, or `pyproject.toml`) | [`references/python-tools.md`](references/python-tools.md) | Detection from `pyproject.toml`, Ruff, mypy, pytest, the workflow sequence, virtualenv and `setup.cfg` gotchas |
| Go (`.go` changed, or `go.mod`) | [`references/go-tools.md`](references/go-tools.md) | `gofmt`, `go vet`, golangci-lint where present, `go test`, the workflow sequence, vendor and build-tag gotchas |

More than one stack changed → load each mode body and run each pipeline.

**The resolver decides which row applies, not the file extension alone.**
`resolve_toolchain` returns the ecosystems it found and the quality commands
per ecosystem; the rows above name what those commands are. A TypeScript
repository resolves the ecosystem `js`, never `typescript` — the pack name and
the ecosystem label are different vocabularies.

## Execution policy — on demand only, never proactive

```
NEVER RUN QUALITY TOOLS PROACTIVELY WHEN quality.local_auto_run IS
false OR MISSING (THE DEFAULT). DO NOT ASK WHETHER TO RUN THEM.
THE USER RUNS THEM MANUALLY. REMOTE CI IS THE AUTHORITATIVE GATE.
```

Toolchains differ per language and project and are often unknown to the
agent — discovering and running them burns time and tokens. Under the
default, exactly three triggers justify running a quality tool:

1. **Explicit ask this turn** — the user says so or invokes `/fix quality`.
2. **Concrete CI failure** — the remote pipeline reports a failing
   check; run exactly that failing check to reproduce and fix it
   (`/fix:ci` is the canonical flow).
3. **New-gate carve-out** — the change itself introduces a NEW CI gate,
   smoke test, or test file; it must run once locally to be proven.

`quality.local_auto_run: true` restores the legacy autonomous behaviour
(run the pipeline when work is ready for verification). When runs are
suppressed, the completion message says *"quality gates delegated to
remote CI"* — never that the tools passed.

## Language detection

Detect which tools to run based on **what files were changed**:

```bash
# Check changed file extensions (diff against base branch)
git diff --name-only origin/main..HEAD | grep -E '\.(php)$'       # → PHP tools
git diff --name-only origin/main..HEAD | grep -E '\.(js|ts|tsx)$'  # → JS/TS tools
```

If both PHP and JS/TS files changed → run **both** pipelines.

## Procedure

1. Confirm a run is justified — see Execution policy above. No trigger, no run.
2. Detect the stack from the changed files — see Language detection above.
2b. **Inspect the project's own quality config before running anything.** Read
   the config files the detected stack actually ships (`phpstan.neon`,
   `ecs.php`, `rector.php`, `biome.json`, `tsconfig.json`, the `scripts` block
   of `package.json`) and the task/make wrapper if one exists. Never assume a
   default ruleset, a default baseline, or a default command — the mode body
   names where to look per stack. Running a tool against assumed config
   produces findings the project never asked for.
3. Load the matching mode body from the table in Modes and follow its
   procedure. PHP → [`references/php-tools.md`](references/php-tools.md)
   § Procedure: Run quality checks. JS/TS →
   [`references/js-ts-tools.md`](references/js-ts-tools.md)
   § JS/TS Quality Workflow.
4. Both stacks changed → run both mode procedures; neither result excuses the
   other.
5. Report per Output format below.

## Related rules and guidelines

- `verify-before-complete` rule — no pass claims without fresh output; suppressed runs are surfaced as "delegated to remote CI", never claimed
- `php-coding` rule → PHPStan section — inline ignores, PHPDoc rules
- `contexts/execution/verification-mechanics.md` — Gate zero (`local_auto_run`) + timing when `true` (quality tools ONCE at the end, not after each edit)
- [`testing-anti-patterns`](../testing-anti-patterns/SKILL.md) and
  [`process-anti-patterns.md`](../testing-anti-patterns/process-anti-patterns.md) —
  test-side rationalizations these tools cannot catch (e.g. "CI is red,
  patch first, test later").

---

## Execution environment

### PHP tools

All PHP commands run **inside the Docker container** (`make console` or `docker compose exec`).

### JS/TS tools

JS/TS commands run on the **host** or in a **Node container**, depending on the project setup:

1. Check if a `Makefile` / `Taskfile.yml` has targets for linting/testing.
2. Check if `docker-compose.yml` has a Node service.
3. If neither → run on the host directly.

## Output format

1. Tool exit code and error count summary
2. Fixed issues or remaining errors to address

## Auto-trigger keywords

- quality check
- quality fix
- PHPStan
- Rector
- ECS
- code style
- lint
- Biome
- type check
- tscheck

## Gotcha

- Always check exit code first — if 0, don't read output (saves tokens).
- Rector + ECS can introduce PHPStan errors — always re-run PHPStan after fixing.
- A project-specific `quality:*` wrapper may expose different flags than the native tools — check the project's wrapper before assuming flags.
- Docker commands need `-T` flag to avoid TTY issues in non-interactive mode.

## Do NOT

- Do NOT run `vendor/bin/phpstan` or `vendor/bin/ecs` directly — use the wrapper.
- Do NOT manually edit `phpstan-baseline.neon` — it's auto-managed.
- Do NOT skip type checking (`tsc --noEmit`) for TypeScript projects.
- Do NOT run Biome without `--write` if the intent is to fix (otherwise it's dry-run only).
- Do NOT mix ESLint + Biome in the same project — check which one is active.
