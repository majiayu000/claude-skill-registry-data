---
name: data-analytics
description: >
  Use to understand the data an application houses and to identify high-value
  metrics, KPIs, and charts worth surfacing — the groundwork for dashboards.
  Invoke whenever exploring a schema/domain, planning analytics or a dashboard
  for an app section ("what should this dashboard show?", "what metrics matter
  here?", "add stats/charts to X"), or deciding which data points matter. Builds
  a per-project catalog of entities, relationships, and candidate visualizations.
  This skill decides WHAT to measure and WHY — for making the backing queries
  fast use database-optimization; for building the chart/table UI use frontend
  (+ tabler-ui); for chart colors/visual styling use design-guide; for which
  dashboard a metric belongs on and the order the sections read in use
  information-architecture.
---

# Data Analytics

Goal: build understanding of an app's data and propose the metrics/charts that would be
genuinely useful — decision-driving, validated against real data — before any dashboard
is built. The same method applies to any project.

## Workflow

Work the steps in order. The ordering is the point: metrics proposed before the domain is
understood, or shipped before the data is validated, are the two ways this work fails.

### Step 1 — inventory the schema/domain

Check `LEARNINGS.md` beside this skill, when your copy keeps one, first — a catalog for
this project may already exist; extend it rather than re-deriving it. (This install's
catalogued projects: `LOCAL.md` beside this skill, when your copy keeps one — *Existing
catalogs*.)

- Identify the core entities, their tables/schemas, key columns, and the relationships
  (ownership, foreign keys, join/lookup tables, existing views/read models — pre-joined
  views are usually the best dashboard sources).
- Note the identity model (which id is canonical, how legacy/new ids map) — some apps
  key much of their data on a *legacy* user id via an auth-bridge table; confirm which
  id is canonical before building on it (this install's example: `LOCAL.md` beside this
  skill, when your copy keeps one — *Identity model example*).
- Note rough volumes and freshness (row counts, min/max of timestamp columns) — they
  determine whether a metric needs a rollup layer or can query the operational tables.

### Step 2 — find the lifecycles and the business questions

- Most value lives in **state over time**: funnels, status transitions,
  created→completed timestamps. Locate the state machines and timestamp columns.
- Write down the questions the business actually asks of this data, per audience
  (internal admin vs partner vs end user) — a metric that answers no one's question is a
  vanity count. If the audience's questions aren't obvious, ask the user now (front-load;
  don't guess mid-build).

### Step 3 — propose metrics, ranked by usefulness

For each candidate metric, state all four (a metric missing any of these isn't proposable
yet):

1. **The question it answers** and for whom (audience → also sets data-scoping/auth).
2. **The chart type it deserves:** trend over time → line; funnel/stage conversion →
   funnel; categorical comparison → bar; current snapshot of one number → single stat;
   detail/ranking → table; distribution → histogram. Don't default everything to a stat
   card row.
3. **The grain** (per user / partner / location / day) and roughly the query shape.
4. **The source** (table/view/columns) — including whether the data is internal or needs
   an external integration (recalls, maintenance schedules, etc.).

Prefer a few decision-driving metrics over a wall of counts.

### Step 4 — validate against real data (hard gate)

Before any metric is presented as buildable, run the candidate queries against a real
database (local restore, staging):

- Do the columns actually exist, with the assumed types/values?
- Is the data **populated** — non-null, non-empty, covering the time range the chart
  implies? A column that exists but is 2% populated makes a chart that lies.
- Is the data **current**? A dev snapshot's empty/stale table proves nothing about prod
  (same trap as the code-quality "don't infer dead from stale data" rule) — check
  max(timestamp) against today before concluding either "no data" or "we have this".
- Spot-check that the numbers are plausible (compare a count against a known figure).

Mark each proposed metric: **validated** / **data gap** (what's missing) / **needs
external source**.

### Step 5 — map to UI and record the catalog

- Tie each surviving metric to the screen/section that would host it and its audience —
  which also sets the scoping/auth (e.g. partner admins see only their `partner_id`).
- Flag where a rollup/materialized layer is warranted before heavy dashboarding (big
  scans on operational tables) — hand the query-tuning itself to database-optimization.
- Record the entity catalog, lifecycles, validated metrics, and gaps in `LEARNINGS.md`
  beside this skill, when your copy keeps one — the catalog is the deliverable that
  outlives the session.

## Common failure modes

- **Dashboard-first:** picking charts before understanding entities/lifecycles produces
  pretty vanity counts. Steps 1–2 come first, always.
- **Proposing metrics on empty/stale/unpopulated columns** — the schema says the column
  exists; only Step 4 says it has usable data. This is the most common way an analytics
  plan dies in review.
- **Ignoring the audience/scoping** — a metric without a "who sees this" has no auth
  model and no home screen; it isn't shippable.
- **Wall-of-stats syndrome** — 20 single-stat cards instead of 5 metrics that drive a
  decision. Rank and cut.
- **Treating estimate/cost data as actuals** — e.g. labor-time guides are legally
  "guide only"; present derived cost figures as non-binding ranges (see LEARNINGS).
- **Skipping the existing catalog** — re-deriving a domain that LEARNINGS already maps
  wastes the session and loses the recorded scoping rules.

## Before you call this done

- [ ] Read (and extended, not duplicated) the project's LEARNINGS catalog.
- [ ] Every proposed metric names its question, audience, chart type, grain, and source.
- [ ] Every metric is marked validated / data-gap / needs-external-source, from queries
      run against real data — not schema-reading alone.
- [ ] Data gaps and rollup-layer needs are flagged explicitly.
- [ ] The catalog updates are written to LEARNINGS.md.

## Capturing learnings (session-handoff protocol)

Accumulate per-project data knowledge in `LEARNINGS.md` beside this skill, when your
copy keeps one. On handoff / "update skills" / after data work: record the entity
catalog, ownership/scoping rules, useful timestamp/state columns, the candidate
metrics/charts identified (with their validation status), and known data gaps. Dedupe/merge, tag by project, and read it before
analytics work on a matching app.
