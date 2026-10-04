---
name: source-session
description: Find the Claude Code session that originated a given artifact — commit hash, PR, idea/decision, file, or feature name. Use when the user invokes /source-session [query] or asks "what session did we make X in" or "where did this come from". Searches ~/.claude/history.jsonl by correlating timestamps or keywords to session windows.
args:
  query:
    description: Artifact to trace — commit hash, PR number, idea/keyword, file path, or feature name
    example: "/source-session abc1234  OR  /source-session 'flecs ecs'  OR  /source-session PR#42"
---

# /source-session [query]

Trace any artifact back to the Claude Code session that produced or decided it.

## Supported Input Types

Detect what the user passed:

| Pattern | Type |
|---------|------|
| 7–40 hex chars | Git commit hash |
| `PR#N` or `#N` | GitHub PR number |
| File path (`/` or `./` prefix, or ends in extension) | File |
| Anything else | Keyword/idea search |

## Workflow by Type

### Commit hash

1. Get the commit's author timestamp from git:
```bash
git log --format="%at %H %s" | grep "^[0-9]* HASH"
# or
git show -s --format="%at %s" HASH
```

2. Find sessions whose time window contains that timestamp:
```bash
# Get per-session min/max timestamps from history
jq -r --arg project "$PWD" \
  'select(.project == $project) | [.sessionId, (.timestamp / 1000)] | @tsv' \
  ~/.claude/history.jsonl \
  | awk -F'\t' '{
      if (!min[$1] || $2 < min[$1]) min[$1] = $2;
      if ($2 > max[$1]) max[$1] = $2;
    }
    END { for (s in min) print min[s], max[s], s }' \
  | sort
```

3. Match: find session where `session_start <= commit_time <= session_end`. If the commit falls in a gap between sessions, assign to the session that ended most recently before the commit (user likely committed right after stopping).

4. Show the matching session: date, resume command, and 5 surrounding messages from the session for context.

### PR number

1. Use `gh pr view N --json createdAt,title,body,commits` to get PR metadata and commit SHAs.
2. Trace each commit SHA as above.
3. Report the sessions that cover the PR's commits.

### File path

1. Use `git log --follow --format="%at %H %s" -- PATH` to get all commits touching that file.
2. Trace each commit to a session.
3. Report: creation session + most recent modification session.

### Keyword / idea search

Search `~/.claude/history.jsonl` for the keyword across all sessions in the current project:

```bash
jq -r --arg project "$PWD" \
  'select(.project == $project and (.display | ascii_downcase | contains("KEYWORD"))) |
   [(.timestamp / 1000 | strftime("%Y-%m-%d %H:%M")), .sessionId, (.display[:200])] | @tsv' \
  ~/.claude/history.jsonl | sort
```

Group hits by session, rank by hit density. Show top 3 sessions with surrounding messages.

## Output Format

```
**Artifact:** [what was searched]
**Type:** commit | PR | file | keyword

**Found in session:**
Date: YYYY-MM-DD HH:MM–HH:MM
Project: ~/path/to/project
Resume: claude --resume SESSION_ID

**Context** (messages around the time of the artifact):
HH:MM  "message content..."
HH:MM  "message content..."
...
```

If multiple sessions match (keyword search), list them ranked by relevance with hit counts.

If nothing found, say so — don't fabricate a session.

## Cross-project search

If the artifact isn't found in the current project's sessions, automatically widen to all projects in `~/.claude/history.jsonl` before giving up.
