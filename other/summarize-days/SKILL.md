---
name: summarize-days
description: Summarize what was accomplished and decided across Claude Code sessions for the past N days. Use when the user invokes /summarize-days [N] or asks "what have we done in the past N days". Reads ~/.claude/history.jsonl, groups sessions by project and day, samples messages, and synthesizes a human-readable digest of accomplishments and major decisions.
args:
  N:
    description: Number of days to look back (e.g. 7 = last 7 days)
    type: integer
    default: 3
    example: "/summarize-days 14"
---

# /summarize-days [N]

Produce a digest of all Claude Code work from the past N days across all projects (or scoped to current project if specified).

## Arguments

- `N` — integer, days to look back (e.g. `/summarize-days 7` = last 7 days). Default: 3 if omitted.
- `--project` — restrict to current working directory's project only.

## Workflow

### 1. Compute the cutoff timestamp

```bash
# N days ago in epoch seconds
CUTOFF=$(python3 -c "import time; print(int(time.time()) - N * 86400)")  # replace N with arg
```

### 2. Extract sessions in window

```bash
# All messages from the past N days
jq -r --argjson cutoff "$CUTOFF" \
  'select((.timestamp / 1000) >= $cutoff) | [(.timestamp / 1000 | strftime("%Y-%m-%d")), .sessionId, .project, (.display[:200])] | @tsv' \
  ~/.claude/history.jsonl | sort
```

Filter to current project only if `--project` flag used:
```bash
jq -r --argjson cutoff "$CUTOFF" \
  'select((.timestamp / 1000) >= $cutoff and .project == "'"$PWD"'") | ...' \
  ~/.claude/history.jsonl
```

### 3. Group by project + session

For each unique `(project, sessionId)` pair, extract ALL user messages (not just first/last — sample evenly across the session):

```bash
# All messages from one session
jq -r --arg sid "SESSION_ID" \
  'select(.sessionId == $sid) | [(.timestamp / 1000 | strftime("%H:%M")), (.display[:250])] | @tsv' \
  ~/.claude/history.jsonl | sort
```

Sample strategy for long sessions (>20 messages): take first 3, last 3, and every Nth in between to get ~12 representative messages. This preserves session arc (setup → work → conclusion).

### 3b. Correlate commits to sessions (always — no flag needed)

For each project in the window, get git log with timestamps:

```bash
# From the project directory
git -C PROJECT_PATH log --format="%H %at %s" --since="$(date -d "N days ago" +%Y-%m-%d 2>/dev/null || date -v-Nd +%Y-%m-%d)" 2>/dev/null
```

For each commit, find the session whose time window contains the commit timestamp:
- A session's window = `[first_message_timestamp, last_message_timestamp]`
- Match commit `author_time` against session windows
- If a commit falls between two sessions (gap), assign to the earlier one (most likely the committing session)
- If outside all session windows but within N days, list under date with no session attribution

Annotate each session summary with its commits:
```
**commits:** `abc1234` fix(mining): normalize vein density — `def5678` test: add NewsManager round-trip
```

If no commits in a session, omit the commits line entirely.

### 4. Synthesize per-session summary

For each session, produce:
- **What was built/fixed/decided** — concrete outputs, not vague activity
- **Major decisions** — architecture choices, approach pivots, tool selections, explicit user approvals
- **Unresolved / in-progress** — if session ended mid-task or with "proceed" / "continue" hanging
- **commits** (if any, from step 3b)

Use the message content directly. Don't speculate — if the messages are too thin to determine what happened, say "session content unclear."

### 5. Render the digest

Group by date, then project. Within each project-day, one paragraph per session (or merge short sessions on same day).

```
## YYYY-MM-DD

### ~/path/to/project

**Session 1** (HH:MM–HH:MM)
[accomplishments + decisions]
**commits:** `abc1234` fix(thing): description

**Session 2** ...

---

## YYYY-MM-DD (continued)
...
```

End with a **Summary** section: bullet list of the 5–10 most significant things accomplished across all sessions in the window.

## Output Rules

- Lead with date headings, not session IDs (include session ID in parentheses for `--resume` reference)
- Bold concrete outputs: file names, feature names, system names
- Decisions get a `→` prefix: `→ Chose Flecs.NET over custom ECS for relational queries`
- Skip sessions that are clearly just `/compact`, `/new`, or single-message with no content
- If N > 14 days: warn that output may be very long and suggest narrowing scope or using `--project`

## Resume Reference

Append at end:

```
## Resume Commands
- `claude --resume SESSION_ID`  — [project] [date] [one-line topic]
```

Only include sessions that ended with unfinished work.
