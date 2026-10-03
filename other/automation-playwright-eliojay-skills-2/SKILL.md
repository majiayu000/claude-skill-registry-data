---
name: "automation-playwright"
description: "Use when the task requires automating a real browser from the terminal (navigation, form filling, snapshots, screenshots, data extraction, UI-flow debugging) via `playwright-cli` or the bundled wrapper script. Do not use for: designing or writing a repeatable integration or E2E test suite in CI (use integration-e2e-testing), unit tests (use code-testing), static code review (use code-review-deep-zh), or visual design decisions for a new UI (use frontend-design)."
---


# Playwright CLI Skill

Drive a real browser from the terminal using `playwright-cli`. Prefer the bundled wrapper script so the CLI works even when it is not globally installed.
Treat this skill as CLI-first automation. Do not pivot to `@playwright/test` unless the user explicitly asks for test files.

## Prerequisite check (required)

Before proposing commands, check whether `npx` is available (both wrappers depend on it).

Bash:

```bash
command -v npx >/dev/null 2>&1
```

PowerShell:

```powershell
Get-Command npx -ErrorAction Stop
```

If it is not available, pause and ask the user to install Node.js/npm (which provides `npx`). Provide these steps verbatim:

```bash
# Verify Node/npm are installed
node --version
npm --version

# If missing, install Node.js/npm, then:
npm install -g @playwright/cli@latest
playwright-cli --help
```

Once `npx` is present, proceed with the wrapper script. A global install of `playwright-cli` is optional.

## Run from the skill directory

Use the wrapper for the current shell from this skill's directory. Both paths are relative so the skill works regardless of where it was installed:

```bash
./scripts/playwright_cli.sh --help
```

```powershell
.\scripts\playwright_cli.ps1 --help
```

## Quick start

Use the wrapper script:

```bash
./scripts/playwright_cli.sh open https://playwright.dev --headed
./scripts/playwright_cli.sh snapshot
./scripts/playwright_cli.sh click e15
./scripts/playwright_cli.sh type "Playwright"
./scripts/playwright_cli.sh press Enter
./scripts/playwright_cli.sh screenshot
```

On PowerShell, replace `./scripts/playwright_cli.sh` with `.\scripts\playwright_cli.ps1`; the arguments are identical.

If the user prefers a global install, this is also valid:

```bash
npm install -g @playwright/cli@latest
playwright-cli --help
```

## Core workflow

1. Open the page.
2. Snapshot to get stable element refs.
3. Interact using refs from the latest snapshot.
4. Re-snapshot after navigation or significant DOM changes.
5. Capture artifacts (screenshot, pdf, traces) when useful.

Minimal loop:

```bash
./scripts/playwright_cli.sh open https://example.com
./scripts/playwright_cli.sh snapshot
./scripts/playwright_cli.sh click e3
./scripts/playwright_cli.sh snapshot
```

## When to snapshot again

Snapshot again after:

- navigation
- clicking elements that change the UI substantially
- opening/closing modals or menus
- tab switches

Refs can go stale. When a command fails due to a missing ref, snapshot again.

## Recommended patterns

### Form fill and submit

```bash
./scripts/playwright_cli.sh open https://example.com/form
./scripts/playwright_cli.sh snapshot
./scripts/playwright_cli.sh fill e1 "user@example.com"
./scripts/playwright_cli.sh fill e2 "password123"
./scripts/playwright_cli.sh click e3
./scripts/playwright_cli.sh snapshot
```

### Debug a UI flow with traces

```bash
./scripts/playwright_cli.sh open https://example.com --headed
./scripts/playwright_cli.sh tracing-start
# ...interactions...
./scripts/playwright_cli.sh tracing-stop
```

### Multi-tab work

```bash
./scripts/playwright_cli.sh tab-new https://example.com
./scripts/playwright_cli.sh tab-list
./scripts/playwright_cli.sh tab-select 0
./scripts/playwright_cli.sh snapshot
```

## Wrapper script

The wrapper script uses `npx --package @playwright/cli playwright-cli` so the CLI can run without a global install:

```bash
./scripts/playwright_cli.sh --help
```

Prefer the wrapper unless the repository already standardizes on a global install.

## References

Open only what you need:

- CLI command reference: `references/cli.md`
- Practical workflows and troubleshooting: `references/workflows.md`

## Guardrails

- Always snapshot before referencing element ids like `e12`.
- Re-snapshot when refs seem stale.
- Prefer explicit commands over `eval` and `run-code` unless needed.
- When you do not have a fresh snapshot, use placeholder refs like `eX` and say why; do not bypass refs with `run-code`.
- Use `--headed` when a visual check will help.
- When capturing artifacts in this repo, use `output/playwright/` and avoid introducing new top-level artifact folders.
- Default to CLI commands and workflows, not Playwright test specs.
