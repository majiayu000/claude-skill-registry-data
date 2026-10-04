---
name: coord-respawn-self
description: >
  Coord context-aware self-respawn. Invoked by a Coord agent when context window
  reaches 80% threshold mid-L3. Saves mid-L3 state, writes a continuation manifest,
  notifies the spawner (PD or Dept Head depending on caller role), and stops. The
  spawner then resumes the L3 with a fresh Coord. Enforces max 3 respawns per Coord
  per 24h. Use at clean task boundaries only — never mid-Executor-spawn or
  mid-ACK/NACK cycle.
---

# /coord-respawn-self — Coord Context-Aware Self-Respawn

## When to Invoke

- **Mandatory:** when context window reaches 80% (CONTEXT_PCT_ALERT fires)
- **Proactive:** at a clean sub-task boundary within L3 when context > 70%
- **Never mid-Exec:** do not invoke while an Executor is awaiting APPROACH or CHECKPOINT
  response — finish that exchange first, then respawn

## Respawn Counter Enforcement

Max 3 respawns per Coord per 24h. Uses the same counter mechanism as /respawn-self:
`~/.claude/state/respawn-counters/coord-{l3-name}-{pun}.txt`

```bash
COORD_ID="coord-{l3-name}-{pun}"
COUNTER_FILE="$HOME/.claude/state/respawn-counters/$COORD_ID.txt"
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
  echo "RESPAWN_BLOCKED: max 3 respawns reached for $COORD_ID in 24h."
  exit 1
fi

NEW_COUNT=$(( COUNT + 1 ))
echo "$NEW_COUNT $RESET_AT" > "$COUNTER_FILE"
echo "RESPAWN_OK: respawn $NEW_COUNT/3 for $COORD_ID"
```

If RESPAWN_BLOCKED: escalate to PD with current state — do not continue.

## Step 1 — Complete Current Work Unit

- Finish any pending APPROACH or CHECKPOINT gate exchange
- Do NOT start a new Exec spawn
- Reach a clean "N Execs ACKed, M pending" boundary

## Step 2 — Write Coord Continuation Manifest

Write to `{project}/memory/agents/coords/coord-{l3-name}-{pun}-respawn-{timestamp}.md`:

```markdown
# Coord Respawn Manifest — Coord-{l3-name}-{pun} — {timestamp}
Context at respawn: {PCT}%
Respawn count: {N}/3
L3 task: {l3-task-description}

## Sub-tasks Completed
- {Exec-name}: {status} — {1-line summary}
- ...

## Sub-tasks In Flight at Respawn
- {Exec-name or task}: {state — e.g. "APPROACH received, not yet approved"}
- ...

## Sub-tasks Not Yet Started
- {task}: {description}
- ...

## Scratch State
(copy current ## Status and ## Children tables)

## Next Action for Fresh Coord
{exact next action — e.g. "Spawn Exec-{X} for task Y, then Exec-{Z} for task W in parallel"}

## Active Blockers
{none | list}
```

## Step 3 — Notify Your Spawner

**Determine who your spawner is:**
- If you are an **execution Coord** (spawned by a PD, `reports_to: pd-coordinator`):
  → Send to "PD-{slug}" via SendMessage.
- If you are a **Dept-Coord** (role: dept-coord, spawned by a dept lead):
  → Send to your Dept Head (e.g. "engineering-lead", "marketing-lead") via SendMessage.

Message format (same in both cases — substitute the correct recipient):
```
Coord-{l3-name}-{pun}: COORD_RESPAWN TRIGGERED
Context at respawn: {PCT}%
Respawn count: {N}/3
L3: {l3-task-name} — {completed}/{total} sub-tasks done
Continuation manifest: {project}/memory/agents/coords/coord-{l3-name}-{pun}-respawn-{timestamp}.md
A fresh Coord session is needed to continue this L3.
Spawner should start a new Coord-{l3-name}-{pun} with the manifest path in the spawn prompt.
```

## Step 4 — Delete Scratch and Stop

Delete `{project}/memory/agents/coords/coord-{l3-name}-{pun}-scratch.md`.
Stop. The fresh Coord will read the manifest and continue.
