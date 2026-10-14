---
name: table-drill-down
type: Skill
title: "Table drill-down — group, break out, and land on a page about the value"
description: "Drill-down on the shared MatrxDataTable, local or server, with per-Dimension levels. Use when adding group-by, breakdown or 'by X' analytics to a table, replacing hand-built totals or rollup tables, or when people want counts or sums by status, owner, model or day."
tags: [tables, ui, drill-down, analytics]
timestamp: 2026-10-07
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/table-drill-down/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# Table drill-down

A drill-down is a table about the thing you clicked, not a list of groups. Usage by user, click a
user, and you land on that user (header of facts and totals, one-click "By provider / agent /
conversation / day" chips); group by conversation and you see title, agent, started, last activity,
cost, calls, tokens. That second half is **levels**. API detail (needs `@ai-matrx/design-system`
>= 0.79.4) lives in `aidream/apps/shared/design-system/README.md` sections "Drill-down" and "How to
declare levels" (and its selector list); state and rules in
`common-docs/systems/data/drill-down/STATE.md`. Do not copy them here or into the page.

## 1. Add it, or not

- **Add** when the table has a few groupable columns (status, owner, model, a date) and number columns
  (amount, cost, count), or when the page hand-builds totals or rollup tables. The drill replaces them.
- **Do not add** to config editors, work queues, spreadsheet-style editors, or tiny tables.
- **Before absorbing a hand-built rollup, run the no-loss checklist**: its links, selection, scope
  panels, prior-window compare, zero-row behavior, special states. Each one is adopted into the
  primitive or the rollup stays. Never drop one silently.

## 2. Local or server (decide on completeness, not on convenience)

Local only if the list is **complete**. It is partial if any of these holds: it reached its fetch cap,
it is server-paged, a known total is larger than the rows held, or an API silently truncates. Check the
source's own cap and the true count (read-only SQL: `pnpm admin-query` in matrx-frontend). Then:

| The table holds | Use |
|---|---|
| Every row of its source, under 50,000 | **Local**: `drill={{ local: true }}` |
| Partial in any way above, or over 50,000 rows | **Server**: a declared `*.drill.ts` |

The table refuses in words ("List capped at 200: group on the server."). Never silence it by passing
`source`/`coverage` to make it look complete: pass them **honestly** (`source: { total }`,
`{ paged: true }`, `{ cap }`). `coverage.loaded` is inferred; do not set it.

A rollup the server computes (medians, rates, anything not a sum of the rows held) cannot be rebuilt
locally: it is a server definition. A server definition needs SQL (campaign file, clone rehearsal,
owner apply), so it is a planned piece of work, never a cheap fallback to keep the page moving.

## 3. Local, then levels

```tsx
<MatrxDataTable data={jobs} columns={columns} getRowId={(j) => j.id} drill={{ local: true }} />
```

Dimensions and Measures are inferred from `columns`. Rules the inference follows:

- An inferred Measure takes its column's `format` (money, duration, percent). `extraMeasures` is only
  for a new label or op.
- A column not on the row needs an accessor or it vanishes; the dev warning names it.
- **Nulls**: a Measure over blanks says what it means with `nulls: "unknown"` (the group reads
  Unknown) or `"count"` (the known part, then "N unknown"). Never silently sum the known values where
  the old page said "not available".

Then declare **levels** keyed by Dimension, for each Dimension someone will drill into:

- **`breakouts`**: the questions asked next about one value, most useful first, time last
  (`"due:month"`). A sibling definition's Dimension is `def:dim` (cross-definition).
- **`show`**: the numbers that matter for that thing, in reading order.
- **`attributes`**: facts constant inside the value's group (a user's organization). Never a per-row
  number. `attributes: []` suppresses the inferred ones.
- **`hide`**: keys never offered (Dimension, Measure or column).
- **`records`** (server): the columns "See these records" shows.

Worked local example (jobs by owner and client):

```tsx
drill={{ local: true, levels: {
  owner:  { breakouts: ["client", "project", "status", "due:month"], attributes: ["team"], show: ["count", "sum_amount"] },
  client: { breakouts: ["owner", "status", "due:month"], attributes: ["industry"] },
} }}
```

Dropped items (a level naming a non-Dimension) warn once in dev. Test levels instead of eyeballing:
`drillLevelProblems` and `drillDroppedItems` return the same findings for a unit test.

## 4. Server

1. Write `aidream/apps/shared/records/scripts/drill-definitions/<key>.drill.ts`, copying
   `ai_usage.drill.ts`: source, lanes (every lane gets a rule), Dimensions with `level`, Measures,
   `records`.
2. `pnpm drill:sync --write --lane <LANE>` (in `apps/shared/records`) writes the campaign migration;
   apply it the way DB changes are applied in this workspace (never hand-edit the generated
   `platform.drill_def__<key>()`).
3. `pnpm drill:sync` with no flag fails when a declaration and the live body differ or a definition is
   unsound. It must pass.
4. Mount `DrillExplorer` (matrx-frontend `components/official/drill-explorer/`, read its FEATURE.md)
   or `useDrill` in a records grid. Never a second explorer screen.

Worked server example, Arman's usage (usage, then a person, then "by conversation", then the
conversation level showing title, agent, started, last activity, duration, cost, calls, tokens):

```ts
{ key: "person", ..., level: { breakouts: ["provider", "model", "agent", "feature", "conversation", "at:day"], attributes: ["organization"] } },
{ key: "conversation", ..., level: { breakouts: ["request", "model", "at:hour"], attributes: ["agent", "person"],
  show: ["cost", "calls", "tokens_in", "tokens_out", "started", "last_activity", "duration"] } },
```

A level whose list equals the default has not been designed.

## 5. Verify

- **Link with the question in the address**: your page with `?drill.by=<dimension>` (it carries the
  level's `show`), or the playground `http://127.0.0.1:3026/?scenario=drill-level-owner` (`pnpm demo`;
  also `drill-level-breakout`, `drill-level-attributes`, `drill-partial`, `drill-ceiling`). Walk it as
  a user: group, click a value, read the header, click a chip.
- Stable selectors for a walk: `data-matrx-drill-group`, `-into`, `-breakout`, `-see-records`,
  `-focus-total`, `-focus-attribute`, `-crumb`, `-failed`, `-unknown` (full list in the README).
- Preview parking: `/__dev-walk?parked=1` keeps the walk off the user's screen.
- Check every number against a hand count or read-only SQL on the same rows. A drill that looks right
  and is not counted is worse than none.
- Look at it at 390 px wide. Real data only.

## 6. Anti-patterns

- A hand-built group table or totals strip beside the table.
- `local: true` on capped, paged or partial data, or `source`/`coverage` passed to dodge the refusal.
- Summing known values where blanks mean "unknown".
- Every level showing the same columns (levels not declared).
- Styling the table from the host (`className`, arbitrary variants). A missing option is added in
  `@ai-matrx/design-system`, released and adopted (canonical-table-usage rule 7).
- A per-row measure listed as an `attribute`, or an id column offered as a Dimension.
- A second explorer or a one-off chart instead of `DrillExplorer` / `MatrxDrillChart`.
