---
name: creo-perf
description: >
  Full-stack performance optimization with measured proof. Six-layer audit
  (database, API, edge proxy, client data layer, rendering, browser resources),
  immutable labeled baselines, deterministic before/after captures via the
  perf-harness extension (EXPLAIN medians, p50/p95 loops, wire bytes, ETag replay,
  Lighthouse, Playwright interaction probes, pg_stat_statements discovery), an
  auto-built dashboard, and a one-concern-per-commit fix loop. /creo perf init
  scaffolds everything for a project. Trigger keywords: performance, slow page,
  latency, benchmark, baseline, EXPLAIN, query plan, index, N+1, bundle size,
  Lighthouse, Core Web Vitals, p95, payload, compression, ETag, profiling.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
  - Edit
  - WebFetch
  - Agent
---

# creo-perf — performance optimization with proof

No performance claim without a number. Baseline before touching code, an
identical re-measure after, one concern per commit, correctness checked on
every pair. The harness makes the numbers deterministic; this skill makes the
workflow non-negotiable.

## Commands

| Command | What it does |
|---------|--------------|
| `/creo perf init` | Scaffold `.claude/skills/creo-perf/` for this project, detect the stack, fill targets, propose scenarios from the route code, write SQL sources, verify with preflight. **Run first.** |
| `/creo perf preflight` | Tools, targets, DB, scenarios, SQL mode — everything a capture needs |
| `/creo perf baseline [label]` | Full sweep under one immutable label (default `before`): platform, schema, every scenario, fe, workload |
| `/creo perf audit [baseline\|after\|discover]` | Spawn `creo-perf-audit` (measure-only) for a severity-ranked findings report over the six layers |
| `/creo perf optimize [scenario or finding]` | The fix loop: pick a finding, implement one concern, re-measure, verify correctness, commit |
| `/creo perf scenario <id> <label>` | Re-capture one scenario |
| `/creo perf fe <label>` | Initial-load / build / Lighthouse capture |
| `/creo perf platform <label>` / `schema <label>` | Config-fact captures (context, not before/after metrics) |
| `/creo perf workload <label>` | Discovery window: pg_stat_statements ranking under scripted traffic |
| `/creo perf after <label> [ids...]` | Re-measure the scenarios a landed fix touches (default: all) and show deltas |
| `/creo perf dashboard` | Rebuild `results/dashboard.md` |
| `/creo perf report` | Write the per-finding SOLUTION entries (bottleneck, proof, fix, before/after) from the dashboard |
| `/creo perf observability [--teardown]` | Enable (or revert) pg_stat_statements + auto_explain + hypopg |

## Harness resolution

The scripts live in the `perf-harness` extension. Resolve `PERF_HARNESS` as
the first existing of:

1. `${CLAUDE_PLUGIN_ROOT}/extensions/perf-harness` (plugin install)
2. `~/.claude/skills/creo-perf-harness` (`extensions/perf-harness/install.sh`)
3. `<creo checkout>/extensions/perf-harness`

After init, the project wrapper `.claude/skills/creo-perf/perf <cmd> [args]`
resolves it automatically; prefer the wrapper in every Bash call below. If no
harness is found, say so and offer the manual protocol from
`references/measurement-protocol.md` — never fabricate numbers.

## Configuration

1. Read `.claude/project-config.md` (`project_id`, `dev_server_url`, stack).
2. Load the project extension `.claude/skills/creo-perf/creo-perf-{project_id}.md`
   — targets, scenarios, hot-path map, hazards, environment log, findings
   ledger. It is authoritative; consult it before any work.
3. `perf.config.sh` in the same directory is the machine-readable twin the
   scripts read. Keep the two in sync (init writes both; fixes update both).
4. If the extension is missing, run `/creo perf init` before anything else.

## `/creo perf init` — prepare a project

Goal: after init, `perf audit-all before` runs end to end without edits.

1. **Scaffold**: `"$PERF_HARNESS/scripts/init-project.sh" [--project-id X]`
   (copies templates, writes the `perf` wrapper, appends `.gitignore`).
2. **Detect the stack** (read, do not guess): package managers, `docker-compose*`,
   Dockerfiles, nginx/Caddy configs, backend framework and ORM, frontend
   bundler, DB engine and connection details, container names, ports.
   Record the port map and which port bypasses the proxy.
3. **Fill `perf.config.sh`**: `PERF_API`, `PERF_PROXY` (empty if no proxy),
   `PERF_WEB`, `PERF_PSQL_CMD` (array), containers, `PERF_DB_TABLES` /
   `PERF_DB_HOT_TABLE`, app/backend dirs, build command, `PERF_BACKEND_KIND`,
   `PERF_SQL_MODE` (`record` for SQLAlchemy/SQLModel apps with a venv, else
   `compile`), `PERF_ALL_ORDER`, hazards. Verify every URL with curl.
4. **Propose scenarios** from the hot path: read the route handlers the
   problem statement points at, list the user-facing interactions (default
   page load, search, each filter, sort, pagination variants, heavy endpoints
   such as tiles/exports), and write one `scenarios/<id>.sh` each using
   `scenarios/.template.sh`. URLs come from the API docs or the handler
   signature — never invented. Put the unbounded / cache-churning variants in
   the scenario that runs last. Follow `references/scenario-spec.md`.
5. **SQL sources**: record mode — fill `sql-calls.py` with one `call(...)` per
   scenario mirroring the URLs; compile mode — write `sql-src/<runner>/<label>.sql`
   with the statement each handler executes (binds inlined), `.rows.sql` for
   row-returning statements. Note which is which in the extension doc.
6. **FE probes**: fill `fe-interactions.json` with one entry per interaction
   scenario (selectors read from the component source; `rows` = the rendered
   row selector). Check Playwright resolves from `PERF_APP_DIR`; if not, say
   the FE rows will read "unavailable" until it is installed.
7. **Dashboard config**: `dashboard.json` order, titles, `endpoint -> handler
   file:line` per scenario.
8. **Write the extension doc** `creo-perf-{project_id}.md` from the template:
   stack table, targets, scenario table, hot-path map with `file:line`,
   hazards (large files never to open, destructive commands, port collisions,
   missing env vars), empty environment log and findings ledger.
9. **Verify**: `perf preflight` must pass; then run ONE cheap scenario under a
   throwaway label (`perf audit-scenario <id> init-check --runs 3`), read its
   metrics file, fix whatever is empty or wrong, delete the throwaway dir.
10. Summarize what was configured and what stays manual (browser-only
    layers, stacks without a platform probe).

Ask the user only for facts that cannot be read from the repo (credentials
not in compose files, which page is the complaint about, a proxy that only
exists in production).

## Measurement rules (non-negotiable)

- Baseline BEFORE any code change. A label directory is immutable once
  written; `before` is never re-run after a fix lands. New label per
  re-measure (`after-<what>`); `--force` only on non-baseline captures.
- Only script-to-script pairs are comparable. Never derive an ad-hoc number
  for a before/after claim.
- Identical scenario, environment and commands on both sides; label every
  number (direct vs proxy, warm vs cold, prod vs dev build, docker vs local).
- Median of >= 3 warm runs plus the first cold hit; never a single run, never
  averages that hide tails.
- Never run two captures concurrently. Respect `PERF_ALL_ORDER`.
- Correctness rides along: row counts, filter results, ETag/304 behavior must
  match before vs after — drift is a regression, not a win.
- Never `ANALYZE` mid-audit; planner-stats state is itself an observation.
- A config value is never evidence; prove a config change by re-running a
  scenario and diffing its plan/latency.
- Environment changes (observability enablement, container restarts) go in
  the extension doc's environment log with the capture that validated them.

Full protocol: `references/measurement-protocol.md`.

## `/creo perf baseline`

1. Preflight. Confirm the stack is the production-shaped one (proxy in front,
   prod build served) — a dev server baseline is invalid for proxy/bundle work.
2. `perf audit-all <label>` (default `before`). Runtime 15-30 min; do not run
   anything else against the stack meanwhile.
3. Verify the run ended with `dashboard: .../results/dashboard.md` and that
   every scenario has a column. Read each `<id>-metrics.md`; any `n/a`,
   `missing`, or `unavailable` cell is fixed now (scenario file, SQL source,
   Playwright) and that scenario re-captured under the same label with
   `--force` — the baseline is still pre-fix, so this is legitimate.
4. Commit `results/dashboard.md` and the project extension.

## `/creo perf audit`

Spawn `creo-perf-audit` via the Agent tool with `context: fork`, passing the
mode (`baseline` | `after` | `discover`), the label(s), and the scope (which
page / flow). It measures and ranks; it never edits application code. Relay
its findings ranked by severity with the evidence index. Do not re-run the
harness yourself while it is running.

## `/creo perf optimize` — the fix loop

One finding at a time, top severity first unless the user picks one.

1. **Read the evidence**: the finding's scenario metrics and the decisive plan
   or trace lines. Attribute the cost to one layer with that layer's
   profiler; do not claim a cause measured at another layer.
2. **Design the smallest fix** at that layer. Prefer: unindexable predicate ->
   sargable rewrite + index; duplicate aggregates -> one query; oversized
   payload -> trim to what the UI reads; missing compression / caching headers
   at the edge; refetch storms -> query-client config; blank-on-refetch ->
   placeholder data; eager heavy libs -> route-level lazy boundaries;
   per-row render work -> virtualization. See `references/layer-audit-checklists.md`.
3. **Implement one concern**. Keep the harness aligned: if the fix changes a
   query shape, update `sql-calls.py` / `sql-src` and the scenario's expected
   sections in the same change so the after-capture measures the real thing.
4. **Re-measure**: `perf audit-scenario <id> after-<what>` for every scenario
   the fix touches (fe for bundle/edge work; platform/schema when config or
   indexes changed). Never re-run `before`.
5. **Verify**: dashboard delta on the headline metric; correctness refs
   identical; no other scenario regressed (re-capture a neighbor if the fix
   could affect it). A regression or drift blocks the commit.
6. **Record**: append a row to the findings ledger in the extension doc
   (scenario, layer, bottleneck, fix, before -> after, commit); update the
   hot-path map if files moved.
7. **Commit** one concern: `perf(<layer>): <what> — <headline before -> after>`,
   body with the decisive evidence and the labels compared. Include the
   updated `dashboard.md` and harness config in the same commit.
8. Repeat. Stop when remaining findings are Low or the user's target is met.

## `/creo perf report`

Produce the deliverable write-up (SOLUTION.md-style) per finding:
bottleneck -> profiling proof (plan/trace excerpt, numbers, labels) -> fix
(files, mechanism) -> before/after table from the dashboard -> commit. Use
`references/report-templates.md`. Numbers are copied from
`results/dashboard.md`, never retyped from memory.

## Layers

| # | Layer | Proof tool | Harness capture |
|---|---|---|---|
| 1 | Database | EXPLAIN (ANALYZE, BUFFERS), pg_stat_statements, hypopg | scenario DB rows, schema, workload |
| 2 | API shape | queries/request, payload composition, p50/p95 direct | scenario API rows, platform |
| 3 | Edge / proxy | compression on the wire, time-to-304, cache headers | scenario Network rows, fe assets |
| 4 | Client data layer | refetch counts, blank-on-refetch, waterfall | fe-interactions probe |
| 5 | Rendering | long tasks, commit counts, virtualization | fe-interactions probe, Lighthouse TBT |
| 6 | Browser resources | bundle composition, lazy boundaries, lifecycle leaks | fe build/composition rows |

Checklists per layer: `references/layer-audit-checklists.md`. Top-down
triage, bottom-up proof.

## Reference files

| File | When to load |
|---|---|
| `references/measurement-protocol.md` | Any capture, any before/after claim, the manual fallback |
| `references/scenario-spec.md` | Writing or editing `scenarios/*.sh`, SQL sources, FE probes, dashboard config |
| `references/layer-audit-checklists.md` | Auditing or fixing a specific layer |
| `references/platform-audit.md` | Interpreting platform/schema facts; stacks without an automated probe |
| `references/report-templates.md` | Metrics row grammar, dashboard reading, SOLUTION entries, commit messages |
| `references/project-extension-template.md` | What `creo-perf-{project_id}.md` must contain |

## Quality gates

- Every claim in a report maps to a dashboard cell or an archived raw file.
- Before/after pairs share scenario, environment, and script version.
- Correctness references identical across the pair.
- Findings ledger and dashboard committed with each perf commit.
- No emojis in generated files; kebab-case scenario ids; stable metric names.
