---
name: "l1-promote"
description: "Review L2 session facts and promote valuable ones to L1 Atomic Memory. Use at end of session or when L2 accumulates facts worth keeping permanently. Runs add-fact.sh for each promoted fact."
---

# L1 Promote Skill

## When to trigger

- End of session: "promote facts", "save session facts", "l1-promote"
- When L2 has 3+ facts and session is wrapping up
- After `/session` shows facts worth keeping permanently
- "cuối session", "lưu facts", "promote l2 lên l1"

## What to do

### Step 1 — List current L2 facts

```bash
bash .claude/scripts/search-session-facts.sh
```

If output is empty or "no session facts found": report "No L2 facts to promote" and stop.

### Step 2 — Evaluate each fact for promotion

For each L2 fact, apply this filter — promote only if:

| Criterion | Promote | Skip |
|-----------|---------|------|
| Still true beyond this session? | ✓ | ✗ |
| Reusable in future sessions? | ✓ | ✗ |
| Specific enough to be useful? | ✓ | ✗ |
| About session state only (e.g. "currently editing X")? | ✗ skip | |
| Duplicate of existing L1 fact? | ✗ skip | |

Present the list to the user with your recommendation (promote/skip) for each.
Ask: "Promote these? [y/n for each or 'all'/'none']"

### Step 3 — Run add-fact.sh for approved facts

For each fact approved by the user:

```bash
bash .claude/scripts/add-fact.sh
```

`add-fact.sh` is interactive — guide the user through:
- `name`: short slug (kebab-case)
- `type`: decision | constraint | pattern | reference | warning
- `scope`: yamtam | project | global
- `value`: the fact content
- `confidence`: verified | likely | unverified
- `tags`: comma-separated

Pre-fill from the L2 fact content where possible to reduce typing.

### Step 4 — Clear promoted facts from L2

After all promotions:

```bash
bash .claude/scripts/clear-session.sh
```

Confirm with user before clearing. If user wants to keep some L2 facts for next session, skip clear.

### Step 5 — Report

```
L1 Promote Summary
──────────────────
L2 facts reviewed:  N
Promoted to L1:     N
Skipped:            N
L2 cleared:         yes/no

Promoted facts are now in memory/L1_atomic/
Search with: /memory <keyword>
```

## Constraints

- Never promote facts about current file state, git branch, or session-specific context.
- Never auto-promote without user confirmation.
- Never run `add-fact.sh` non-interactively — it requires user input for quality control.
- If `add-fact.sh` is missing, say so and stop.
