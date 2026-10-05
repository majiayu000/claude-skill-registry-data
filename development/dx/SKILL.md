---
name: dx
description: "Audit developer experience and generate a DX health score. Evaluates devcontainer, git hooks, linting, build caching, environment setup, and release pipeline. Use when you want to check how easy it is to onboard, improve developer workflow, score project tooling maturity, or find gaps in your dev setup."
version: "2.0.0"
category: productivity
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Do NOT pause for confirmation.
Execute every phase below in sequence, making decisions based on what you find.

============================================================
PHASE 0 — INPUT
============================================================

$ARGUMENTS may contain:
- `--fix` — automatically apply fixes and generate missing configs (default: report only)
- `--focus=AREA` — limit scan to a specific area: `devcontainer`, `hooks`, `lint`, `env`, `monorepo`, `release`
- `--score-only` — output just the numeric scores, skip recommendations

If no arguments are provided, run a full audit in report-only mode.

============================================================
PHASE 1 — STACK DETECTION
============================================================

Detect the project stack by scanning for manifest files:

- **Language**: `package.json` (Node/TS), `pyproject.toml`/`requirements.txt` (Python), `go.mod` (Go), `Cargo.toml` (Rust), `pubspec.yaml` (Flutter/Dart), `Gemfile` (Ruby)
- **Package manager**: `package-lock.json` (npm), `yarn.lock` (yarn), `pnpm-lock.yaml` (pnpm), `bun.lockb` (bun)
- **Framework**: read dependencies for Next.js, Fastify, Django, FastAPI, etc.
- **Monorepo**: `turbo.json`, `nx.json`, `pnpm-workspace.yaml`, `lerna.json`, root `workspaces` in package.json
- **CI provider**: `.github/workflows/`, `.gitlab-ci.yml`, `.circleci/config.yml`, `Jenkinsfile`, `bitbucket-pipelines.yml`

Record the detected stack — it drives all subsequent scoring.

============================================================
PHASE 2 — AUDIT SIX DX AREAS
============================================================

Scan the project root and score each area on a 0-10 scale:

**2.1 — Dev Container (0-10)**

Check for:
- `.devcontainer/devcontainer.json` exists (+3)
- `Dockerfile` or `image` specified in devcontainer config (+2)
- `features` or `postCreateCommand` configured (+2)
- VS Code `extensions` list present and matches detected stack (+1)
- `forwardPorts` configured for detected services (+1)
- Docker Compose integration for multi-service setups (+1)

Score 0 if `.devcontainer/` directory does not exist.

**2.2 — Git Hooks (0-10)**

Check for:
- `.husky/` directory OR `.lefthook.yml` OR `.pre-commit-config.yaml` exists (+3)
- Pre-commit hook configured: lint + format (+2)
- Pre-commit hook runs type-check (+1)
- Commit-msg hook enforces conventional commits (+2)
- Lint-staged or equivalent for incremental checks (+1)
- Hook runner matches stack (husky for Node, pre-commit for Python, lefthook for polyglot) (+1)

Score 0 if no hook tooling is detected.

**2.3 — Linting & Formatting (0-10)**

Check for:
- Linter config exists: `.eslintrc.*` / `eslint.config.*` / `biome.json` / `ruff.toml` / `.golangci.yml` / `.rubocop.yml` (+3)
- Formatter config exists: `.prettierrc*` / `biome.json` / `pyproject.toml [tool.black]` (+2)
- Editor config: `.editorconfig` (+1)
- VS Code settings: `.vscode/settings.json` with format-on-save (+1)
- Lint script in package.json / pyproject.toml / Makefile (+1)
- No conflicting configs (e.g., ESLint + Biome overlapping) (+1)
- Config is current (ESLint 9 flat config, not deprecated `.eslintrc.json`) (+1)

**2.4 — Build Tooling & Caching (0-10)**

Check for:
- `turbo.json` or `nx.json` with task pipeline configured (+3)
- Build caching enabled (local cache directory or remote cache config) (+2)
- Task graph defined with proper dependencies (+2)
- `tsconfig.json` project references (TypeScript composite builds) (+1)
- Incremental builds configured (+1)
- Dev server script exists and uses watch mode (+1)

Score N/A if project is not a monorepo and has no build step.

**2.5 — Environment Setup (0-10)**

Check for:
- `.env.example` or `.env.template` exists with documented variables (+3)
- `docker-compose.yml` for local services (database, cache, etc.) (+2)
- Setup script: `Makefile`, `scripts/setup.sh`, or `just` / `task` taskfile (+2)
- `.tool-versions` or `.nvmrc` or `.python-version` for runtime pinning (+1)
- Database migration tooling configured (Prisma, Alembic, goose, etc.) (+1)
- README has "Getting Started" section with fewer than 5 steps (+1)

**2.6 — Release Pipeline (0-10)**

Check for:
- Semantic-release or changesets or equivalent configured (+3)
- Conventional commits enforced (commitlint + husky or equivalent) (+2)
- CHANGELOG.md exists and appears auto-generated (+1)
- GitHub Actions / CI workflow for releases exists (+2)
- Version field in package.json / pyproject.toml / Cargo.toml is not `0.0.0` placeholder (+1)
- Git tags exist following semver pattern (+1)

============================================================
PHASE 3 — CALCULATE DX HEALTH SCORE
============================================================

Compute the overall DX health score:

- **Overall Score** = average of all applicable area scores (skip N/A areas)
- **Grade**: A (9-10), B (7-8.9), C (5-6.9), D (3-4.9), F (0-2.9)

Classify each area:
- **Strong** (8-10): well-configured, no action needed
- **Adequate** (5-7): functional but has gaps
- **Weak** (2-4): partially set up, needs work
- **Missing** (0-1): not configured at all

============================================================
PHASE 4 — GENERATE RECOMMENDATIONS
============================================================

For each area scored below 8, generate specific recommendations:

- What is missing and why it matters
- Estimated setup effort: `quick` (< 5 min), `medium` (15-30 min), `involved` (1+ hr)
- Which sub-skill to run: `/devcontainer`, `/git-hooks`, `/linter`, `/env-setup`, `/monorepo`, `/release`
- Priority: `critical` (score 0-2), `high` (3-5), `medium` (6-7)

Sort recommendations by priority (critical first), then by effort (quick first).

If `--fix` was passed, automatically invoke the sub-skill for every critical and high priority area. Run them in sequence since some depend on others (e.g., `/linter` before `/git-hooks`).


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After completing, validate the output was produced correctly:

1. Verify generated files exist and are syntactically valid.
2. Run any available validation (lint, type-check, dry-run).
3. If the skill produces configuration, verify it parses without errors.

IF VALIDATION FAILS:
- Diagnose from error context and re-generate the failing artifact
- Repeat up to 2 iterations

============================================================
OUTPUT
============================================================

Print the DX Health Report:

```
## DX Health Report

### Project: {name}
### Stack: {language} / {framework} / {package-manager}
### Overall: {score}/10 ({grade})

| Area             | Score | Status  |
|------------------|-------|---------|
| Dev Container    | X/10  | {status}|
| Git Hooks        | X/10  | {status}|
| Lint & Format    | X/10  | {status}|
| Build & Cache    | X/10  | {status}|
| Environment      | X/10  | {status}|
| Release Pipeline | X/10  | {status}|

### Recommendations (by priority)
1. {area} — {what's missing} — run `/sub-skill` ({effort})
2. ...

### Quick Wins (under 5 minutes)
- {actionable items that can be done immediately}
```

============================================================
NEXT STEPS
============================================================

1. Run individual sub-skills for areas that need improvement:
   - `/devcontainer` — generate dev container configuration
   - `/git-hooks` — set up pre-commit and commit-msg hooks
   - `/linter` — configure linting and formatting
   - `/env-setup` — automate local environment bootstrap
   - `/monorepo` — set up monorepo tooling and caching
   - `/release` — configure automated release pipeline
2. Re-run `/dx` after fixes to verify score improvement
3. Run `/dx --fix` to auto-apply all critical and high priority fixes


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /dx — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT modify any files unless `--fix` was explicitly passed
- Do NOT score areas that are not applicable to the detected stack
- Do NOT recommend monorepo tooling for single-package projects
- Do NOT recommend tools that conflict with existing configs (e.g., Biome when ESLint is established)
- Do NOT inflate scores — be honest about gaps
- Do NOT skip the stack detection phase — every recommendation must be stack-appropriate
