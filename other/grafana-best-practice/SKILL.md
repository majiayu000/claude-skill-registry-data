---
name: grafana-best-practice
description: Review, improve, organize, deploy, and verify Grafana dashboards, provisioned alert rules, and the Telegraf→InfluxDB→Grafana monitoring stack. Use when working on Grafana dashboards, folders, tags, legends, panel readability, Flux/InfluxDB query correctness or performance, Telegraf JSON/HTTP scraping, anonymous access, dashboard/alert provisioning, Grafana Docker deployments, high CPU or memory from dashboard queries, InfluxDB cardinality and tag-vs-field modelling, Flux alert conditions, contact points and Telegram delivery, or requests like "review this dashboard", "optimize Grafana panels", "why is this dashboard slow", "fix legends", "move dashboards into a folder", "set up Grafana alerting", "alert won't fire / won't deliver", "fix Telegram alerts", "route alerts to a Telegram topic (message_thread_id)", "bump the Grafana version", "deploy and verify dashboards", "InfluxDB is OOM-killed / restart-looping", "series cardinality explosion", "should this be a tag or a field", or "Grafana best practices".
---

# Grafana Best Practice

Use this skill to make Grafana dashboards readable, correctly aggregated, navigable, and safely deployable. Treat the rendered dashboard, Grafana API state, datasource query results, and container health as the source of truth.

## Core Workflow

1. Inspect the current dashboard JSON and provisioning files before editing:
   - Dashboard JSON: `uid`, `title`, `tags`, `templating.list`, `links`, `panels`.
   - Provisioning: `provisioning/dashboards/*.yaml`, especially `folder`, provider `path`, and `allowUiUpdates`.
   - Runtime state when available: `/api/search`, `/api/folders`, `/api/dashboards/uid/<uid>`, `/api/ds/query`, `/api/health`.
2. Audit dashboards for:
   - Filters: default values, multi/all behavior, variable labels, and whether All views preserve required dimensions.
   - Aggregation dimensions: each metric's real labels — a per-instance/shard id, per-event labels (e.g. `symbol`, `reason`, `side` in a trading app), `container_name` for containers, and host-level metrics that carry none of these.
   - Legend placement, values, sorting, and display names.
   - Long labels leaking into stat cards or legends, such as `environment`, `project`, `url`, or raw Prometheus family names.
   - Bar chart sorting and limits.
   - Table column headers — no field-wide `defaults.displayName` (it overrides every column); columns renamed via the `organize` transform.
   - Multi-bucket / `union()` queries — every `filter()` pushed inside each `from()` (predicate pushdown), never after `union()`.
   - Query cost: panel count, target count, default time range, refresh interval, high-cardinality tags, expensive reshape operators, and whether current-value panels scan the whole dashboard range.
   - Tag-vs-field modelling on any dimension the dashboard filters or groups by — a churning value used as a tag is a latent datasource outage, not a query-tuning nit (see *Tags Versus Fields*).
   - Anonymous/read-only access if the dashboard is public.
3. Patch dashboard JSON narrowly and preserve existing panel intent. Row nesting differs by state: a collapsed row (`collapsed: true`) holds its child panels in the row's own `panels[]`, but an expanded row (`collapsed: false`) keeps them as TOP-LEVEL siblings after the row object — not nested. A programmatic patch that assumes nesting silently skips every panel under an expanded row; index panels by walking both top-level entries and each row's `panels[]`.
4. Validate locally with JSON parsing, repository tests, and static checks.
5. Validate queries against the real datasource before deployment when possible.
6. Deploy through the repository's normal provisioning path.
7. Verify post-deploy using live Grafana API and datasource query results. Do not rely only on file diffs.
8. Then verify what the page actually RENDERS, because step 7 cannot. Transformations and the
   display processor run client-side, so the API answers a different question than "what does
   the reader see". Open the deployed panel (`/d-solo/<uid>/?panelId=N` isolates one) and read
   its cells out of the DOM. Do this whenever you touched units, transforms, `displayName`,
   value mappings, overrides, or anything that returns more than one frame.

## Hard Rules

These fail SILENTLY — the panel renders, the query returns, the alert stays green, and the
result is wrong. You will not know to go read the reference file, so they live here. Each
points at the file with the worked example.

- **Never make a churning value a tag** (status, "best route", container name on a shared
  host, interface name). It is a latent datasource outage, not a tuning nit — see below.
- **`schema.tagValues()` / `schema.fieldKeys()` do not tell you what is being written now.**
  They read the index and report the old shape after a collector change. Query real points.
- **The InfluxDB Flux datasource IGNORES `legendFormat`.** Series names come from group-key
  labels + `displayName`. A bare `set()` that is not in the group key is not a label.
  → [flux.md](references/flux.md)
- **Never `group()` before a pivot that mixes a string field with numeric ones** —
  `schema collision: column "_value" is both of type string and float`. Pivot first, group
  after. (For an all-numeric pivot the opposite holds: group first, or the rowKey tags stay
  frame labels and pollute every column header.) → [flux.md](references/flux.md),
  [panels.md](references/panels.md)
- **`aggregateWindow(fn: max|mean)` cannot aggregate a string** — use `fn: last`.
- **Aggregators drop every column that is not a group key or the aggregated value.** A column
  built with `map()` before `spread()` vanishes. Map after, or make it a group key.
  → [flux.md](references/flux.md)
- **Push every `filter()` INSIDE each `from()` before `union()`.** A filter after `union()` is
  not pushed down: each branch full-scans the whole bucket into memory and can wedge a shared
  host. → [flux.md](references/flux.md)
- **Never run an unfiltered or heavy ad-hoc Flux query against a shared production
  datasource.** Filter by measurement, keep the range tight, validate with `count()` first.
- **Never set `fieldConfig.defaults.displayName` on a table** — it overrides EVERY column
  header. Rename in the `organize` transform. → [panels.md](references/panels.md)
- **Never set a field-wide `unit` on a table either — it CORRUPTS string columns.** Grafana
  leaves a string alone only when no unit is set (`getDisplayProcessor`:
  `else if (!unit && field.type === string) unit = 'string'`). With one set it runs
  `Number(value)`, and JS parses `0x…` as a HEX LITERAL — an address column rendered
  `2.84027890695473e+22 Sept`. Set units per column via overrides.
  → [panels.md](references/panels.md)
- **`/api/ds/query` CANNOT verify what a panel displays.** Transformations and the display
  processor both run in the BROWSER, so the API returns pre-transform, pre-format data. Every
  server-side check can be green while the page is wrong — read the rendered DOM.
  → [deployment.md](references/deployment.md)
- **`noDataState: OK` turns a broken query into permanent silence** — never fires, never
  errors, never shows NoData. Verify any schema change under such a rule against live data
  before shipping. → [alerting.md](references/alerting.md)
- **Current-value panels must use a bounded window** (`range(start: -15m)` + `last()`), not
  the dashboard picker. → [performance.md](references/performance.md)
- **A committed config fix is not a deployed one**, and the three planes (Grafana image,
  collector bind mount, app) ship by different mechanisms.
  → [deployment.md](references/deployment.md)

## Tags Versus Fields (Cardinality At The Source)

This is a collector-config decision (`telegraf.conf` `tags` vs `included_keys`), not a
dashboard one, but it is the single thing most likely to take the datasource down — so audit
it whenever you touch a dashboard that filters or groups by a status-like dimension.

**series = distinct tag-sets × field keys.** A tag whose value changes for a *fixed entity
over time* — a "churning tag" — multiplies cardinality by every value it has ever taken
inside the retention window. Status flags, a "best route"/"cheapest provider" pick, a
container name on a shared host, a network interface name, a request id: all churn.

Three properties make this worse than an ordinary sizing mistake:

1. **It does not self-heal.** InfluxDB's series file is append-only. Retention expiry drops
   shard *data* but never reclaims series entries, so cardinality only ever goes up until
   someone rebuilds the index.
2. **Uptime hides it.** The cost is paid on shard-index load, i.e. only on a COLD start. A
   container can sit for weeks pegged at 95-100% of its memory cap and look perfectly
   healthy, then fail to boot forever after the first restart — a deploy, a host reboot, one
   heavy query. Cold-start capacity is not exercised by uptime; nothing warns you.
3. **The estimate in the comment is probably wrong.** Measured example (2026-08): a comment
   claiming "20-25k series worst case" sat above a measurement holding **166,773** — 7× off,
   and that staleness is why nobody looked. Another: six route-venue tags added on the belief
   that "cardinality is bounded by asset × a small venue-pair" minted **897,212 dead series,
   79% of the whole bucket**, and the resulting boot loop was a full outage.

Rules:

- Keep as tags only what genuinely identifies the entity (venue, asset, instance,
  container_name for containers). Put churning values in `included_keys` as string **fields**
  and pivot them back in at query time.
- State the arithmetic (rows × field keys) BEFORE changing a tag set, and re-measure AFTER
  deploying. Against a **stopped** instance:
  `influxd inspect report-db --db-path <data>/<bucket-id> --rollup m`. Every cardinality
  comment must carry a measured number and its date.
- Demoting a tag is a COORDINATED change — collector config, every dashboard panel that
  filters/groups on it, every alert rule, and the downsample task's string guard all move in
  one commit. A partial change breaks silently, not loudly.
- Never trust `schema.tagValues()` / `schema.fieldKeys()` to tell you what is being written
  NOW. They read the index, which still lists every tag value and field key whose series
  exists in an overlapping shard, so right after a collector change they report the OLD shape
  for the new window — a `-3m` query can return 30 days of dead values. To answer "what is
  actually landing", query real points:
  `range(start: -90s) |> filter(...) |> keep(columns: ["<tag>"]) |> group() |> distinct(column: "<tag>")`.

## Folder And Tag Rules

Prefer a named Grafana folder when permissions are known to be handled. For provisioned Grafana OSS dashboards with anonymous access, verify folder permissions explicitly because named folders can 403 even when dashboards exist.

Safe folder checklist:

- `provisioning/dashboards/default.yaml` uses the intended folder, for example `folder: Production`.
- Startup or deployment code grants Viewer read on every provisioned folder and dashboard when Grafana state is ephemeral.
- `/api/folders` shows the folder.
- `/api/search?type=dash-db&tag=<base-tag>` shows every dashboard with the expected `folderTitle`.
- Anonymous probes return `200` for both `/d/<uid>/...` and `/dashboards`.

Use one stable base tag for dashboard links and discovery, then add semantic tags. Keep tags low-cardinality and queryable.

Recommended tag shape — one stable base tag (the service slug) plus semantic axes. The values below are an illustrative set; substitute your own facets:

```text
<service>                     # stable base tag, e.g. `myservice`
area:<facet>                  # e.g. area:overview | area:app | area:risk | area:infra
audience:<role>               # e.g. audience:operator | audience:oncall
plane:<data-plane>            # e.g. plane:prometheus | plane:app | plane:host
```

Keep dashboard dropdown links on the stable base tag (the service slug, e.g. `myservice`) so adding semantic tags does not break navigation.

## Variables And Filters

Use explicit labels that explain important defaults:

```json
{
  "name": "instance",
  "label": "Instance (All by default)",
  "multi": true,
  "includeAll": true,
  "allValue": ".*"
}
```

For high-level fleet dashboards, defaulting `instance` to All is good only if every panel handles All safely. When All is selected:

- Stat panels should either show one compact value per instance or deliberately aggregate fleet-wide.
- Time series panels should not collapse multiple instances into one unlabeled series.
- Legends and display names should stay short.

## Detailed References

Load the file that matches what you are doing:

- **Writing or fixing a Flux query** — dimension handling, series naming, hidden-cardinality
  collapse, ratio math, reading a string field back, dual-bucket `union()` and downsampling:
  [references/flux.md](references/flux.md)
- **Reviewing or improving a dashboard's readability** — information architecture, the
  answer-first summary row, and stat / timeseries / bar / table panel rules:
  [references/panels.md](references/panels.md)
- **Something is slow, timing out, or pegging the datasource** — query-surface audit, bounded
  lookbacks, cheaper producer-side fields, and how to prove a performance fix:
  [references/performance.md](references/performance.md)
- **Alert rules, contact points, notification delivery** — Flux alert conditions and reducer
  errors, `noDataState` choice, Telegram chat_id / supergroup / topic `message_thread_id`,
  parse-mode escaping, message-template composition (group-label-in-header DRY, no-text-color
  emphasis, resolved-only context), live rule-health and real delivery verification:
  [references/alerting.md](references/alerting.md)
- **Deploying, verifying, upgrading, or recovering the stack** — provisioning paths, folder
  permissions, Grafana major-version bumps, the minimum post-deploy verification curls,
  compose + Telegraf monitoring-stack gotchas, and the InfluxDB OOM boot-loop recovery
  runbook: [references/deployment.md](references/deployment.md)

## Review Output

When reviewing or finishing work, report evidence, not just intent:

- Files changed.
- Dashboard count and panel query count verified.
- Folder and tag API evidence.
- Anonymous access probes.
- Datasource query result summary. After any schema-shaped change (a tag demoted, a
  measurement/field renamed, a bucket purged), extract EVERY panel target from the deployed
  dashboards, substitute the Grafana variables, and execute them all against the datasource —
  not just the ones you edited. It is cheap, it is scriptable, and it is the only thing that
  catches a panel you did not realise depended on the old shape. Report the tally
  (e.g. "70 queries: 69 returned data, 0 errors, 1 empty") and explain every empty one; an
  empty result is only acceptable once you have shown the query is sound by loosening its
  filter to a value that does exist.
- Cardinality before/after when a tag set changed, measured (not estimated) with
  `influxd inspect report-db`, plus proof the new shape is what is actually landing (a
  `distinct()` over real points from the last 90s — NOT `schema.tagValues()`).
- Query performance evidence when performance changed: target count, expensive
  operators removed, bounded time windows added, old/new query result or timing
  comparison, and live dashboard JSON proof after deploy.
- First-viewport summary row evidence for operational dashboards: key stat
  cards render, use range-correct semantics, and are not blank when expected
  data exists.
- **Rendered-cell evidence whenever formatting, transforms or frame count changed** — the
  actual DOM text of the affected panel, quoted. "The datasource returns the right value" is
  not evidence that the panel shows it; those are different layers and only the second one is
  what the reader gets. A before/after pair is best: it is the only thing that distinguishes
  a fixed panel from one whose bug you never saw.
- Alert rule health (`/api/.../rules` all `ok`) and a real delivery test, when alerting changed.
- Container/service health.
- Any risks intentionally left unchanged.

If a validation failure appears, fix the dashboard and rerun the relevant static, API, and datasource checks before declaring completion.
