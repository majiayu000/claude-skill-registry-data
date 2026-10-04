---
name: respawn-self
description: >
  PD context-aware self-respawn. Invoked by a PD agent when context window reaches
  80% threshold. Saves current state, writes a continuation manifest with all
  in-flight work and next actions, then stops. The parent session (or user) spawns
  a fresh PD with the manifest. Enforces max 3 respawns per project per 24h.
  Invoke when context ≥ 80% during a PD session. Also used proactively at phase
  transitions when context > 70% and a major task boundary is clean.
---

# /respawn-self — PD Context-Aware Self-Respawn

## When to Invoke

- **Mandatory:** when context window reaches 80% (CONTEXT_PCT_ALERT fires)
- **Proactive:** at a clean phase boundary (all current L3s done) when context > 70%
- **Never mid-L3:** do not invoke while an L3 Coord is in flight — wait for ACK/NACK
  from the current Coord, complete the phase, then respawn

## Respawn Counter Enforcement

Max 3 respawns per project per 24h. Counter lives at:
`~/.claude/state/respawn-counters/{slug}.txt` (format: `{count} {epoch-timestamp-of-reset}`)

```bash
SLUG="{project-slug}"
COUNTER_FILE="$HOME/.claude/state/respawn-counters/$SLUG.txt"
NOW=$(date +%s)
DAY=86400

mkdir -p "$HOME/.claude/state/respawn-counters"

if [ -f "$COUNTER_FILE" ]; then
  COUNT=$(awk '{print $1}' "$COUNTER_FILE")
  RESET_AT=$(awk '{print $2}' "$COUNTER_FILE")
  AGE=$(( NOW - RESET_AT ))
  if [ "$AGE" -ge "$DAY" ]; then
    COUNT=0
    RESET_AT=$NOW
  fi
else
  COUNT=0
  RESET_AT=$NOW
fi

if [ "$COUNT" -ge 3 ]; then
  echo "RESPAWN_BLOCKED: max 3 respawns reached for $SLUG in last 24h. Save state and stop — manual restart needed."
  exit 1
fi

NEW_COUNT=$(( COUNT + 1 ))
echo "$NEW_COUNT $RESET_AT" > "$COUNTER_FILE"
echo "RESPAWN_OK: respawn $NEW_COUNT/3 for $SLUG"
```

If RESPAWN_BLOCKED: run `/save-state {slug}` and stop with a clear message to root.

## Step 1 — Complete Current Work Unit

Before saving state, complete the smallest safe stopping point:
- If mid-Coord-ACK/NACK cycle: finish the ACK/NACK exchange
- If mid-aggregation: finish writing the digest
- Never stop mid-edit or mid-Coord-spawn

## Step 2 — Write Continuation Manifest

Write to `{project}/memory/agents/respawn-manifest-{timestamp}.md`:

```markdown
# Respawn Manifest — {project} — {timestamp}
Context at respawn: {PCT}%
Respawn count: {N}/3

## What Was Completed This Session
- {L3 or task}: {status}
- ...

## In-Flight at Respawn
- {Coord-name or task}: {state, what was last communicated}
- ...

## Next Action for Fresh Session
{exact next action — one sentence, precise}

## Pending L3s (not yet started)
- {L3-name}: {description}
- ...

## Active Blockers
{none | list}

## Key Decisions Made This Session
{locked decisions that affect the continuation}
```

## Step 3 — Run /save-state

```
Skill({ skill: "save-state", args: "{slug}" })
```

## Step 4 — Update next-session.md

Ensure next-session.md points to the respawn manifest:
```
Next: Resume from respawn manifest at {project}/memory/agents/respawn-manifest-{timestamp}.md
Mid-flight: respawn-manifest-{timestamp}.md — continuation manifest with all in-flight work
```

## Step 5 — Notify Root

Send to "root" via SendMessage:
```
PD-{slug}: SELF-RESPAWN TRIGGERED
Context at respawn: {PCT}%
Respawn count: {N}/3
State saved. Continuation manifest: {project}/memory/agents/respawn-manifest-{timestamp}.md
Fresh PD session needed to continue — run /pd-resume {slug}
```

## Step 6 — Stop

Do not attempt more work. The fresh PD session will read the manifest and continue.
