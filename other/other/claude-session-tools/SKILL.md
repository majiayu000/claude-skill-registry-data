---
name: claude-session-tools
description: Explore, search, analyze, and recover files and conversations from Claude Code session histories stored in ~/.claude/projects/ using the aise command-line tool.
version: "0.9.0"

# VISIBILITY & TRIGGERING
user-invocable: true
disable-model-invocation: false

# EXECUTION CONTEXT - Tools this skill can use
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# Claude Session Tools

Search, analyze, and recover anything from Claude Code session histories. Use when the user needs to find past work, understand what Claude did in a session, recover a file, search conversation history, or detect patterns in how Claude is being used.

**Invoke with:** `/ar:claude-session-tools` or natural language like "find that file from last week's session", "what did Claude do in session ab841016", "search my Claude sessions for authentication"

**Tool:** `aise` — run `aise --help` to see all commands

---

## Goal → Command Quick Reference

| Goal | Command |
|------|---------|
| Find all sessions | `aise list` |
| Find sessions for a project | `aise list --project myproject` |
| Read all messages from a session | `aise messages get SESSION_ID` |
| Search text across all sessions | `aise messages search "query"` |
| See what tools Claude used | `aise messages analyze SESSION_ID` |
| See chronological session events | `aise messages timeline SESSION_ID` |
| Find a file Claude wrote or edited | `aise files search --pattern "name.py"` |
| See version history of a file | `aise files history filename.py` |
| Recover a file to stdout | `aise files extract filename.py` |
| Find all Write/Edit calls to a file | `aise tools search Write "filename"` |
| Check if edits appear in current file | `aise files cross-ref ./path/to/file` |
| Find user corrections to Claude | `aise messages corrections` |
| Count planning command usage | `aise messages planning` |
| Get clipboard content from a session | `aise messages extract SESSION_ID pbcopy` |
| Export session to markdown | `aise export session SESSION_ID` |
| Export last N days of sessions | `aise export recent 7 --output week.md` |
| Search files + messages together | `aise search --pattern "*.py" --query "error"` |
| Find specific tool invocations | `aise tools search Bash "git commit"` |

---

## Goal-Oriented Sequences

### "Find and recover a file from a past session"

```bash
# 1. Find which sessions touched the file
aise files search --pattern "filename.py"

# 2. See version history (how many times it was edited, which sessions)
aise files history filename.py

# 3. Preview a specific version
aise files extract filename.py --version 3

# 4. Recover latest version to disk
aise files extract filename.py > filename.py
```

---

### "Understand what happened in session X"

```bash
# 1. Get session list to find the right ID
aise list --project myproject

# 2. Read the conversation
aise messages get ab841016

# 3. See statistics: tool counts, files touched
aise messages analyze ab841016

# 4. See chronological event timeline
aise messages timeline ab841016
```

---

### "Search for when something was discussed"

```bash
# Search all sessions for a phrase
aise messages search "authentication bug"

# Search only user messages
aise messages search "authentication" --type user

# Search with surrounding context
aise messages search "authentication" --context 3

# Search across files AND messages
aise search --query "authentication" --pattern "*.py"
```

---

### "Verify that Claude's edits are in the current file"

```bash
# Show each Edit/Write call Claude made to the file
# and mark ✓ (found in current file) or ✗ (missing)
aise files cross-ref ./path/to/file.md

# Limit to one session
aise files cross-ref ./cli.py --session ab841016

# JSON output to process programmatically
aise files cross-ref ./engine.py --format json
```

---

### "Find a specific tool use (Bash, Edit, Write, Read…)"

```bash
# All Write calls across all sessions
aise tools search Write

# Bash calls containing a pattern
aise tools search Bash "git commit"

# Edit calls targeting a file
aise tools search Edit "cli.py"

# Via root search with --tool flag
aise search --tool Read --query "engine.py"
```

---

### "Export sessions for documentation or review"

```bash
# Export one session to stdout, redirect to file
aise export session ab841016 > session.md

# Export to an explicit file
aise export session ab841016 --output notes/session.md

# Preview without writing
aise export session ab841016 --dry-run

# Export last 7 days of sessions
aise export recent 7 --output weekly.md

# Filtered by project
aise export recent 14 --project myproject --output sprint.md
```

---

### "Understand patterns in Claude usage"

```bash
# Find messages where you corrected Claude
# Categories: regression, skip_step, misunderstanding, incomplete, other
aise messages corrections

# Filter by project or date
aise messages corrections --project myproject --after 2026-01-01

# Count planning command usage (/ar:plannew, /ar:planrefine, etc.)
aise messages planning

# Get clipboard content Claude prepared in a session
aise messages extract ab841016 pbcopy
```

---

## All Commands Reference

### Session Discovery
```bash
aise list                                    # all sessions, newest first
aise list --project myproject                # filter by project
aise list --after 2026-01-01                 # sessions since date
aise list --before 2026-02-01                # sessions before date
aise list --limit 20                         # cap results
aise list --format json                      # machine-readable
```

### Message Search & Reading
```bash
aise messages search "query"                 # search all sessions
aise messages search "query" --type user     # user messages only
aise messages search "query" --type assistant
aise messages search "query" --context 3     # N messages before/after
aise messages search "query" --limit 20
aise messages search "query" --format json
aise messages get SESSION_ID                 # read full session
aise messages get SESSION_ID --type user
aise messages get SESSION_ID --limit 10
```

### File Recovery
```bash
aise files search                            # all files Claude touched
aise files search --pattern "*.py"           # by glob pattern
aise files search --include-extensions py ts # by extension
aise files search --min-edits 5              # heavily-edited files
aise files search --include-sessions ID      # files in one session
aise files history filename.py               # version history
aise files extract filename.py               # latest version → stdout
aise files extract filename.py --version 2   # specific version
aise files cross-ref ./file.py               # verify edits in current file
aise files cross-ref ./file.py --session ID
```

### Tool Call Search
```bash
aise tools search Write                      # all Write calls
aise tools search Bash "git"                 # Bash calls matching pattern
aise tools search Edit "filename"            # Edit calls
aise tools search Read                       # all Read calls
aise tools search Write --format json
aise tools search Write --limit 20
```

### Session Analysis
```bash
aise messages analyze SESSION_ID             # tool counts, files touched
aise messages analyze SESSION_ID --format json
aise messages timeline SESSION_ID            # chronological events
aise messages timeline SESSION_ID --preview-chars 80
aise messages corrections                    # user corrections to Claude
aise messages corrections --project myproject
aise messages corrections --limit 50
aise messages planning                       # planning command frequency
aise messages extract SESSION_ID pbcopy      # clipboard content
aise messages extract SESSION_ID pbcopy --format json
```

### Export
```bash
aise export session SESSION_ID               # → stdout
aise export session SESSION_ID --output f.md # → file
aise export session SESSION_ID --dry-run     # preview
aise export recent 7                         # last 7 days → stdout
aise export recent 7 --output week.md
aise export recent 14 --project myproject --output sprint.md
```

### Combined Search
```bash
aise search                                  # default: all files
aise search --query "error"                  # auto-routes to messages
aise search --pattern "*.py"                 # auto-routes to files
aise search --pattern "*.py" --query "error" # both: files + messages
aise search --tool Write --query "login"     # tool search with query
aise search tools --tool Bash --query "git"  # explicit tools domain
aise find messages --query "error"           # find = alias for search
aise find files --pattern "*.py"
```

### Statistics
```bash
aise stats                                   # session + file counts
```

---

## Output Formats

All commands support `--format` / `-f`:

| Format | Use When |
|--------|----------|
| `table` | Default — human-readable in terminal |
| `json` | Scripting, piping to `jq`, programmatic use |
| `csv` | Spreadsheet import |
| `plain` | Raw text, minimal formatting |

---

## Session File Structure

Sessions live at `~/.claude/projects/<ENCODED-PATH>/<SESSION-ID>.jsonl`

Path encoding: non-alphanumeric characters → `-`
- `/Users/alice/myproject` → `-Users-alice-myproject`
- `/Users/alice/.claude` → `-Users-alice--claude` (dot → dash)
- `/home/alice/project` → `-home-alice-project`

Each JSONL line is a JSON object with `type` (`user`/`assistant`/`system`), `timestamp`, and `message` containing tool calls and text content.

---

## Configuration

```bash
# Override projects directory (default: ~/.claude/projects)
export AI_SESSION_TOOLS_PROJECTS=~/.claude/projects
```
