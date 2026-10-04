---
name: hot-graduator
description: |-
  Scans HOT.md and proposes which rules should graduate to SOUL.md (untouched 30+ days)
  or be removed entirely. Run weekly via cron, or invoke ad-hoc when HOT.md feels stale.
  Triggers: "clean up HOT", "graduate rules", "is HOT.md stale", "what HOT rules can I drop".
---

# HOT Graduator

Enforces the HOT.md self-graduation rule: rules untouched 30+ days move out.

## When to use
- Weekly cron run (or manual invocation when HOT.md feels stale)
- After a SOUL.md update to verify HOT entries are still distinct

## Process

1. Run `python tools/hot_graduator.py` — outputs candidates
2. For each candidate, decide:
   - **Graduate** → move the rule into SOUL.md (find the right section)
   - **Drop** → delete from HOT.md (the lesson is internalized)
3. Update HOT.md (remove graduated entries; renumber remaining rules)
4. Append a daily-note entry: `[HH:MM IL] Graduated N HOT rules to SOUL §X`

## Output format
- Concise list of decisions
- Diff of HOT.md before/after
- One-line summary to owner DM (only if any rules graduated)
