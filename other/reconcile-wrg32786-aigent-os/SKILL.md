---
name: reconcile
agent: none
description: Read-only attention reconciliation. Computes actual seven-day project attention from daily notes against explicit Tier-1 intended shares.
allowed-tools: Read, Bash
user-invocable: true
status: PRODUCTION - deterministic and read-only
triggers:
  - reconcile
  - attention drift
  - cross-system check
  - consistency check
---

# /reconcile - attention reconciliation

This measurement leg reports attention drift. It never edits priorities, daily
notes, goals, or runtime state.

Run:

```text
node daemons/nightly-reconcile.mjs --root <aigent-root> --as-of <fire-date>
```
Use literal output and exit status as the checkpoint evidence.

## Required intended-share input

Read `vault/memory/ACTIVE_PRIORITIES.md` and locate explicit Tier-1 projects
with intended percentages. Accepted forms:

```markdown
| Tier | Project | Intended share |
| 1 | [[Project Name]] | 40% |
```

or:

```text
Tier 1 - [[Project Name]] - intended 40%
```

Shares are integers from 1 through 100 and the Tier-1 total must be at most
100. Names or aliases must resolve to a project note or an explicit canonical
name in the priorities file.

No intended shares returns nonzero:

```text
RECONCILE FAIL reason=intended-share-input-absent projects=0
```

This is a configuration failure, never permission to invent shares.

## Seven-day measurement

1. Select valid `vault/daily/YYYY-MM-DD.md` notes inside the exact calendar
   window `as_of-6d .. as_of`. A missing day contributes no mentions.
2. Per project and note, count at most:
   - 3 points for a heading or heading wikilink;
   - 2 points for a body wikilink to a canonical note or alias;
   - 1 point for an exact plain-text name.
3. One occurrence receives only its highest applicable weight.
4. Track project references outside Tier 1 as non-Tier-1 attention.
5. Compute `actual = project points / all project points * 100`, rounded to one
   decimal.

A zero denominator returns
`RECONCILE FAIL reason=no-measurable-project-attention`.

## Drift predicates

- Tier-1 drift: `actual < 0.40 * intended`.
- Combined non-Tier-1 drift: actual share over 25 percent.

Output raw points, actual share, intended share, thresholds, drift decisions,
and source paths so the arithmetic is reproducible:

```text
RECONCILE PASS window=YYYY-MM-DD..YYYY-MM-DD notes=<N>
project=<name> points=<N> actual=<N.N>% intended=<N>% threshold=<N.N>% drift=<yes|no>
non_tier_1 points=<N> actual=<N.N>% drift=<yes|no>
```

Missing notes, shares, measurable attention, or parseable dates are not green.
