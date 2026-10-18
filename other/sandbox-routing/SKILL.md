---
name: Sandbox Routing
description: SELF-CORRECT tool choice. About to Read a long file just to extract one piece of info? Use a sandbox tool that returns only the summary. About to run a long shell command? Same. Sandbox keeps raw output OUT of context — only summaries land. Triggers when about to flood context with large output.
---

# Sandbox Routing

> [!danger] HARD RULE — fires before any large Read or Bash that isn't for editing
> If you're about to Read a long file to *analyze* (not to Edit), or run a Bash command with >20 line output, **route through sandbox tools instead**. Raw output stays out of context; only the summary you print enters context.

This skill assumes your Claude Code install includes context-mode (or equivalent) sandbox tools — `ctx_execute`, `ctx_execute_file`, `ctx_batch_execute`. If those aren't available, the principle still applies: use `head_limit` on Grep, narrow Read to specific line ranges, and avoid `cat large.log`.

## The decision tree

```
Am I about to Read or run Bash?
   ├── Editing a file? (need full content for Edit tool)
   │     → Read is correct, proceed
   │
   ├── Running git status / git log -n short / mkdir / mv / rm / short command?
   │     → Bash is correct, proceed
   │
   ├── Reading a file just to extract a piece of info / find a line?
   │     → STOP. Use ctx_execute_file with grep/awk code that prints just the answer.
   │
   ├── Running a shell command with >20 line output?
   │     → STOP. Use ctx_execute with the same command — only printed summary enters context.
   │
   └── Multiple commands at once?
         → Use ctx_batch_execute with all commands as labelled chunks, indexed for FTS5 search.
```

## When to use each tool

### `ctx_execute(language, code)`
- Shell command with large output → `language: "shell"`
- Python data processing → `language: "python"`
- API calls + response analysis → wrap the call in code
- Anything where you want *the answer*, not the raw output

### `ctx_execute_file(path, language, code)`
- File analysis without loading the file into context
- Searching within a specific known file
- Extracting structured info from JSON/YAML/MD

### `ctx_batch_execute(commands, queries)`
- Multiple commands you want to run + index together
- Chained recon (e.g., git log + git diff + git status as one batch)
- Building a knowledge base for later FTS5 queries

## Calibration anchors

| File size | Read/Bash OK? | Sandbox? |
|---|---|---|
| <20 lines | ✅ Read/Bash | not needed |
| 20-100 lines | ✅ if editing or referencing in full | ✅ if extracting |
| 100-500 lines | ⚠️ only if editing | ✅ for extraction |
| 500+ lines | ❌ unless absolutely editing | ✅ always for extraction |

## Concrete examples

### Example A: Find an insertion anchor in a 900-line JSON
- ❌ **Wrong:** `Read skill-index.json (entire file)` to find where to insert
- ✅ **Right:** `ctx_execute_file path=skill-index.json code='grep -n "skill-name" skill-index.json'` → returns just the line number, then use Edit

### Example B: Check git log for a specific commit pattern
- ❌ **Wrong:** `Bash: git log --oneline -100` (100 lines of log into context)
- ✅ **Right:** `ctx_execute language=shell code='git log --oneline -100 | grep -i "ship"'` → returns just matches

### Example C: Read a large config file for one value
- ❌ **Wrong:** `Read large-config.yaml`
- ✅ **Right:** `ctx_execute_file path=large-config.yaml code='grep "specific_key" large-config.yaml'`

## Output format

When this skill fires, internally evaluate before the tool call:
- Will the raw output be >20 lines AND I don't need it for editing?
- If yes → re-route to sandbox before invoking

You don't need to announce this to the principal. Just use the right tool.

## Anti-patterns this prevents

- Reading a 900-line skill-index just to find an insertion anchor
- `cat large.log` via Bash to "see what's happening"
- Reading 50-page docs to extract one quote
- Running parallel Bash commands when a single batch call could do one round-trip
- The PreToolUse hooks firing reminders that get ignored as false positives

## Connects to

- [`/timeline-calibration`](../timeline-calibration/SKILL.md) — sister discipline rule, both about respecting the resource budget
