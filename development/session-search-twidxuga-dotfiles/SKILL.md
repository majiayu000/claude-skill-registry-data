---
name: session-search
description: Search across Claude Code session transcripts and prompt history for keywords. Equivalent to OpenCode's session_search.
user-invocable: true
argument-hint: "<query> [--project filter] [--limit N]"
---

# Session Search

Search across Claude Code session transcripts for keywords or patterns. This operates on the JSONL transcript files and the global prompt history.

## Search strategies

### 1. Global prompt history (fastest — search all user prompts)

```bash
jq -r --arg q "$QUERY" 'select(.display | test($q; "i")) | [(.timestamp / 1000 | strftime("%Y-%m-%d %H:%M")), .sessionId[0:12], .project, (.display[0:80])] | @tsv' ~/.claude/history.jsonl 2>/dev/null | tail -${LIMIT:-30} | column -t -s$'\t'
```

### 2. Session index search (search first prompts across all projects)

```bash
for idx in ~/.claude/projects/*/sessions-index.json; do
  project=$(echo "$idx" | sed 's|.*projects/||;s|/sessions-index.json||')
  jq -r --arg q "$QUERY" --arg p "$project" '.entries[] | select(.firstPrompt | test($q; "i")) | [$p, .sessionId[0:12], .firstPrompt[0:80], .modified] | @tsv' "$idx" 2>/dev/null
done | sort -t$'\t' -k4 -r | head -${LIMIT:-20} | column -t -s$'\t'
```

### 3. Deep transcript search (slower — search full conversation content)

```bash
for f in ~/.claude/projects/${PROJECT_FILTER:-*}/*.jsonl; do
  matches=$(grep -ci "$QUERY" "$f" 2>/dev/null || echo 0)
  if [ "$matches" -gt 0 ]; then
    sid=$(basename "$f" .jsonl | cut -c1-12)
    echo -e "${matches}\t${sid}\t${f}"
  fi
done | sort -t$'\t' -k1 -rn | head -${LIMIT:-20} | column -t -s$'\t'
```

### 4. Extract matching lines from a specific transcript

Once you have a session file path from the search above:

```bash
jq -r --arg q "$QUERY" 'select(.message?.content?) | select(.message.content | tostring | test($q; "i")) | [(.timestamp // 0 | if . > 0 then (. / 1000 | strftime("%H:%M")) else "?" end), (.message.role // "?"), (.message.content | tostring | .[0:120])] | @tsv' "$FILE" 2>/dev/null | head -30
```

## Arguments

Parse `$ARGUMENTS` for:
- First positional argument: search query (required)
- `--project <filter>`: restrict to matching project directories
- `--limit N` or `-n N`: max results (default 20)
- `--deep`: force full transcript search (slower but comprehensive)
- `--prompts-only`: search only user prompts via history.jsonl (fastest)

## Workflow

1. Start with prompt history search (strategy 1) — instant results
2. If insufficient, try session index search (strategy 2)
3. For thorough search, use deep transcript search (strategy 3)
4. Once you find a relevant session, use `/session-read <session-id>` for details
