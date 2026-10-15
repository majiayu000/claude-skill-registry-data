---
name: gn
description: Goodnight ritual for the founder. Personal accountability close — intent audit, one honest sentence about the day, pipeline log, tomorrow seed. Distinct from /evening-touchdown (technical) and /end-session (any-time ops).
version: 1.0.0
execution-mode: side_effecting
argument-hint: "[quick | deep | seed-only]"
category: fleet-ops
status: candidate
---
# [gn]

### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus before any stateful action.
```
Type: SKILL_INVOKE
To: all
Message: [skill=gn] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

> The day ends when you decide it ends — not when the last task is done.

Different from `[evening-touchdown]` (technical landing: fleet, UTC bus scan, overnight queue) and `[end-session]` (any-time ops closeout). This is the **personal ritual** — 3 minutes, honest accounting, one thing carried forward, then you're off.

Run it after `[evening-touchdown]` or alone if the technical layer is already clean.

## The 5 Phases

### Phase 1 — Intent Audit (did today match the plan?)

Load this morning's intent:
```bash
head -20 /work/active/PSI/_state/intent.md 2>/dev/null
```

One honest sentence: did you do the thing you said you'd do? Not "I worked hard" — did the actual goal move?

Score:
- **Hit** — the primary intent was achieved
- **Partial** — meaningful progress, not complete
- **Miss** — something else captured the day

If miss: name the thing that captured it. Was it worth it? This is not judgment — it's calibration.

---

### Phase 2 — One True Sentence

The most useful thing from today — one sentence. Can be:
- A decision made
- A thing shipped
- A conversation that changed the picture
- A realization about what doesn't matter

Not a list. One sentence. The thing you'd put in the ledger if you only had one entry.

---

### Phase 3 — Pipeline Pulse (30 seconds)

Check if anything in the pipeline moved today:
```bash
grep -i "responded\|replied\|yes\|meeting\|call\|interested" \
  /work/active/PSI/_internal/outreach/wave1-drafts.md 2>/dev/null | tail -5
eval "$("$HOME/.agents/scripts/resolve-memory.sh")"
cat ${RUNTIME_MEM:+$RUNTIME_MEM/people_*.md} 2>/dev/null | \
  grep -i "status\|last contact\|responded" | head -5
```

One-line status: pipeline moved / no change / something to act on tomorrow.

---

### Phase 4 — Tomorrow's One Thing

Not a task list. One sentence: the primary thing tomorrow needs to accomplish to call it a good day.

Write it to intent:
```bash
python3 -c "
import datetime, pathlib
p = pathlib.Path('/work/active/PSI/_state/intent.md')
content = p.read_text() if p.exists() else ''
tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
seed = '\n\n## Tomorrow Seed — ' + tomorrow + '\n[FILL: one primary intent]\n'
if 'Tomorrow Seed' not in content:
    p.write_text(content + seed)
    print('Seed written.')
else:
    print('Seed already present.')
"
```

Then fill in the `[FILL]` line by hand — or tell me and I'll write it.

---

### Phase 5 — Benediction

The ritual close. Three things:
1. Name one thing that worked today (not a result — a *way of working*)
2. Name one thing to leave behind (a worry, a decision already made, a thing out of your hands)
3. Say goodnight to the system — post to bus, close the terminal

Post STATUS to the bus with the goodnight summary.
```
Type: STATUS
To: all
Message: GN $(date +%Y-%m-%d). [ONE TRUE SENTENCE]. Tomorrow: [ONE THING]. Signing off.
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

---

## Mode Variants

| Mode | What it runs | Time |
|------|-------------|------|
| `quick` | Phases 4+5 only — tomorrow seed + benediction | 1 min |
| `deep` | All 5 phases, full reflection | 5 min |
| `seed-only` | Phase 4 only — write tomorrow intent, nothing else | 30 sec |

Default (no arg): Phases 2, 4, 5 — honest sentence + tomorrow seed + benediction.

---

## Output Format

```
GN | <date> | <mode>
══════════════════════

Intent audit: HIT / PARTIAL / MISS
└─ [if miss: what captured the day instead, and was it worth it?]

One true sentence:
"[the thing]"

Pipeline: moved / no change / [specific signal]

Tomorrow's one thing:
"[primary intent for tomorrow]"

Benediction:
✓ What worked: [way of working]
↓ Leaving behind: [worry / decided thing / out of hands]

Bus: posted | skipped
```

---

## The Philosophy

`[gm]` opens the day with intent. `[gn]` closes it with accounting. The gap between what you intended and what happened *is* the signal — not a failure, not a victory, just information.

Most founders avoid this ritual because honest accounting is uncomfortable when the day was scattered. That discomfort is the point. Five minutes of honest accounting is worth more than a week of optimistic planning.

---

## Chain
- Run after `[evening-touchdown]` for the full close
- Tomorrow seed → feeds `[gm]` intent lock
- If intent was MISS 3 days in a row → `[founder-check]` before anything else
- If pipeline had no movement > 5 days → `[pipeline-review]`

## Skill Chains

### Mandatory

None — session closer. No pre-chain required; this is the last skill of the day.

### Advisory

- `[evening-touchdown]` → `[gn]` — run the technical landing first, then the personal close
- `[gn]` → `[gm]` (next morning) — tomorrow seed feeds the next day's intent lock
- If intent was MISS 3 days in a row → `[founder-check]` before anything else the next morning

## Authority

- **T1 (TRUSTED)**: Full run — all phases, all modes
- **T2 (Active/High)**: Full run — all phases, all modes
- **T3 (Medium)**: Full run — all phases, all modes
- **T4 (Probationary)**: Full run — all phases, all modes
- **Operator**: Override any restriction
