---
name: agy-delegate
description: >
  Delegate work to the local `agy` CLI (print mode) — typically Gemini or other
  models listed by `agy models`. Use from Cursor when you need a one-shot or
  follow-up agy turn with a self-contained handoff, optional `--add-dir`
  workspace, and parseable stdout. Triggers: agy, agy -p, --model gemini,
  Gemini via agy, delegate to agy, agy print mode, agy-delegate. NEVER for
  LibrAgent HTTP Session API (that is `libr-delegate`). NEVER invent MCP tool
  names for agy. NEVER swap `--model` away from this skill’s default unless the
  user explicitly names a model.
---

# Agy Delegate (Cursor → `agy` CLI)

Spawn and steer **agy** turns from Cursor via the local CLI. `agy` must be
installed and on `PATH` (typically `~/.local/bin/agy`).

## vs `libr-delegate`

| Caller need | Skill |
| --- | --- |
| Cursor → **agy** (Gemini/Claude/etc. CLI) | **This skill** |
| Cursor → **LibrAgent** HTTP `/api/sessions` | `libr-delegate` |

## Preconditions

```bash
# Bash (Linux / macOS)
command -v agy >/dev/null || { echo "agy not on PATH"; exit 1; }
```

```powershell
# PowerShell (Windows)
if (-not (Get-Command agy -ErrorAction SilentlyContinue)) { Write-Error "agy not on PATH"; exit 1 }
```

Only run `agy models` when the user asked for a non-default model, or the
default id failed as unknown/stale.

## Workflow

1. Write a **self-contained** handoff (agy does **not** see this Cursor chat)
2. Use this skill’s **default** `--model` (below). Do **not** pick a different
   model for “harder” work, cost, or preference
3. Run print mode (`-p` / `--print`) from the relevant cwd or pass `--add-dir`
4. Read stdout as the result; on failure check exit code and stderr
5. Follow-ups: new `-p` with fuller context, or `--conversation <id>` /
   `--continue` when resuming the same thread — **same model as the first turn**
6. Optional: `--output-format json` when you need `status` / `response` fields

Recipes: `references/cli.md`. Handoff / isolation: `references/handoff.md`.
Optional wrappers: `scripts/run.sh` (Bash) or `scripts/run.ps1` (PowerShell).

## Default invoke (unattended)

**Default model (do not change):** `gemini-3.8-flash-high`

### Linux / macOS (Bash)

```bash
agy -p "$TASK" \
  --model gemini-3.8-flash-high \
  --dangerously-skip-permissions \
  --print-timeout 300s \
  --add-dir "$WORKSPACE_ABS"
```

```bash
# Using bundled bash wrapper
./scripts/run.sh --dir "$WORKSPACE_ABS" -- "$TASK"
./scripts/run.sh --json --dir "$WORKSPACE_ABS" -- "$TASK"
```

### Windows (PowerShell)

> [!IMPORTANT]
> In PowerShell, unquoted multiline variables split across spaces. Always quote `"$TASK"` or pass via Here-String (`@' ... '@`).

```powershell
$TASK = @'
Goal: ...
Scope: ...
'@

& agy -p "$TASK" `
  --model gemini-3.8-flash-high `
  --dangerously-skip-permissions `
  --print-timeout 300s `
  --add-dir "$WORKSPACE_ABS"
```

```powershell
# Using bundled PowerShell wrapper (recommended on Windows)
& .agents/skills/agy-delegate/scripts/run.ps1 -Dir "$WORKSPACE_ABS" -Task "$TASK"
& .agents/skills/agy-delegate/scripts/run.ps1 -Dir "$WORKSPACE_ABS" -Json -Task "$TASK"
```

- Omit `--dangerously-skip-permissions` / `-NoSkipPerms` when the user must approve tool use
- Raise timeout for long coding/research turns; `0` waits until completion
- Repeat `--add-dir` / `-Dir` for extra roots
- Use `--output-format json` / `-Json` to parse `status` (`SUCCESS` / …) and `response`

## Model selection (strict)

| Rule | Action |
| --- | --- |
| Normal delegate | Always `--model gemini-3.8-flash-high` (or omit `--model` when using `scripts/run.sh` / `AGY_MODEL` default) |
| User names a model | Use **exactly** that id (verify with `agy models` if it fails) |
| Agent judgment (“this needs Pro/Claude”) | **Forbidden** — keep the default |

Do **not** hardcode alternate model names into invocations. Do **not** “upgrade”
to Pro/Opus/Claude unless the user asked. If `agy` rejects the default id as
stale, list `agy models` and pick the closest **flash-high** equivalent — still
do not silently jump to Pro.

## Isolation (critical)

The agy session is not a clone of this Cursor chat:

- Default cwd is whatever shell cwd you launch with — set it, or pass absolute
  `--add-dir`
- Put objective, scope, paths, and output format in the `-p` prompt
- Require deliverables in **stdout** (final assistant text / JSON `response`)
- Do not assume Cursor files, notes, or skills are visible inside agy

## Anti-patterns

- Calling nonexistent MCP tools (`agy__*`, `spawnAgy`, …)
- Vague prompts that rely on Cursor thread context
- Treating non-zero exit or JSON `status` ≠ `SUCCESS` as success
- Using this skill for LibrAgent Session API (use `libr-delegate`)
- Interactive-only flags (`-i`) for automation — prefer `-p`
- Changing `--model` without an explicit user request (including Pro/Claude “for quality”)
- Unquoted variables in PowerShell (`agy -p $TASK` splits words into CLI flags; always quote or use Here-Strings)
- Bash syntax in PowerShell (`&&`, `\`, `./scripts/run.sh` — use `;`, `` ` ``, or `run.ps1`)
- Script sprawl: fabricating ad-hoc .bat/.py/.js wrappers instead of using direct invocations or the provided `run.sh`/`run.ps1`
