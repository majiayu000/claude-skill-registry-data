---
name: save
description: Save current session transcript to markdown with per-turn token counts, cost breakdown, and context usage.
allowed-tools: Bash(*)
argument-hint: "[output_path]"
---

Save the current Claude Code session transcript as a markdown file with token usage, cost stats (/cost), and context window utilization (/context). Never overwrites existing files — appends -1, -2, etc. suffixes.

The user may pass an optional output path as an argument. If provided, use it as OUT. Otherwise default to the current directory.

## Steps

1. Find the most recent session JSONL. Try exact project key first, then fall back to the most recently modified JSONL across all projects (which is almost certainly this session):

```bash
PROJECT_KEY=$(pwd | sed 's|/|-|g')
JSONL=$(ls -t ~/.claude/projects/${PROJECT_KEY}/*.jsonl 2>/dev/null | head -1)
if [[ -z "$JSONL" ]]; then
    JSONL=$(find ~/.claude/projects/ -maxdepth 2 -name '*.jsonl' -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)
fi
if [[ -z "$JSONL" ]]; then
    echo "No session JSONL found" >&2
    exit 1
fi
echo "JSONL: $JSONL"
```

2. Determine output path — use the argument if provided, otherwise save to current directory. If the argument is a directory, create the transcript file inside it:

```bash
SESSION_ID=$(basename "$JSONL" .jsonl)
DATE=$(date +%Y-%m-%d)
DEFAULT_NAME="transcript_${SESSION_ID}_${DATE}.md"
if [[ -n "$ARGUMENTS" ]]; then
    if [[ -d "$ARGUMENTS" ]]; then
        OUT="${ARGUMENTS%/}/${DEFAULT_NAME}"
    else
        OUT="$ARGUMENTS"
    fi
else
    OUT="$(pwd)/${DEFAULT_NAME}"
fi
```

3. Find and run the save script relative to the repo root:

```bash
SAVE_SCRIPT="$(git rev-parse --show-toplevel 2>/dev/null)/.claude/skills/save/save.sh"
if [[ ! -f "$SAVE_SCRIPT" ]]; then
    echo "save.sh not found at: $SAVE_SCRIPT" >&2
    exit 1
fi
bash "$SAVE_SCRIPT" "$JSONL" "$OUT"
```

4. Report the output path and total estimated cost.
