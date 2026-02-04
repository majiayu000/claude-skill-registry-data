---
name: visidata
description: VisiData is a terminal spreadsheet for exploring data. Use it instead of one-off jq/SQL queries. Check --help first, then use with tmux for programmatic control.
allowed-tools: Bash, Read
---

# VisiData - Terminal Spreadsheet

VisiData is like Excel in your terminal. Use it to explore data interactively instead of writing one-off jq or SQL queries.

## Installation

```bash
uv tool install visidata

# Verify
vd --version
```

## Start Here: Use the Help

**ALWAYS check the built-in help first:**

```bash
# Comprehensive reference
vd --help | less

# Inside VisiData:
g^H         # View full man page
z^H         # Commands for current sheet
Alt+H       # Interactive help menu
```

The help is comprehensive and always current. Use it.

## Basic Usage

### Interactive (for humans)

```bash
vd data.csv              # Open and explore
vd data.json             # Works with JSON
vd data.xlsx             # Works with Excel
vd file1.csv file2.csv   # Open multiple files
```

**Common operations:**
- `hjkl` or arrows to navigate
- `G` / `gg` - bottom / top
- `/` - search
- `[` / `]` - sort ascending/descending
- `Shift+F` - frequency table (like GROUP BY)
- `Shift+I` - statistics summary
- `q` - back/quit
- `gq` - quit all

### Batch (for scripts)

```bash
# Convert without interaction
vd -b input.csv -o output.json
vd -b data.xlsx -o data.csv
```

## Programmatic Use: VisiData + tmux

**For programmatic control, always use tmux** (see tmux skill for details):

```bash
SOCKET="/tmp/claude-tmux-sockets/claude.sock"
SESSION="vd"
PANE="vd:1.1"

mkdir -p /tmp/claude-tmux-sockets

# Start VisiData
tmux -S "$SOCKET" new -d -s "$SESSION" "vd data.csv"
sleep 2

# Send commands (go to bottom, find column, widen)
tmux -S "$SOCKET" send-keys -t "$PANE" "G"
sleep 1
tmux -S "$SOCKET" send-keys -t "$PANE" "c"
tmux -S "$SOCKET" send-keys -t "$PANE" -l "column_name"
tmux -S "$SOCKET" send-keys -t "$PANE" Enter
sleep 1
tmux -S "$SOCKET" send-keys -t "$PANE" "_"
sleep 1

# Capture what you see
tmux -S "$SOCKET" capture-pane -p -J -t "$PANE" -S -30

# Clean up
tmux -S "$SOCKET" send-keys -t "$PANE" "gq"
tmux -S "$SOCKET" kill-session -t "$SESSION"
```

## When to Use VisiData

**Instead of jq one-liners:**
```bash
# ❌ Complex jq that's hard to get right
jq '.[] | select(.status == "active") | {name, email}' data.json

# ✅ Use VisiData - see your data, filter interactively
vd data.json
# Navigate, filter, select columns visually
# Save result: ^S output.csv
```

**Instead of ad-hoc SQL:**
```bash
# ❌ Writing SQL for quick data check
sqlite3 db.sqlite "SELECT category, COUNT(*) FROM items GROUP BY category"

# ✅ Use VisiData for exploration
vd db.sqlite
# Navigate to table, Shift+F for frequency, see results visually
```

**For debugging data issues:**
```bash
# See the actual data, not just summaries
vd large_file.jsonl
# Navigate to problem rows, inspect actual values
```

## Integration with JN

```bash
# Export from JN for visual inspection
jn cat data.json | jn put /tmp/inspect.csv
vd /tmp/inspect.csv

# Or use jn vd command
jn vd data.json
```

## Key Insight

**VisiData lets you SEE your data while working with it.**

Instead of guessing what jq filter to write, open it in VisiData and explore. Instead of writing GROUP BY queries, use Shift+F to see frequency distributions.

It's faster for exploration. Use `vd --help` to learn the commands, then explore your data visually.

## Common Issues

**⚠️ Too many 'q' presses quit entirely:**
- `q` - go back one sheet
- `qq` or `gq` - quit VisiData
- Be careful when sending 'q' via tmux!

**Running out of memory:**
```bash
# For huge files, use limit
vd --max-rows 10000 huge.csv

# Or preview with JN first
jn head -n 1000 huge.csv | jn put /tmp/preview.csv
vd /tmp/preview.csv
```

## That's It

1. Install with `uv tool install visidata`
2. Check `vd --help` for commands
3. Use it instead of guessing jq/SQL queries
4. Use with tmux for programmatic control

VisiData is for exploration. Let the data show you what it contains.
