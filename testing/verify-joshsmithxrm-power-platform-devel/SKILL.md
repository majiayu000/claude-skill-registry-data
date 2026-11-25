---
name: verify
description: Check that a PPDS change actually works in its running surface, beyond unit tests - drive the CLI binary, the TUI in a PTY (tui-verify.mjs), the VS Code extension's webviews over CDP (webview-cdp.mjs), the MCP server, or the .claude/ hooks and settings, and report observed values. Use after implementing a change and before opening a PR, or when asked to verify, smoke-test or screenshot a surface.
---

# Verify

Confirms a change works where it runs. Unit tests come first; this skill
covers what they cannot see. Mechanics (commands, keys, row maps, flags)
are in `REFERENCE.md`, by section.

## Usage

- `/verify` - pick the mode from the changed paths
- `/verify cli|tui|extension|mcp|workflow` - explicit mode

## Prerequisites

| Mode | Required |
|------|----------|
| cli | .NET SDK; builds `src/PPDS.Cli` |
| tui | `tests/PPDS.Tui.E2eTests/tools/tui-verify.mjs` with its npm deps (`@microsoft/tui-test`, `node-pty`); Windows only today (it launches `ppds.exe`) |
| extension | `src/PPDS.Extension/tools/webview-cdp.mjs` with its npm deps (`@playwright/test`, `@vscode/test-electron`) |
| mcp | `tests/PPDS.Mcp.Tests`; for a live check, an MCP client the user registers the built server in |
| workflow | Python with `pytest` |

If a prerequisite is missing, tell the user what to install and stop.

## Process

### 1. Detect the surface

From `$ARGUMENTS` or the changed paths:

| Changed path | Mode |
|--------------|------|
| `src/PPDS.Cli/Commands/` | cli |
| `src/PPDS.Cli/Tui/` | tui |
| `src/PPDS.Extension/` | extension |
| `src/PPDS.Cli/Commands/Serve/` (daemon RPC used by the extension) | extension, plus cli for `ppds serve` |
| `src/PPDS.Mcp/` | mcp |
| `src/PPDS.Cli/Services/` (Application Services, shared) | every surface that calls the changed service |
| `.claude/`, `scripts/` | workflow |

No match: ask.

### 2. Unit tests first

- CLI/TUI: `dotnet test PPDS.sln --filter "Category!=Integration" -v q`
- TUI logic only: `dotnet test PPDS.sln --filter "Category=TuiUnit"`
- Extension: `npm run ext:test`
- MCP: `dotnet test tests/PPDS.Mcp.Tests/PPDS.Mcp.Tests.csproj -v q`

Don't spend interactive cycles on code that fails its tests.

### 3. Safety pre-check

Any mode that reaches live Dataverse: run `REFERENCE.md` "Safety pre-check"
first. In particular, call the CLI as `ppds`, by its built path, or via
`dotnet run --project src/PPDS.Cli -- <args>` (with `--` before the
application arguments), so the shakedown safety hook can see it. The hook
covers the Bash tool and the PowerShell tool alike.

### 4. CLI mode

```bash
dotnet build src/PPDS.Cli/PPDS.Cli.csproj -f net10.0 -v q
src/PPDS.Cli/bin/Debug/net10.0/ppds <command> <args>
```

Check the exit code, that stdout holds only data and stderr the status,
and the edge cases (empty input, invalid input, no profile). Details:
`REFERENCE.md` "§cli — CLI Mode".

### 5. TUI mode

`REFERENCE.md` "§tui — TUI Mode": worked example (Phase A/B/C), commands,
keys, the 120x30 row map, error recovery. Phase B is mandatory when changed
files touch `src/PPDS.Cli/Tui/`.

### 6. Extension mode

`REFERENCE.md` "§ext — Extension Mode": worked example (Phase A/B/C), the
`--ext` rule, commands, exact command titles, Monaco and notebook caveats,
log locations. Phase B is mandatory when query, data or panel files change.

### 7. MCP mode

`REFERENCE.md` "§mcp — MCP Mode". Cover tools at protocol level in
`tests/PPDS.Mcp.Tests` (pattern: `Tools/FormsProtocolTests.cs`); for a live
check, have the user register the built server with `--read-only` in an MCP
client. Per tool: valid input gives the success shape, an edge case gives a
descriptive error, the arguments match the schema. Do not pipe raw JSON-RPC
into `ppds-mcp-server`; it needs the `initialize` handshake first.

### 8. Workflow mode

**Check 1 - Python tests:** run only the files that cover what you
changed, and leave the full `tests/` suite to CI (`workflow-tests.yml`),
because it starts hundreds of child processes (git, PowerShell) and flashes
console windows on Windows:
```bash
python -m pytest tests/test_hook_paths.py tests/test_snk_protect.py tests/hooks/test_shakedown_safety.py tests/test_skill_bash_portability.py -q -p no:cacheprovider
```
Hooks: `test_hook_paths.py`, `test_snk_protect.py`,
`hooks/test_shakedown_safety.py`. Skill files: `test_skill_bash_portability.py`.

**Check 2 - Hook scripts:** for `snk-protect.py`, `shakedown-safety.py`
and `shakedown-safety-launcher.py` in `.claude/hooks/` (`_pathfix.py` is a
helper): `echo '{}' | python .claude/hooks/{hook}.py`. Exit 0 or 2, never 1.
Fixture-driven checks: `REFERENCE.md` "§workflow — Workflow Infrastructure".

**Check 3 - settings.json:** parses; every hook `command` resolves to a
file on disk.

**Check 4 - Skill frontmatter:** every `.claude/skills/*/SKILL.md` parses;
`name` and `description` non-empty.

**Check 5 - Skill file refs:** every path a skill references exists.

### 9. Report

Use `REFERENCE.md` "Report template" with the values you observed (row
counts, timings, exit codes, screenshot paths).

Verify sits between build/test (per AGENTS.md) and opening a PR. On PASS,
open the PR. On FAIL, report and root-cause it; do not fix during verify.
After the fix lands, re-run `/verify`.

## Rules

1. Unit tests first.
2. For visual changes, take screenshots and read them.
3. Report actual values, not just pass/fail.
4. Prerequisites are hard gates.
5. Don't fix during verify; report and root-cause separately.
6. Screenshots and captures go under `$TEMP`, never the repo tree.
