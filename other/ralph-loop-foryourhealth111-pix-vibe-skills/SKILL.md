---
name: ralph-loop
description: Codex-compatible Ralph loop runner with dual engines (compat local state loop + optional open-ralph-wiggum backend).
---

# ralph-loop

This is a Codex-oriented `ralph-loop` command with two execution engines.

## Engine model

- Keeps the same command name: `ralph-loop`.
- Keeps the same default state file format: `.claude/ralph-loop.local.md`.
- Default `compat` engine keeps local-state semantics and manual `--next`.
- Optional `open` engine delegates to external `open-ralph-wiggum` CLI for auto-iteration.

## Script

- Script path: `scripts/ralph-loop.ps1`

## Usage

```powershell
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$script = Join-Path $codexHome 'skills/ralph-loop/scripts/ralph-loop.ps1'

# Start a local compat loop
powershell -ExecutionPolicy Bypass -File $script Build a todo API --max-iterations 20 --completion-promise DONE

# Move to the next iteration manually
powershell -ExecutionPolicy Bypass -File $script --next

# Show current loop state
powershell -ExecutionPolicy Bypass -File $script --status

# Force restart with a new prompt
powershell -ExecutionPolicy Bypass -File $script New prompt --max-iterations 10 --force

# Use open-ralph-wiggum backend (auto loop, defaults to --agent codex and --no-commit)
powershell -ExecutionPolicy Bypass -File $script --engine open Build a todo API --max-iterations 20 --completion-promise DONE
```

## Vibe compatibility

- Safe in `/vibe` routed sessions as a direct execution tool.
- Does not force multi-agent orchestration.
- Keeps command names stable for unified memory and invocation.
- `open` engine remains mutually exclusive with active XL team orchestration.

## Notes

- Compat mode: if `max_iterations` is reached, the local state file is removed automatically.
- Compat mode: completion promises are tracked in local state.
- Open mode: `--next`, `--force`, `--state-file`, `--stop` are not available (managed by external `ralph` CLI semantics).

