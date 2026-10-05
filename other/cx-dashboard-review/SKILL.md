---
name: cx-dashboard-review
description: Use to audit a CX dashboard for tiles nobody acts on and metrics nobody agrees on — assign an owner per tile, apply kill criteria, and run an actionability test before adding or keeping a chart. Trigger for "clean up the dashboard", "too many metrics", "which KPIs should we keep", dashboard audit, metrics review workshop, "nobody looks at this anymore", or before a BI migration or exec-pack refresh.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Dashboard review

Dashboards rarely fail because they lack data. They fail because **every tile survived
every prior review** — nobody owns removal, and adding a metric is free.

Six months later there are forty charts, three definitions of the same rate, and a
leadership meeting that scrolls for twenty minutes while decisions go unchanged.

This skill audits what stays, what goes, and what must be fixed before it earns a
tile. It complements metric registries and executive reporting: the registry defines
numbers; this process decides which numbers deserve screen space.

## The actionability test

Every tile must pass all five checks. Fail one and it is a candidate for removal,
redesign, or demotion to an appendix — not a default keep.

| Check | Question | Fail signal |
| --- | --- | --- |
| **Owner** | Who is named on the tile and accountable for explaining moves? | "The dashboard team" or blank |
| **Action** | What do they do when it crosses a threshold? | "Monitor" with no threshold or play |
| **Definition** | Is there a registry entry (or equivalent) linked? | Two teams define it differently |
| **Cadence** | How often is it reviewed, and by whom? | Never, or only when someone asks |
| **Denominator** | Is sample size visible or one click away? | Rate alone on a volatile n |

**Pass** — keep, with owner and review date recorded.

**Fix** — worth keeping but missing owner, definition, or denominator; fix within
one sprint or remove until fixed.

**Kill** — fails action and owner; remove or archive.

## Kill criteria

Remove a tile when any of these is true:

- **No action in twelve months** — nobody changed staffing, policy, or priority
  because of it, and nobody can name what they would do if it moved.
- **Duplicate story** — another tile on the same dashboard shows the same lane with
  a clearer definition.
- **Vanity activity** — measures busyness, not customer outcome or sustainable
  efficiency.
- **Permanent "WIP"** — added for a project that ended; kept out of inertia.
- **Unstable definition** — the number changes when the SQL changes and nobody
  versions it; fix the registry first or kill the tile.
- **Unowned alert behaviour** — people only notice it when it turns red, and red
  has no runbook.

Demotion is not failure. A metric can move to an analyst workbook or a monthly
report appendix and serve the operation better without occupying headline space.

## Audit procedure

Work tile by tile. Do not "review the dashboard" as a single vague task.

1. **Inventory** — export tile list: title, data source, creator, last modified,
   linked reports/alerts.
2. **Lane map** — tag each tile: volume/demand, quality/outcome, cost/efficiency,
   or **none** (supporting detail only). More than three headline-class tiles in
   the same lane is a prioritisation problem.
3. **Definition match** — for each rate, find the registry entry or write "missing".
   Flag duplicates and conflicts.
4. **Owner assignment** — one person or team per tile; not a channel.
5. **Actionability test** — pass / fix / kill per tile.
6. **Executive fit** — which tiles qualify for the three-number pack vs operator
   view only.
7. **Removal list** — kills and demotions with rationale; agree who communicates
   to stakeholders who bookmarked removed tiles.

## Owner per tile

An owner is accountable for:

- Explaining period-over-period movement in one team meeting
- Keeping the registry entry current
- Declaring when the tile should be retired
- Ensuring denominator and suppression rules are visible

If no one will take that job, the tile is not owned — and unowned tiles should not
be on a shared dashboard.

Record ownership in the inventory:

```yaml
tile: sla-attainment-inbound
owner: workforce-planning
registry_id: sla-attainment-v2
review_cadence: weekly
threshold: "< 85% triggers intraday staffing review"
status: active
```

## After the audit

- **Headline layer** — at most three tiles (or one composite view) for leadership;
  everything else is drill-down or a separate operator dashboard.
- **Definition blockers** — tiles on "fix" status come down until the registry
  entry exists and consumers are aligned.
- **Review date** — schedule the next audit; dashboards accrete again without one.
- **Change log** — what was removed, why, and where the metric went if anywhere.

Do not add tiles in the same sprint you remove others without running the same
actionability test on the new ones.

## Traps

- **Keeping tiles because someone senior liked them once.** Tenure is not
  actionability.
- **Merging incompatible definitions into one "blended" rate.** Fix definitions;
  do not average confusion.
- **Default filters that change silently.** A tile that "always looked fine" because
  it excluded the hard queue is a definition bug, not a comfort blanket.
- **Colour thresholds nobody agreed on.** Red without a runbook trains ignore.
- **Audit without removal authority.** An inventory that recommends killing twelve
  tiles and kills zero is wasted effort — confirm who can approve removal before
  starting.

## Present results to the user

1. **Tile inventory** — full list with lane, owner, registry link, and status.
2. **Pass / fix / kill table** — every tile classified with one-line rationale.
3. **Definition gaps** — metrics in use without registry entries or with conflicts.
4. **Recommended headline set** — which tiles (if any) belong in executive view.
5. **Removal and demotion plan** — what comes off, what moves to appendix, owners
   to notify.
6. **Next review date** — and the rule for new tiles (actionability test before publish).
