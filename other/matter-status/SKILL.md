---
name: matter-status
description: "Shows a complete status summary for a matter. Use when Mandy says 'status', 'what's happening with', 'where are we with', 'summary', or asks about a specific client's matter. Shows client details, deadlines, stage expectations, documents, flags, letters, financials, and recent history."
---

# Matter Status

## Important
- READ-ONLY. Do not commit.
- Resolve matter first.

## Instructions

### Step 0: Resolve Matter
Follow `_shared/resolve-matter.md`.

### Step 1: Gather Data
1. Read `matter.json` fully
2. Read all `.extract.json` files (Tier 1) — collect all flags
3. Check for unanalysed documents
4. Read last 20 lines of `activity-log.jsonl`
5. Check stage expectations from `rules/stage-expectations.json`
6. Git history: `git -C matters/ log --oneline -10 -- {id}/`
7. Check compliance: costs disclosure sent?

### Step 2: Present
```
CLIENT: name, DOB, contact, preferred method
MATTER: ID, type, stage, sub_stage, claim number, DOI
INJURY: mechanism, body parts, work capacity, CoC status
INSURER: name, agent, contact
LIMITATION: expiry date, time remaining
DEADLINES: all with status (✓ met / ⚠ overdue / ⏰ imminent / ○ pending)
STAGE EXPECTATIONS: checklist (✓ / ⚠ / ○)
COSTS DISCLOSURE: s174 status
DOCUMENTS: list with analysed status
FLAGS: open flags with severity
LETTERS: all with status
FINANCIALS: estimated value, fees, disbursements
RECENT HISTORY: last 10 git entries
NEXT STEPS: prioritised recommendations
```
