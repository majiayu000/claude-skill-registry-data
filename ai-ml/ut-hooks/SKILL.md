---
name: ut-hooks
description: View UltraThink hook event log and privacy audit trail
disable-model-invocation: true
allowed-tools: Bash, Read
argument-hint: "[count]"
---

# UltraThink Hook Events

View the privacy hook event log.

## Show recent events

The hook log is at `./reports/hook-events.jsonl` (relative to git root) or check common locations:

```bash
LOG_FILE=""
for path in "$(git rev-parse --show-toplevel 2>/dev/null)/reports/hook-events.jsonl" "./reports/hook-events.jsonl" "$HOME/Documents/GitHub/InuVerse/ai-agents/ultrathink/reports/hook-events.jsonl"; do
  if [ -f "$path" ]; then
    LOG_FILE="$path"
    break
  fi
done

if [ -z "$LOG_FILE" ]; then
  echo "No hook event log found"
  exit 0
fi

COUNT="${1:-20}"
echo "Last $COUNT hook events from: $LOG_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
tail -n "$COUNT" "$LOG_FILE" | jq -r '"[\(.severity)] \(.timestamp) \(.action) — \(.path // .file // "n/a") — \(.description // .message // "n/a")"' 2>/dev/null || tail -n "$COUNT" "$LOG_FILE"
```

Default to 20 events, or use `$ARGUMENTS` as the count.

## Summary stats

```bash
if [ -f "$LOG_FILE" ]; then
  echo ""
  echo "Stats:"
  echo "  Total events: $(wc -l < "$LOG_FILE" | tr -d ' ')"
  echo "  Blocked:      $(grep -c '"blocked"' "$LOG_FILE" 2>/dev/null || echo 0)"
  echo "  Allowed:      $(grep -c '"allowed"' "$LOG_FILE" 2>/dev/null || echo 0)"
  echo "  Warnings:     $(grep -c '"warning"' "$LOG_FILE" 2>/dev/null || echo 0)"
fi
```

Present results in a clean table format with severity color indicators.
