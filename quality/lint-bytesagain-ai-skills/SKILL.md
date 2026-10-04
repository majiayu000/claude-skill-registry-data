---
name: lint
version: "2.0.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [lint, tool, utility]
description: "Check code syntax, enforce style, and suggest auto-fixes with CI integration. Use when linting PRs, enforcing code style, detecting errors before merge."
---

# Lint

Lint is a developer-focused toolkit for recording and tracking code quality operations from the terminal. It provides 13 core action commands for managing checks, validations, formatting, linting, code generation, conversions, templates, diffs, previews, fixes, reports, and explanations — all with timestamped local logging for full traceability. Additional utility commands let you view statistics, export data, search history, and monitor health status.

## Commands

### Core Action Commands

Each action command works in two modes: run without arguments to view the 20 most recent entries, or pass input text to record a new timestamped entry.

| Command | Description |
|---------|-------------|
| `lint check <input>` | Record a syntax/code check entry |
| `lint validate <input>` | Record a validation result |
| `lint generate <input>` | Record a code generation action |
| `lint format <input>` | Record a formatting operation |
| `lint lint <input>` | Record a linting pass |
| `lint explain <input>` | Record an explanation or annotation |
| `lint convert <input>` | Record a conversion operation |
| `lint template <input>` | Record a template action |
| `lint diff <input>` | Record a diff comparison |
| `lint preview <input>` | Record a preview action |
| `lint fix <input>` | Record an auto-fix action |
| `lint report <input>` | Record a report generation |

### Utility Commands

| Command | Description |
|---------|-------------|
| `lint stats` | Show summary statistics — entry counts per category, total entries, data size, and earliest activity timestamp |
| `lint export <fmt>` | Export all data to JSON, CSV, or TXT format. Output file saved to `~/.local/share/lint/export.<fmt>` |
| `lint search <term>` | Full-text search across all log files (case-insensitive) |
| `lint recent` | Show the 20 most recent entries from the history log |
| `lint status` | Health check — version, data directory, total entries, disk usage, last activity |
| `lint help` | Show help with all available commands |
| `lint version` | Print version string (`lint v2.0.0`) |

## Data Storage

All data is stored locally in `~/.local/share/lint/`. Each action command writes to its own log file (e.g., `check.log`, `validate.log`, `fix.log`). A unified `history.log` records every action with timestamps. No external services, databases, or network connections are used.

**Directory structure:**
```
~/.local/share/lint/
├── check.log        # Check entries
├── validate.log     # Validation entries
├── generate.log     # Generation entries
├── format.log       # Formatting entries
├── lint.log         # Lint pass entries
├── explain.log      # Explanation entries
├── convert.log      # Conversion entries
├── template.log     # Template entries
├── diff.log         # Diff entries
├── preview.log      # Preview entries
├── fix.log          # Fix entries
├── report.log       # Report entries
├── history.log      # Unified activity log
└── export.*         # Export output files
```

## Requirements

- Bash (with `set -euo pipefail`)
- Standard Unix utilities: `date`, `wc`, `du`, `head`, `tail`, `grep`, `basename`, `cut`
- No external dependencies or API keys required

## When to Use

1. **Tracking linting sessions** — Record which files you linted, what issues you found, and what fixes you applied, all with timestamps for audit trails.
2. **Code review workflows** — Log check and validate results during PR reviews so you can refer back to what was inspected and when.
3. **Template and diff management** — Keep a running record of template operations and diff comparisons across project iterations.
4. **Exporting quality reports** — Use `lint export json` to generate machine-readable reports of all recorded lint activity for CI dashboards or team reviews.
5. **Searching past actions** — Quickly find previous lint results, fixes, or explanations with `lint search <term>` across all categories.

## Examples

```bash
# Record a check on a Python file
lint check "src/main.py — 3 unused imports found"

# Record a fix applied
lint fix "Removed unused imports in src/main.py"

# View recent formatting actions
lint format

# Search for all entries mentioning "import"
lint search import

# Export everything to JSON
lint export json

# View overall statistics
lint stats

# Health check
lint status
```

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
