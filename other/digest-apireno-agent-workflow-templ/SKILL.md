---
name: digest
description: Generate a daily CTO digest summarizing fleet state, recent ADRs/RCAs, telemetry warnings, and pending escalations. Use when CEO asks "what's the digest", "summarize today", or starts the day and wants a status briefing. Also can be wired as a scheduled task.
allowed-tools: Bash(cat *) Bash(ls *) Bash(stat *) Bash(date *) Bash(find *) Bash(wc *) Bash(scripts/agentic/preflight.sh) Read Write
---

# CTO Daily Digest

Generated: !`date -u +%FT%TZ`

## Preflight status (fleet health)

```!
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"; cd "$ROOT" || { echo "ERROR: not in a repo"; exit 1; }
scripts/agentic/preflight.sh 2>&1 || echo "(preflight exited non-zero — see above)"
```

## Recent ADRs (last 7 days)

```!
find docs/architecture/decisions -name 'ADR-*.md' -type f -mtime -7 2>/dev/null | while read f; do
  ts=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$f")
  size=$(stat -f "%z" "$f")
  echo "  $ts  $(basename $f)  (${size} bytes)"
done | sort -r | head -10 || echo "  (none in last 7 days)"
```

## Recent CTO decisions (last 7 days)

```!
find docs/architecture/decisions -name 'cto-decision-*.md' -type f -mtime -7 2>/dev/null | while read f; do
  ts=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$f")
  echo "  $ts  $(basename $f)"
done | sort -r | head -10 || echo "  (none in last 7 days)"
```

## Pending escalations in inbox

```!
INBOX=$HOME/.cto/inbox
if [ -d "$INBOX" ]; then
  count=$(ls "$INBOX"/*.md 2>/dev/null | wc -l | tr -d ' ')
  echo "  $count pending escalation(s) in $INBOX"
  if [ "$count" -gt 0 ]; then
    # A read loop, not `ls -lt | awk` on column numbers: awk field references are
    # dollar-digit tokens, which the skill runtime rewrites with invocation-argument text
    # before awk ever parses the program. (It also stops depending on ls column layout.)
    ls -t "$INBOX"/*.md 2>/dev/null | head -5 | while IFS= read -r _f; do
      printf '    %s  %s\n' "$(date -r "$_f" '+%Y-%m-%d %H:%M' 2>/dev/null)" "$(basename "$_f")"
    done
  fi
else
  echo "  no inbox configured (~/.cto/inbox does not exist — Sprint B work)"
fi
```

## Sprint cycle state (delegate to /sprint-status)

For the per-repo Phase 2 fleet state, run `/sprint-status` separately — it's a richer view than a digest line.

## Your task as CTO

Synthesize the data above into a tight digest for the CEO:

1. **Top-line health:** preflight ok / warnings / critical
2. **What's new since last digest:** ADRs/decisions added in last day specifically (if any)
3. **What needs the CEO's attention:** pending escalations, sprint-accepts waiting, plan revisions outstanding
4. **What's coming up:** any deadlines visible (e.g., countdown to 2026-06-15 from preflight)

Write the digest to `~/cto-daily-$(date +%Y%m%d).md` (one file per day; overwriting same-day reruns is fine).

Present a **5-line summary** to the CEO inline. Brief.

Sign as: — CTO
