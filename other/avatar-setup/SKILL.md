---
name: avatar-setup
description: Aang choosing which bender takes which fight. Configures which model each Team Avatar character runs on, the default reasoning effort, and whether the SessionStart hook routes work into avatar-mode. Use for /avatar-setup, "setup team avatar", "configure team avatar models", changing a character's model, or turning the session hook on or off.
---

# Avatar setup

Before the first battle, the Avatar decides who stands where. Each character runs on the model that fits the discipline, and the user decides what models they have. This skill writes that choice down once, in one sheet, so every dispatch reads the same answer.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents, including its note for this skill.

## Where the sheet lives

| Runtime | Sheet | How it loads |
|---------|-------|--------------|
| Claude Code | `${CLAUDE_CONFIG_DIR:-~/.claude}/team-avatar-models.md` | `avatar-mode` prints it with `show-sheet.sh claude` before the first dispatch. The SessionStart hook reads its `session hook` line. |
| Codex | `${CODEX_HOME:-~/.codex}/team-avatar-models.md` | `avatar-mode` prints it with `show-sheet.sh codex` before the first dispatch. The SessionStart hook reads its `session hook` line. |

The scripts live in [scripts/](scripts/), and every one runs with plain `sh` and POSIX `awk`.

- `read-sheet.sh <sheet>` decodes the sheet once (UTF-16LE from PowerShell 5.1, a UTF-8 BOM, CRLF line endings) and prints plain lines. Every other script and the hook read through it.
- `check-sheet.sh <sheet>` prints `sheet ok`, or `sheet invalid: <problems>` and exits 1.
- `show-sheet.sh <claude|codex> [sheet]` prints every line that applies on that runtime, each marked `(sheet)` or `(default)`. With no sheet it prints the defaults.
- `sheet.awk` holds the line list, the defaults, and the checks. Change a default there and nowhere else.

## Steps

### 1. Detect the models you can use

List the model names the `Agent` tool's `model` parameter accepts in this session. That is the dependable source. On Claude Code they are the family names `opus`, `fable`, `sonnet`, and `haiku`, each running that family's current model, and a full model ID is rejected. On Codex, use the Codex models you have configured (see the codex.md note). Ask the user to confirm the list or paste more names. Never write a model name you have not confirmed is available. `inherit` is always valid. It runs the line on the parent session's model, which a dispatch expresses by omitting `model`.

### 2. Load the current state

Print the current lines with `sh <this skill>/scripts/show-sheet.sh claude` (or `codex`). Lines marked `(sheet)` are the user's current choices. Lines marked `(default)` are the defaults below. Then run `check-sheet.sh` on the sheet if one exists, and note each problem it prints.

An older sheet may hold a line this skill no longer writes, or a full model ID that starts with `claude-`, which the `Agent` tool rejects. Drop the unknown line. Replace the full ID with its family name, the word after `claude-`.

### 3. Map and confirm

Show every line with its current value. Mark any model name not in the detected set as needing a choice, and list each line step 2 dropped or rewrote. Ask whether to accept as-is or change specific lines, offering the detected models plus `inherit`. Prefer `AskUserQuestion` over free text.

- `panel` is a list. One runner goes out per entry, so the list length sets the count, and it needs at least two entries. Pick models from different families where you can, because a panel's signal comes from diversity.
- `strongest` takes the hardest changes and the strongest judgment calls. Point it at your best model.
- `toph review` is Toph reviewing a diff or a design. `toph` is Toph reading and investigating.
- `suki` runs squad workers and every verification pass, so do not set it weaker than the work it checks.

Then ask for the default reasoning effort, the `default effort` line. It is `session`, which keeps the parent session's effort, or one of `low`, `medium`, `high`, `xhigh`, `max`. Every value without a suffix runs at it. Then ask whether any line should run at another level. A value may carry one after its model, as in `sokka: opus @high`. Panel entries take their own, as in `panel: opus @xhigh, fable @max`. On Claude Code the level goes out as the `Agent` tool's `effort` parameter. On Codex it goes out as `spawn_agent`'s `reasoning_effort`.

### 4. Choose whether the session hook routes work

On Claude Code and Codex, the plugin's SessionStart hook injects a short routing context on startup, resume, clear, and compact. It sends nontrivial work into `avatar-mode`. Codex asks the user to trust plugin hooks through `/hooks` before running them. Ask whether to keep the hook. The default is on. The answer is the `session hook` line, `on` or `off`. With no sheet or no line, the hook injects.

### 5. Validate

Every model name written must be in the detected set. `inherit` always passes. Check the name without its `@<level>` suffix, and the level against the levels above. On Codex, the levels are the `reasoning_effort` values your Codex models accept. If a chosen name or level is not available, stop and ask again.

### 6. Write the sheet

Write the whole file with the shape below, so a rerun stays idempotent. Keep every line, in this order, with the user's values. The defaults are shown.

```markdown
# Team Avatar models

Which model each Team Avatar character runs on. avatar-mode reads this sheet before it dispatches, and a line it lacks keeps its default. `inherit` runs on the parent session's model. A value may carry a reasoning effort, as in `opus @high` (levels: low, medium, high, xhigh, max). `panel` is a list, one runner per entry. `default effort` sets the level for a value without one, and `session` keeps the parent session's effort. `session hook: off` stops the SessionStart hook from routing work into avatar-mode.

aang: inherit
sokka: opus
toph: sonnet
toph review: opus
katara: opus
zuko: opus
iroh: opus
appa: sonnet
momo: haiku
suki: opus
strongest: fable
panel: opus, fable, sonnet, haiku
default effort: session
session hook: on
```

Then run `sh <this skill>/scripts/check-sheet.sh <sheet>`. It must print `sheet ok`. Fix and rewrite on any problem.

### 7. Wire it in (optional)

`avatar-mode` reads the sheet itself, so nothing else is required. A user who wants the lines in every session's context can still add them.

- On Claude Code, append `@<config>/team-avatar-models.md` to `<config>/CLAUDE.md`, with `<config>` written as the resolved path (`$CLAUDE_CONFIG_DIR`, or `~/.claude`). For project scope, add it to the project's `CLAUDE.md` instead.
- On Codex, paste the model lines and the `default effort` line into `<codex-home>/AGENTS.md`, since Codex has no `@` include. Leave out the `session hook` line, because the hook reads it straight from the sheet.

### 8. Confirm

Tell the user where the sheet was written, the `check-sheet.sh` result, how `avatar-mode` reads it, and whether the hook is on. Rerunning this skill updates the sheet.

### 9. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a project `verify` or `verify-*` skill, or an existing harness). If it has none, offer once. "Want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with `vital-signs`." On yes, run `vital-signs`. On no, move on without pushing.
