---
name: universal-format-lint
description: Run language-appropriate formatter and lint-fix commands for changed files. Use when the user asks to format, lint, auto-fix, or clean code style across Python, JavaScript/TypeScript, Markdown, YAML/JSON, PowerShell, shell scripts, and similar files.
agent:
  display_name: "Universal Format Lint"
  short_description: "Run format/lint fixes by file type"
  default_prompt: "Apply formatter and lint-fix commands to changed files, grouped by language and run in the configured order."
---

# Universal Format Lint

Apply formatting and lint fixes by file type, with deterministic order and minimal scope.

## Core workflow

1. Detect changed tracked files first:
`git diff --name-only --diff-filter=ACMRTUXB`
2. Include untracked files when relevant:
`git ls-files --others --exclude-standard`
3. Group files by extension and run only matching tools.
4. Run formatters before lint-fixers.
5. Re-run the formatter if the linter applies structural fixes.
6. Keep fixes scoped to files involved in the task unless the user asks for repo-wide formatting.

## Python (`.py`, `.pyi`)

Run in this order:
1. `isort <files>`
2. `black <files>`
3. `ruff check --fix <files>`
4. `black <files>` (only if Ruff changed files)

If available, prefer project runner wrappers (`uv run`, `poetry run`, `pipenv run`) to match the repo environment.

## JavaScript and TypeScript (`.js`, `.jsx`, `.ts`, `.tsx`, `.mjs`, `.cjs`)

Preferred order:
1. `prettier --write <files>`
2. `eslint --fix <files>`
3. `prettier --write <files>` (if ESLint changed files)

If the repo uses package scripts, prefer script entrypoints:
- `npm run format -- <files>`
- `npm run lint:fix -- <files>`

## Markdown, JSON, YAML (`.md`, `.markdown`, `.json`, `.jsonc`, `.yml`, `.yaml`)

Use Prettier when available:
- `prettier --write <files>`

Optionally run lint fixers if configured:
- `markdownlint --fix <md-files>`

## PowerShell (`.ps1`, `.psm1`, `.psd1`)

Run in this order:
1. `Invoke-Formatter -Path <files>` (PSScriptAnalyzer)
2. `Invoke-ScriptAnalyzer -Path <files> -Fix`
3. `Invoke-Formatter -Path <files>` (if analyzer changed files)

## Shell (`.sh`, `.bash`, `.zsh`)

Run when tools exist:
1. `shfmt -w <files>`
2. `shellcheck -f gcc <files>` (report or auto-fix mode if configured)

## Missing tools and safety

1. Verify tool availability before running (`Get-Command <tool>` or equivalent).
2. If a required tool is missing, report exactly which tool is missing and continue with available tools.
3. Do not install dependencies unless the user asks.
4. Do not broaden scope silently; ask before running repository-wide fixes.

## Command construction rules

1. Quote paths safely for the current shell.
2. Chunk very long file lists to avoid command-length limits.
3. Skip deleted files and generated/vendor directories unless user requests otherwise.
4. After fixes, show a concise summary of files changed per tool.

## Quick default recipe

For mixed-language repos, use this default sequence:
1. Python: `isort` -> `black` -> `ruff --fix`
2. JS/TS + docs/data formats: `prettier --write` -> `eslint --fix`
3. PowerShell: `Invoke-Formatter` -> `Invoke-ScriptAnalyzer -Fix`
4. Shell: `shfmt -w` -> `shellcheck`

## Bundled lint script

A bundled script at `scripts/format-lint.ps1` (PowerShell) auto-runs formatters per file extension group:

```powershell
.\scripts\format-lint.ps1 -Files file.py,file.js,file.md
.\scripts\format-lint.ps1 -Files file.py,file.js -DryRun
```

Groups files by extension and runs the correct tool chain for each: Python (isort → black → ruff), JS/TS (prettier → eslint), docs/data (prettier), PowerShell (Formatter → ScriptAnalyzer), shell (shfmt → shellcheck).

To use as a project-local tool:

```powershell
cp <skill-path>/universal-format-lint/scripts/format-lint.ps1 .ai_scripts/
.ai_scripts\format-lint.ps1 -Files file.py,file.js,file.md
```

## Cross-references

- **dont-kill-tokens** — Batched formatting saves tokens.

- **follow-existing-patterns** — Formatting should match project conventions.

- **self-validate** — Syntax validation complements linting.
- **project-scripts** — After creating or modifying scripts via project-scripts, run formatters to ensure consistent style across script files.
- **release-changelog** — After writing a changelog entry, run the project's Markdown formatter to keep the changelog consistently styled.
- **skill-loader** — Apply the capped selection policy when deciding which formatting guardrails should also be active.
