---
version: "2.0.2"
name: Bat
description: "Log and search local text entries from the command line. Use when adding quick notes, searching past entries, or exporting a simple activity log."
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags: ["notes", "log", "search", "cli", "productivity"]
---

# Bat

A lightweight, multi-purpose command-line utility for logging, searching, and managing text entries. All data remains on disk in plain-text log files — no cloud, no dependencies.

## Commands

| Command | Description |
|---------|-------------|
| `run <arg>` | Execute the main function — prints the argument and logs the action. |
| `config` | Show the config file path (`$DATA_DIR/config.json`) and log the action. |
| `status` | Print current status ("ready") and log the check. |
| `init` | Initialize the data directory — confirms creation at `$DATA_DIR`. |
| `list` | Print all entries from the main data log (`data.log`). Shows "(empty)" if no entries exist. |
| `add <text>` | Append a timestamped entry to the log. Format: `YYYY-MM-DD <text>`. |
| `remove <text>` | Mark an entry as removed and log the removal action. |
| `search <term>` | Case-insensitive search through all logged entries. Shows "Not found" if no matches. |
| `export` | Output the full data log to stdout. Pipe to a file for backups: `bat export > backup.txt`. |
| `info` | Show version number and data directory path. |
| `help` | Show full usage information with all available commands. |
| `version` | Print version number (`v2.0.2`). |

## Data Storage

All data is stored in `~/.local/share/bat/` by default:

- `data.log` — Main log file (one entry per line, date-prefixed via `add`)
- `history.log` — Command history with timestamps (auto-maintained by every command)
- `config.json` — Configuration file path (shown by `bat config`)

Set the `BAT_DIR` environment variable to change the storage location. Alternatively, `XDG_DATA_HOME` is respected if `BAT_DIR` is not set.

## Requirements

- Bash 4+ (uses `local` variables, `set -euo pipefail`)
- Standard Unix utilities (`grep`, `date`, `wc`, `cat`)
- No external dependencies or API keys required

## When to Use

1. **Quick note-taking from the terminal** — Use `bat add` to jot down thoughts, meeting notes, or TODO items without leaving the shell.
2. **Maintaining a running activity log** — Every `add` creates a dated entry, building a chronological record of activities over time.
3. **Searching past entries by keyword** — Use `bat search <term>` to find specific entries with case-insensitive matching.
4. **Exporting and backing up notes** — Use `bat export > backup.txt` to dump all entries for backup, sharing, or migration.
5. **General-purpose CLI data management** — Use `run`, `init`, `config`, and `status` as building blocks for scripted workflows and automation pipelines.

## Examples

```bash
# Add a note about a meeting
bat add "Met with client about Q2 targets"

# Add another entry
bat add "Sent follow-up email to vendor"

# List all logged entries
bat list

# Search for entries mentioning "client"
bat search "client"

# Export log to a backup file
bat export > ~/bat-backup.txt

# Check version and data directory
bat info

# Initialize (or verify) the data directory
bat init

# Check operational status
bat status

# Show config file path
bat config
```

## Output

All commands print results to stdout and log actions to `history.log`. The `add` command confirms each save with the added text. The `list` and `export` commands output raw log content suitable for piping and redirection.

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
