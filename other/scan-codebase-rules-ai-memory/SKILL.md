---
name: scan-codebase-rules-ai-memory
description: Scan the current repo's structure, config files, and code to extract concrete conventions (lint/format rules, naming, folder layout, commit style, CI checks, testing conventions) and persist them as durable rule pages in ai-memory for future sessions. Use when user says "scan codebase for rules", "extract conventions", "analyze repo and save to memory", "record project conventions", or "generate ai-memory rules from this repo".
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Scan Codebase Rules

Scans the repo for conventions and configuration, then writes each distinct rule as its own durable page in ai-memory (`memory_write_page`) so future sessions apply them without rediscovery.

Full scan every run — no incremental/diff state to track. Scope is conventions + config only: linting, formatting, naming, folder layout, commit message style, CI/CD checks, testing setup. Do NOT extract business logic, feature descriptions, or architecture rationale — that belongs to other skills/memory types.

## Instructions

### Step 1: Check for existing rules first

Call `memory_query` with query like `"rule OR convention OR lint"` (and `tags: ["codebase-rule"]` if supported) to see what's already recorded. Skip re-writing unchanged rules; update pages whose content has drifted (e.g. lint config changed).

### Step 2: Gather source signals

Read/grep the following if present — skip any that don't exist, don't guess their content:

- **Formatting/lint**: `.eslintrc*`, `.prettierrc*`, `.editorconfig`, `pyproject.toml` (`[tool.ruff]`/`[tool.black]`), `rustfmt.toml`, `.golangci.yml`
- **Naming/structure**: top-level folder layout (`src/`, `lib/`, `packages/`, `apps/`), module/file naming pattern (kebab-case vs snake_case vs PascalCase) — sample 10-20 filenames, don't assume from one file
- **Commit style**: `git log --oneline -30` — detect Conventional Commits or other prefix pattern; check for `commitlint.config.*`
- **CI/CD**: `.github/workflows/*.yml`, `.gitlab-ci.yml` — required checks (test, lint, typecheck, build) and when they run (PR vs push vs merge)
- **Testing**: test framework config (`jest.config.*`, `vitest.config.*`, `pytest.ini`, `go test` conventions), coverage thresholds, test file naming/location convention
- **Package manager / build**: lockfile present (`package-lock.json`, `pnpm-lock.yaml`, `poetry.lock`, `Cargo.lock`) tells you the required tool
- **Existing project docs**: `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md` — if a rule is already documented there, do NOT duplicate it into ai-memory; note the pointer instead (ai-memory should hold what ISN'T already in checked-in docs)

Use `Grep`/`Read`/`Bash(git log)` directly for this — do not spawn a subagent unless the repo is unusually large (monorepo with many packages), in which case dispatch one Explore agent per top-level package.

### Step 3: Distill into atomic rules

For each convention found, write ONE short, falsifiable rule statement — not a summary of the config file. Bad: "the project uses eslint." Good: "Use single quotes and no semicolons (Prettier: `singleQuote: true, semi: false`)." Group tightly-related settings (e.g. all Prettier options) into one page; keep unrelated domains (lint vs commit style vs CI) as separate pages.

Skip anything already enforced by an unambiguous config file the agent will read directly anyway (e.g. don't write a rule for exact indent width — that's mechanical and tools apply it automatically). Prioritize rules that require judgment to follow: naming conventions, when to add tests, what CI gates block merge, commit message format.

### Step 4: Write pages to ai-memory

For each distilled rule, call `memory_write_page`:

- `path`: `rules/<topic>.md` (e.g. `rules/lint-format.md`, `rules/commit-style.md`, `rules/ci-checks.md`, `rules/naming-structure.md`, `rules/testing.md`)
- `body`: start with `# <Topic> Rules` (H1), then the rule statements as a bullet list, each with a one-line source citation (e.g. `(source: .eslintrc.json)`)
- `tags`: `["codebase-rule", "<topic>"]`
- `tier`: `semantic`
- `pinned`: `true` — these are stable facts about the repo, not decaying notes

If a page for that path already exists with different content, overwrite it (memory_write_page updates by path). If content is unchanged, skip the write.

### Step 5: Report

Summarize to the user: how many rule pages written/updated/skipped, and which topics. List anything skipped because it was already covered in CLAUDE.md/AGENTS.md (so the user knows why it's not duplicated).

## Examples

### Example 1: TypeScript monorepo

User says: "scan codebase for rules"
Actions: query existing rules → read `.eslintrc.json`, `.prettierrc`, `.github/workflows/ci.yml`, `git log --oneline -30` → find ESLint airbnb-base + Prettier singleQuote, Conventional Commits enforced by commitlint, CI runs lint+test+build on every PR → write `rules/lint-format.md`, `rules/commit-style.md`, `rules/ci-checks.md`
Result: 3 pages written, pinned, tagged `codebase-rule`

### Example 2: Nothing new to add

User says: "extract conventions again"
Actions: query existing rules, find all 5 topic pages already present and configs unchanged
Result: report "0 updated, 5 already current" — no writes

## Troubleshooting

### No config files found for a category

Cause: repo doesn't enforce that convention (e.g. no lint config).
Solution: skip that topic entirely — do not invent a rule from inferred style alone unless it's extremely consistent across 20+ sampled files, and even then label it `(inferred from convention, no enforcing config)`.

### Rule would just duplicate CLAUDE.md/AGENTS.md

Cause: project already documents it in checked-in instructions.
Solution: don't write to ai-memory — those files are already loaded every session. Mention the pointer in the final report instead.
