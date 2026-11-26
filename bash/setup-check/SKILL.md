---
name: setup-check
description: Check this machine for what developer-os needs (python3, rg, jq, gh login, git, vault path, auto memory, Claude Code) and give the fix for each gap. Read-only. Use for "check my developer-os setup", "why do the hooks not run".
license: MIT
compatibility: "Claude Code"
---

# Setup check

Read-only. This skill runs one script that reads versions and two user-level files, then reports. It installs nothing, edits no setting and writes no file. The one outside call is `gh auth status`, which asks GitHub whether the stored login still works.

## 1. Run the check

```bash
python3 -I "${CLAUDE_PLUGIN_ROOT}/skills/setup-check/check.py"
```

If that path still reads as a literal `${...}`, the script is `check.py` in this skill's base directory; use that absolute path. If `python3` itself is not found, that is the answer: report the `python3` fix below and stop.

The script prints one line per check, `<status> <name>: <detail>`, with the status `ok`, `missing` or `warn`, and always exits 0. It reads the vault path from the user level only (the `brain_vault` option in the user-level `settings.json`, else the `Brain vault:` line in the user-level `CLAUDE.md`), never from a project file.

## 2. Report

Show every line as printed, then one fix per line that is not `ok`. Name the install command for the user's platform (Homebrew on macOS, the distribution's package manager on Linux, winget on Windows) as text for the user to run; do not run it.

| Line | What breaks | Fix |
|---|---|---|
| `python3` missing or older than 3.8 | Every hook except the core rules: guard, notices, state card, patterns, repeat-failure, wrap-up nudge. They fail open, so nothing is reported at the time. This is the usual answer to "why do the hooks not run". | Install Python 3.8 or later so that `python3` is on `PATH`, then restart Claude Code. |
| `rg` missing | The skills that search with ripgrep: skill-usage, project-baseline, project-init and the brain skills. | Install ripgrep. |
| `jq` missing | brain-setup and brain-import-memory, which edit `settings.json` through `jq`, and pr-cycle. | Install jq. |
| `gh` missing | The pull-request skills (pr-cycle, fix-pr) and the open-PR check in session-retro. | Install the GitHub CLI. |
| `gh auth` warn | The same skills: `gh` is there but has no working login. | The user runs `gh auth login` in their own terminal. |
| `git` older than 2.38 | A conflict preview with `git merge-tree --write-tree`, which older git lacks. | Upgrade git. |
| `vault` warn, not configured | The brain skills and the upkeep notices have no vault. | Ask for brain-setup. Optional: the rest of the plugin works without a vault. |
| `vault` missing | The configured path is not a readable directory (moved, unmounted or mistyped). | Correct the path with brain-setup, or mount or restore the directory. |
| `autoMemoryEnabled` warn | Claude Code's auto memory keeps a second, unreviewed store beside the vault. | brain-setup offers `"autoMemoryEnabled": false` in the user-level `settings.json`; with existing memory files, brain-import-memory first. A recommendation, not an error. |
| `claude` missing | The `claude` command is not on `PATH`, so parallel-lanes cannot start a lane. | Add the Claude Code CLI to `PATH`. |

If every line is `ok` and the user asked why a hook does not run, say what the script cannot see: whether the plugin is enabled (`/plugin`), which hooks are registered (`/hooks`), and that a `DEVELOPER_OS_<HOOK>=off` variable turns one hook off.

End with the count of `missing` and `warn` lines and "Nothing was changed."

## Stop point

After the report. Every fix is the user's to run or to ask for; do not start brain-setup or an install on your own.

## Never

- Never install, upgrade or configure anything, and never write a file or a setting.
- Never read the vault path from a project `CLAUDE.md`, a project `settings.json` or an environment variable.
- Never print file contents from the vault or from `settings.json`; the script's lines are the whole output.
