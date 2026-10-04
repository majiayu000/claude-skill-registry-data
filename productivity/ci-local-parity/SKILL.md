---
name: ci-local-parity
description: Reproduce ai-repo PR checks locally with Poe and CI scripts, including per-package typecheck and coverage behavior. Use when validating changes before push or when user asks which local commands match CI.
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "1.0.0"
  languages: python
  audience: developers
  workflow: automation
  since: "2026-05-07"
---

## What I do

Run `ai` repository checks locally with the closest possible parity to PR CI:

- Map changed files to affected packages
- Run checks in CI order: format-check → lint → test → typecheck → coverage → depcheck
- Apply per-package behavior (strict vs baseline typecheck, test args, extras)
- Highlight checks that cannot be fully reproduced via Poe

## When to use me

- User asks how to run CI checks locally in `ai`
- User wants the exact local commands before opening/updating a PR
- User asks about Poe tasks vs CI scripts and where they differ

## Use instead

- `ci-fix` — diagnosing an already-failed CI run
- `ruff` — lint/format-only cleanup without CI parity
- `uv` — dependency/lockfile maintenance

---

## Workflow

### Step 0: Preconditions

Run from the repo root. Verify tooling:

```bash
uv --version
uv run poe --help
```

If `uv` is missing, stop and ask the user to install it.

---

### Step 1: Determine target packages

```bash
git fetch origin main
git diff --name-only origin/main...HEAD
```

Map changed files to packages using the `dir` field in:
`.github/actions/get-packages-matrix/package_configuration.json`

→ See [references/package-matrix.md](references/package-matrix.md) for the full package list.

---

### Step 2: Run baseline checks (CI order)

From inside each package directory:

```bash
uv run ruff format --check .   # CI lint = format check + lint check
uv run poe lint
uv run poe test
uv run poe depcheck
```

> `poe format` writes files — it is **not** equivalent to the CI lint step.

---

### Step 3: Typecheck (strict vs baseline)

Determine mode from `package_configuration.json` flags:

- **Strict** (`typecheck_use_baseline: false`, `typecheck_require_zero_errors: true`):
  ```bash
  uv run poe typecheck
  ```
- **Baseline** (new errors vs `origin/main` only):
  ```bash
  uv run poe ci-typecheck
  # fallback if task missing:
  bash "$(git rev-parse --show-toplevel)/.github/scripts/dev.sh" typecheck --dir .
  ```

→ See [references/package-matrix.md](references/package-matrix.md) for per-package mode.

---

### Step 4: Coverage (diff-based)

```bash
uv run poe ci-coverage
# fallback if task missing:
bash "$(git rev-parse --show-toplevel)/.github/scripts/dev.sh" coverage --dir .
```

Full-package (non-diff) coverage:
```bash
uv run poe coverage
```

---

### Step 5: Call out CI gaps

Some jobs are not reproducible via Poe. Note them explicitly; do not claim full parity.

→ See [references/ci-gaps.md](references/ci-gaps.md) for the full list (min-deps, config-check, PR policy).

---

## Quick recipes

### Any package — closest PR-CI parity

```bash
cd <package_dir>
uv run ruff format --check .
uv run poe lint
uv run poe test
uv run poe depcheck
uv run poe ci-typecheck || bash "$(git rev-parse --show-toplevel)/.github/scripts/dev.sh" typecheck --dir .
uv run poe ci-coverage  || bash "$(git rev-parse --show-toplevel)/.github/scripts/dev.sh" coverage  --dir .
```

### Strict packages: `unique_toolkit`, `unique_sdk`, `unique_skill_tool`

```bash
cd <package_dir>
uv run ruff format --check .
uv run poe lint
uv run poe test        # sdk: add -- -m "not integration"
uv run poe depcheck
uv run poe typecheck
uv run poe ci-coverage || bash "$(git rev-parse --show-toplevel)/.github/scripts/dev.sh" coverage --dir .
```

---

## Tips

1. Always include `ruff format --check` — CI lint is two commands, not one.
2. Check the matrix flags; don't assume strict or baseline mode.
3. Prefer `ci-*` Poe tasks for diff parity; fall back to `dev.sh` when absent.
4. Never claim full parity — deps/config/policy jobs require manual steps.
5. Run from the repo root so script paths and git base refs resolve correctly.
