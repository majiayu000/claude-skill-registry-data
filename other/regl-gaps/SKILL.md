---
name: regl-gaps
version: 1.0.0
description: Produce the weekly regulatory digest — a prioritized rollup of new rules, open comment deadlines, and compliance gaps across every tracked matter.
author: matrixx0070
tags: [regulatory, legal, digest, weekly, deadlines, prioritization]
capabilities: []
---

## When to use

Use this once a cadence (typically weekly) to consolidate everything the watchers, diffs, and comment trackers surfaced into one prioritized brief a stakeholder can act on in five minutes. Reach for it to answer "what moved this week and what needs a decision?"

**Not for:** deep analysis of a single rule (use regl-policy-diff), first-time feed setup (use regl-reg-feed-watcher), or discovering latent unmet obligations (use regl-gap-surfacer). Anything in the digest tagged as a legal risk is routed to an attorney, not resolved inside the digest.

## Method

1. Gather inputs from the week: new feed hits (regl-reg-feed-watcher), completed diffs (regl-policy-diff), open/closing comment periods (regl-comments), and outstanding action items.
2. Deduplicate by docket/RIN so one rule appears once even if several skills touched it.
3. Prioritize by urgency × impact: imminent comment deadlines and high-impact final-rule effective dates rise to the top; dormant monitoring drops to a footer.
4. For each item give one line of "so what": what changed and what it obligates — no raw dumps.
5. **Decision point:** separate items needing a stakeholder decision this week from items that are merely informational; flag every legal-risk item for attorney review explicitly.
6. Carry forward last week's open actions with status so nothing silently drops.
7. Keep it scannable — deadlines and decisions at the top, monitoring at the bottom.

## Example

> Week of 2026-06-29. DECIDE NOW: RIN 3170-AB00 comment closes 08-29 — file? (draft ready, regl-comments). EFFECTIVE SOON: State privacy amendment live 07-15, 2 NEW obligations (diff done, owner Compliance). ATTORNEY: ambiguous "affiliated entities" scope. MONITORING: 3 dockets quiet. CARRIED: vendor-DPA update still open (owner Legal, due 07-10).

## Pitfalls

- Dumping every hit flat, so the one urgent deadline hides in the noise.
- No dedup — the same rule listed three times from three skills.
- Omitting carried-forward actions, letting last week's items vanish.
- Burying a legal-risk item in the body instead of flagging it for counsel.

## Output format

```
REGULATORY DIGEST — week of <date> | matters: <n>
── DECIDE THIS WEEK ──
<item> | docket/RIN | deadline | decision needed | owner
── EFFECTIVE / FINALIZED ──
<rule> | effective date | obligations | owner
── ATTORNEY REVIEW ──
<item> | why (legal risk/ambiguity)
── CARRIED FORWARD ──
<action> | owner | status | due
── MONITORING (no action) ──
<dockets quiet>
```

## Reference

**Rulemaking lifecycle:** the digest spans all stages at once — ANPRM/NPRM signals, open comment windows, final rules, and effective dates. Ordering by lifecycle urgency (closing comment > imminent effective date > early signal) is what makes it actionable.

**Comment-period mechanics:** open windows (~30–60 days) are time-boxed and non-extendable by default, so any period closing within the cadence belongs in "decide this week," not monitoring.

**Policy-diff method:** each digest line is the one-sentence "so what" of an underlying diff — actor, obligation, deadline. Attorney-escalation gate: legal-risk and ambiguous-scope items are surfaced to counsel from the digest, never quietly closed.
