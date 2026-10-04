---
name: weekly
description: Use for a weekly operating review (Friday wrap or Monday plan) — review progress against the 90-day priorities, surface stalled open loops, and set next week's focus. This is the PERSONAL operating review; distinct from /audit (checks the kit's connections/freshness) and /level-up (finds one automation to build). Trigger on "/weekly", "weekly review", "weekly planning", "how did this week go", "plan my week".
---

# Weekly Operating Review

The Cadence layer at week resolution: close the loop on the week, surface what stalled, and aim the
next week at the priorities that matter.

> Not to be confused with: **/audit** (is the *kit* healthy — connections, freshness) or
> **/level-up** (build one new automation). This skill reviews *your week and priorities*.

## When to run
- End of week (retrospective) or start of week (planning) — it does both.

## The output (always this shape)
```
## Weekly review — week of <date>
**Moved** — progress on each 90-day priority this week (concrete, not vibes).
**Stalled / at risk** — priorities or loops that didn't move + why + the unblock.
**Closed loops** — commitments resolved this week.
**Carrying forward** — open loops into next week, with owners.
**Next week's focus** — 3–5 outcomes for the coming week, tied to priorities.
**Surfaced for /level-up** — any task done manually 3+ times this week (candidate to automate).
```

## Process
1. **Read:** `context/priorities.md`, `decisions/log.md` (this week's entries), `projects/`, and open loops (`tools/open_loops.py` if present).
2. **Assess each priority:** moved / stalled / at-risk, with evidence (a shipped thing, a decision, a metric) — not assertion.
3. **Diagnose stalls:** for each, name the single blocker and the unblocking action/owner.
4. **Plan next week:** propose 3–5 outcomes mapped to the 90-day priorities; keep it realistic.
5. **Spot recurring manual work** → list it under "Surfaced for /level-up".
6. **Offer to log:** append a dated summary entry to `decisions/log.md` (allowed without approval).

## Autonomy
**L2 — drafts the review and next-week plan; the human confirms.**

## Guardrails (from CLAUDE.md)
- Evidence over assertion — "verify before you claim done."
- No confidential figures persisted; reference live sources.
- Route next-week owners to the team where appropriate.
