---
name: header-footer
description: Configures the reply header (a line such as "🕐 14:57 · main" at the top of Claude's first reply of each turn) and the footer (Claude Code's status line - session tokens, plan limits, clock, branch, model, context) from one config file - turn each one on or off, pick fields and their order, the time and date format, icon and separator, and diagnose why something does not show. Use when the user asks to change, turn on or off, or debug the header or the footer/status line, for example "put the branch in the header", "remove the clock from the footer", "show seconds", "why is the time not showing", "liga/desliga o header", "tira o relógio do footer", "põe a branch no header", "muda o formato da hora". Triggers - /header-footer or /header-footer:header-footer.
---

# header-footer (reply header and status-line footer)

Two pieces, one config file (`header-footer.json` in the Claude config directory, `~/.claude` unless `CLAUDE_CONFIG_DIR` is set):

- **Header**: a `UserPromptSubmit` hook renders a line (time, date, weekday, folder, repository, branch) and injects it as `<reply-header>...</reply-header>` together with the instruction to copy it. The plugin registers this hook by itself (`hooks/hooks.json`).
- **Footer**: Claude Code's status line. Its `state` field shows `● running 3m` while Claude works, `◐ waiting` while it waits for the user and `○ idle` when it stops; the plugin's hooks on `UserPromptSubmit`, `PostToolUse`, `Notification`, `PermissionRequest` and `Stop` feed it. A plugin cannot set `statusLine`, so `on footer` copies the script to a stable path inside the Claude config directory and points `statusLine` there.

Reply to the user in the user's language. The script's messages are Portuguese: explain them in the user's language.

## When the header line is in your context

If a `<reply-header>` tag is in your context, start your first reply of the turn with its text, verbatim, on a line of its own. Never estimate, complete or reformat it. If the tag is absent, write no header line and never invent one.

## Flow

### 0. Locate the script

The script ships with this skill: `${CLAUDE_SKILL_DIR}/scripts/header_footer.py`. Run it directly, always with `python3 -I`.

```bash
test -f "${CLAUDE_SKILL_DIR}/scripts/header_footer.py" && echo OK || echo FALTA
```

`FALTA` means "missing".

If `${CLAUDE_SKILL_DIR}` appears unexpanded, use the path shown as "Base directory for this skill" when the skill was loaded. Write that path out in full in every command.

### 1. Always start with status

```bash
python3 -I "${CLAUDE_SKILL_DIR}/scripts/header_footer.py" status
```

It prints the config, how each piece is wired, a preview of both, and a diagnosis. Exit code `1` means it found problems; `2` means a usage or config error.

### 2. Translate the request into one command

| The user wants | Command |
| --- | --- |
| header off / on | `off header` / `on header` (takes effect on the next prompt) |
| footer on / off | `on footer` / `off footer` (edits `settings.json` after a backup) |
| branch in the header | `header-fields time,branch` |
| seconds in the time | `header-format "%H:%M:%S"` |
| date as 16/10 | `header-format "%d/%m" --date` and add `date` to the header fields |
| remove the clock from the footer | `footer-fields` with the current list minus `clock` |
| show whether Claude is working | put `state` in `footer-fields` (it is in the default list) |
| another icon / separator | `header-icon "⏱"` / `separator header " \| "` |
| what fields exist | `fields` |
| see both now | `preview` |

Field lists **replace** the current list: read the current fields from `status` first and send the whole new list.

If `on footer` answers that another `statusLine` already exists, show the user which command it is and ask. Re-run with `--replace` only after the user agrees. The backup of `settings.json` is kept next to it as `settings.json.bak-header-footer-<timestamp>`.

### 3. Show the result

Show the preview line the script printed. Do not describe from memory how the header or the footer looks.

## Installs without the plugin system

If the skill was copied with `install.sh`, the plugin's `hooks.json` is not active: the header and the `state` field have no hooks. Run `wire-hooks` to register them in `settings.json`, and `unwire-hooks` to remove them. On Windows, recommend `wire-hooks` even with the plugin installed: the plugin's hooks call `python3`, which Git Bash and PowerShell usually do not have, while `wire-hooks` writes the absolute interpreter path.

## Rules

- Change `settings.json` only through the script: it backs the file up and touches only its own entries.
- `status` warns about an older header hook still in `settings.json` (a `reply-header.py` or `inject-timestamp.sh` entry): with the plugin installed, that would print two headers. Tell the user and remove the old entry only with the user's approval.
- After a plugin update, `status` may report that the stable copy is older than the plugin: re-run `on footer` (or `wire-hooks`) to refresh it. The same fix applies when `status` reports that the python written into `settings.json` no longer exists.
- When `status` reports that the header is on but no hook runs it, check whether the plugin is enabled (it may be enabled only in a project `settings.json`, which `status` does not read); otherwise offer `wire-hooks`.
- The `gsd` footer field shows the GSD status line when GSD is installed (`hooks/gsd-statusline.js` in the Claude config directory, plus `node`). Without GSD it renders nothing.
