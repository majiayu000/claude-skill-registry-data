---
name: build-dashboard
description: Build or improve a Coval dashboard with metric visualizations backed by real data. Creates new dashboards from scratch or rebuilds existing ones by analyzing usage patterns, metric frequency, and data density. Use when user says "create a dashboard", "build a dashboard", "improve my dashboard", "add widgets", "visualize my metrics", "make a performance dashboard", or "dashboard for my runs".
argument-hint: "[dashboard-purpose-or-name]"
---

# Build Coval Dashboard

Build a data-driven dashboard for `$ARGUMENTS`. This skill analyzes the user's existing runs and metrics to create a dashboard populated with real data — never an empty shell.

## Phase 0: Preflight + Usage Analysis

### Step 1: Check authentication

```bash
coval whoami
```

If not authenticated, guide the user:
```bash
coval login
```
This prompts for an API key. Get one at https://app.coval.dev/settings (Organization > Manage > API Keys).

If the user doesn't have a Coval account, direct them to https://coval.dev to sign up.

### Step 2: Inventory resources

Run these in parallel:

```bash
coval dashboards list --format json
coval metrics list --include-builtin --format json
coval agents list --format json
coval runs list --format json --page-size 50
```

**Always ask first:** "Would you like to **create a new dashboard** or **improve an existing one**?"

If they choose **improve existing**:
- List existing dashboards as a numbered list with names and widget counts
- Ask which dashboard to improve
- Fetch that dashboard's widgets: `coval dashboards widgets list <dashboard_id> --format json`
- Analyze what's already there: which metrics are visualized, what viz types are used, what's missing
- **Improving means REBUILDING the dashboard** — delete ALL existing widgets and recreate from scratch with the full metric set and correct viz types. Do NOT just append more widgets to the bottom. The dashboard should look cohesive, not like layers of additions.
- To delete existing widgets: `coval dashboards widgets delete <dashboard_id> <widget_id>`
- Check if any metrics have **no data yet** (newly created metrics that haven't been run in the last 7 days). To check: look at the metric frequency analysis — any metric with 0 appearances has no data.
- **If metrics have no data, STOP and run evals first.** Do NOT build a dashboard with empty widgets. Tell the user:
  > "<metric name> has no data yet. I need to run an evaluation with this metric first so the dashboard has something to show."
- Then invoke `/quick-eval` with the new metrics attached to the agent. Wait for completion. Only then proceed to rebuild.
- **There is no "skip and build anyway" path.** Empty charts are useless — same principle as the no-data gate.
- Then proceed to Phase 1 to plan the new layout from scratch, incorporating all metrics (old + new)

If they choose **create new** or there are no existing dashboards:
- Proceed to Phase 0 Step 3 as normal

### Step 3: Analyze usage patterns

**This is the critical intelligence step.** Determine the data source automatically:

1. **Count runs by type**: Check each run for the presence of `test_set_id`.
   - Runs **with** `test_set_id` → Simulation runs (evaluation test runs)
   - Runs **without** `test_set_id` → Monitoring runs (live conversation submissions)
   - Note: Some runs may also have an `is_monitoring` field, but the primary signal is `test_set_id` presence.

2. **Decision logic** (do NOT ask the user unless ambiguous):
   - Mostly simulation runs → data source is `Simulations`
   - Mostly monitoring runs → data source is `Monitoring`
   - Roughly equal → ask user which they prefer
   - **Human review**: Only if the user explicitly mentions it. Do not suggest.

3. **No recent data scenario — STOP and ask before proceeding.**

   Dashboard widgets only display data from the **last 7 days** (rolling window). Data older than 7 days will NOT appear in any widget, regardless of how many runs exist historically.

   Filter runs by `create_time` and only consider runs from the last 7 days. Then check those runs for **successful simulations with actual metric data** — a run with status COMPLETED but all failed simulations is useless for a dashboard.

   To verify, fetch simulations for each recent run and check that at least some have `status: "COMPLETED"` with non-null metric values. A run where every simulation failed = no data.

   **If there are no runs with successful simulations in the last 7 days, DO NOT create the dashboard yet.** Instead:

   Tell the user:
   > "You don't have any recent evaluation data (last 7 days). I need to run some evaluations first so the dashboard has real data to display."

   Then invoke `/quick-eval` with these **minimum requirements for a useful dashboard**:
   - **At least 5 simulations** (use `--iterations` or pick a test set with 5+ test cases)
   - **At least 5 metrics** including **Latency** (always required — find its ID from the builtin metrics list)
   - **Confirm agent and test set with the user** before launching (unless there's only 1 agent — then auto-select)

   **STOP this skill. Invoke `/quick-eval`** with the above parameters. Wait for the evaluation to complete and produce metric data. Only then resume `/build-dashboard`.

   - If there are **no runs at all**: Also ask whether they want a Simulations or Monitoring dashboard before invoking `/quick-eval`.
   - If the user explicitly says they don't want to run evals: **Do NOT create the dashboard.** Tell them to come back when they have data. An empty dashboard is a waste — never create one.

   **There is no "proceed anyway" path.** No data = no dashboard. This is non-negotiable.

   **Human review**: Only if the user explicitly mentions it. Do not suggest.

### Step 4: Analyze data density

**This determines whether to use time series charts or statistics.**

Check how many runs exist within the last 7 days and their timestamps. The default time bucket is **4 hours**, so data points within the same 4-hour window get aggregated together:
- If **2+ runs within 4 hours of each other** (or 5+ runs total in the last 7 days): **use time series charts** (line, bar) — there's enough data to show meaningful trends
- If **fewer than 2 runs in the same 4-hour bucket** (sparse, isolated runs): **use statistics** — there's not enough data for meaningful time series, just show the numbers

This is the single most important layout decision. Time series charts with 1 data point look broken. Statistics with 50 data points waste the data.

### Step 5: Identify top metrics by frequency

**Only consider runs from the last 7 days.** If no recent runs exist and `/quick-eval` was just run, use that run's data.

For the most recent completed runs (up to 10), fetch simulation metrics:

```bash
coval simulations list --run-id <run_id> --format json --page-size 5
coval simulations metrics <simulation_id> --format json
```

Build a frequency map: count how many times each `metric_id` appears with `status: "COMPLETED"` and non-null `value` across simulations. **Sort by frequency descending.**

**Latency is mandatory.** Always include Latency (`29BlkepvvX19ebbLDB0y6Q` or find by `metric_name: "Latency"`) in the dashboard regardless of its frequency ranking. If it's not in the top metrics, add it.

Cross-reference metric IDs with the metrics inventory to get display names and output types.

If a metric has never produced data (all `status: "FAILED"` or `value: null`), deprioritize it — place it lower or omit it.

**Present the frequency map to the user** before building the layout:

```
Metric frequency (last 7 days):

  Metric                  | Appearances | Type    | Status
  ────────────────────────|─────────────|─────────|────────
  Latency                 | 10/10       | float   | ✓ data
  Turn Count              | 10/10       | float   | ✓ data
  Issue Resolution        | 8/10        | binary  | ✓ data
  Professional Tone       | 8/10        | binary  | ✓ data
  Background Noise        | 0/10        | float   | ✗ no data (omitting)

Data density: 5 runs in last 7 days → using time series charts
```

Ask: **"These are the metrics with data. Use all of them, or adjust?"**

> **Note:** Some simulations may return errors when fetching metrics (e.g., audio simulations). Skip those gracefully and continue with the next simulation.

## Phase 1: Dashboard Planning

### Step 1: Select agent focus

If there is **only 1 agent**, auto-select it and tell the user.

If there are **multiple agents**, ask: **"Which agent should this dashboard focus on?"**
- Present agents as a numbered list, highlighting voice agents (they have richer metrics)
- Allow "all agents" for a cross-agent view

### Step 2: Determine layout

A good dashboard has **at most 8-10 widgets** unless the user specifically requests more.

**Layout principles:**
- **Text widgets** separate sections by utility. Fixed at 2 rows tall. Width: full (48), half (24), or thirds (16). **Markdown does not render — plain text only.**
- **Table widgets** should be full-width (48 cols).
- **Chart widgets** can be halves (24), thirds (16), or **fourths (12)** when you have many metrics.
- **Statistic widgets** should be thirds (16) or halves (24). Only use when data is sparse (see Step 4).
- **Row widths**: 2 widgets = 24+24. 3 widgets = 16+16+16. 4 widgets = 12+12+12+12. All sum to 48.

### Step 3: Build the widget list

**This is where you use judgment — not a template.** The layout should be unique to the user's data, metrics, and purpose. Do not produce the same dashboard every time.

**Hard rules (non-negotiable):**
- Text widget section headers are **optional and should be used sparingly**. Only add one when there's a genuine thematic shift (e.g., switching from performance metrics to compliance metrics). Most dashboards need **0-2 text headers at most**. If the dashboard is small (8-10 widgets) or the metrics are all related, you may not need any text headers at all. A wall of text separators is worse than no separators.
- Latency must always appear somewhere.
- All rows must sum to 48 columns.
- **Improving a dashboard = rebuild from scratch**, not append to the bottom.

**Visualization selection — FAVOR TIME SERIES:**

The default visualization for most metrics should be a **time series chart** (line or bar), NOT a statistic or pie chart. Dashboards are most useful when they show how things change over time.

| Metric Type | Default Visualization | When to Use |
|-------------|----------------------|-------------|
| **Float** (latency, duration, count, score) | `line` chart | **Default for all float metrics.** Shows trend over time. |
| **Float** (latency only, if variance matters) | `histogram` | Only if user explicitly cares about distribution consistency. |
| **Binary YES/NO** (resolution, tone, verification) | `bar` with `aggregation: "count"`, `stacked: true`, `showAsPercentage: true` | **100% stacked bar chart.** Shows YES/NO ratio over time. NOT a pie chart. |
| **Categorical string** (end reason, call outcome) — sparse data | `pie` with `aggregation: "count"` | **Default for categorical.** Shows proportion of each category. |
| **Categorical string** — dense data (2+ runs in same 4h bucket) | `bar` with `aggregation: "count"` | Shows how categories change over time. Switch from pie when enough data. |
| **Any metric, sparse data** (< 2 runs in same 4h bucket) | `statistic` | Fallback when there's not enough data for time series. |

**Pie charts are ONLY for categorical metrics** (3+ string categories like "Resolved/Escalated/Abandoned"). Binary YES/NO metrics NEVER get pie charts — they get 100% stacked bar charts.

**Use fourths (12-col) when you have 4+ metrics in a section.** Don't force everything into halves and thirds — if you have 4 similar float metrics, put them in a row of 4 line charts at 12 cols each.

**Pie chart layout:** Pie charts need more height for their legend. Use a 2×2 grid of wider charts on the left with a narrower tall pie on the right:

```
┌──────────────────┬──────────────────┬──────────────┐
│  Chart 18×8      │  Chart 18×8      │              │
├──────────────────┼──────────────────┤  Pie 12×16   │
│  Chart 18×8      │  Chart 18×8      │              │
└──────────────────┴──────────────────┴──────────────┘
```

Grid positions (starting at y=N):
- Top-left: grid-x=0, grid-y=N, grid-w=18, grid-h=8
- Top-right: grid-x=18, grid-y=N, grid-w=18, grid-h=8
- Bottom-left: grid-x=0, grid-y=N+8, grid-w=18, grid-h=8
- Bottom-right: grid-x=18, grid-y=N+8, grid-w=18, grid-h=8
- Pie: grid-x=36, grid-y=N, grid-w=12, grid-h=16

Total: 18+18+12=48 width, 16h tall. The wider charts (18 col) give more room for time series data while the pie stays compact.

**Compose sections based on what metrics you have:**

Group metrics by theme:
- Latency + Audio Duration + Time to First Byte → "Response Performance"
- Turn Count + Words Per Message + Agent Repeats Itself → "Conversation Quality"
- Issue Resolution + Caller Identity Verification + Professional Tone → "Compliance & Quality"
- Agent Fails to Respond + End Reason → "Reliability"

For each section:
1. **Text header** (full-width)
2. **Charts** — line charts for floats, stacked bar charts for binary metrics. Use halves, thirds, or fourths depending on count.

End with a **summary table** (full-width) containing all metrics.

### Step 4: Present and confirm

**You MUST show the layout as an ASCII box-drawing mockup.** Build it from your actual planned widgets:

```
Dashboard: "<name>" (data: <Simulations|Monitoring>)

┌─────────────────────────────────────────────────┐
│  Response Performance                    (text)  │  48col, 2h
├────────────────────────┬────────────────────────┤
│  Line Chart            │  Line Chart            │  24+24=48, 8h
│  (Latency)             │  (Audio Duration)      │
├─────────────────────────────────────────────────┤
│  Compliance & Quality                    (text)  │  48col, 2h
├────────────────────────┬────────────────────────┤
│  Stacked Bar           │  Stacked Bar           │  24+24=48, 8h
│  (Issue Resolution)    │  (Identity Verified?)  │
├─────────────────────────────────────────────────┤
│  Summary Table (all metrics)                     │  48col, 8h
└─────────────────────────────────────────────────┘
```

Ask: **"Does this layout look right? (yes / customize)"**

If customize:
- Allow swapping visualization types
- Allow adding/removing widgets
- Allow reordering sections or metrics
- Allow changing section groupings

## Phase 2: Create Dashboard + Widgets

### Step 1: Create the dashboard (or clear existing)

For **new dashboards**:
```bash
coval dashboards create --name "<dashboard_name>" --format json
```

For **improving existing dashboards**: Delete all existing widgets first, then recreate:
```bash
# Delete each existing widget
coval dashboards widgets delete <dashboard_id> <widget_id>
```

### Step 2: Create widgets row by row

Create widgets top to bottom, left to right. Use explicit `--grid-x` and `--grid-y` positioning.

#### Text widgets (section headers)

```bash
coval dashboards widgets create <dashboard_id> \
  --name "<section_title>" \
  --type text \
  --grid-w 48 --grid-h 2 \
  --grid-x 0 --grid-y <row_y> \
  --config '{"text": "<section_title>"}'
```

**No markdown — plain text only.**

#### Chart widgets (line, bar, area, statistic, histogram)

```bash
coval dashboards widgets create <dashboard_id> \
  --name "<widget_name>" \
  --type chart \
  --grid-w <cols> --grid-h <rows> \
  --grid-x <x> --grid-y <y> \
  --config '{"metricId": "<metric_id>", "visualizationType": "<viz_type>", "monitoring": "<Simulations|Monitoring>", "aggregation": "<agg>", "metricOutputType": "<float|string>"}'
```

Width options: 48 (full), 24 (half), 16 (third), 12 (fourth).

For **binary YES/NO metrics as 100% stacked bar**: use `visualizationType: "bar"` with `aggregation: "count"`, `metricOutputType: "string"`, `stacked: true`, `showAsPercentage: true`.

For **float metrics as line charts**: use `visualizationType: "line"` with `aggregation: "avg"`, `metricOutputType: "float"`.

#### Table widgets

```bash
coval dashboards widgets create <dashboard_id> \
  --name "<widget_name>" \
  --type table \
  --grid-w 48 --grid-h 8 \
  --grid-x 0 --grid-y <row_y> \
  --config '{"monitoring": "<Simulations|Monitoring>", "aggregation": "success", "groupBy": "agent", "filters": {"metricIds": ["<id1>", "<id2>"]}}'
```

**Table widget rules:**
- Always full-width (48 cols)
- Always use `aggregation: "success"` — handles both float and string metrics correctly.
- Always use `groupBy: "agent"` — splits rows by agent for comparison.
- Put metric IDs in `filters.metricIds` (NOT top-level `metricIds`).
- **Only include metrics that have a success condition** — binary YES/NO metrics (Issue Resolution, Professional Tone, Caller Identity Verification, etc.) and metrics with target conditions. **Exclude raw float metrics** like Audio Duration, Long Pause Detection, Turn Count, Words Per Message, Latency — these don't have a pass/fail threshold so they show meaningless values in a success table. They belong in line charts, not the summary table.

### Grid position tracking

Track `grid_y` as you create rows:
- Row 0: text header (h=2) → next y = 2
- Row 2: charts (h=8) → next y = 10
- Row 10: text header (h=2) → next y = 12
- Row 12: charts (h=8) → next y = 20
- Row 20: table (h=8) → next y = 28

## Phase 3: Verify + Fix Layout

### Step 1: Fetch actual widget state

```bash
coval dashboards widgets list <dashboard_id> --format json
```

### Step 2: Verify and show evidence

**Show the user the raw widget list output** as proof. Then verify:

- Widget sizes respect type minimums (chart ≥ 12w×8h, statistic ≥ 10w×12h, table ≥ 4w×8h, text ≥ 12w×2h)
- Each row's widgets sum to exactly **48 columns**
- No unexpected size adjustments from the server

Present the verification result:

```
Layout verified:
  ✓ Row 0: text 48w = 48
  ✓ Row 2: line 24w + line 24w = 48
  ✓ Row 10: text 48w = 48
  ✓ Row 12: bar 24w + bar 24w = 48
  ✓ Row 20: table 48w = 48
  ✓ All sizes meet minimums
```

> **Note:** When you set `--grid-x` and `--grid-y` during creation, the positions are persisted and returned in the response.

### Step 3: Fix any issues

```bash
coval dashboards widgets update <dashboard_id> <widget_id> --grid-x <x> --grid-y <y> --grid-w <w> --grid-h <h>
```

## Phase 4: Summary

Once all widgets are created and verified, tell the user their dashboard is ready:

```
Your dashboard is ready!

  Name:       <dashboard_name>
  Widgets:    <count>
  Data:       <Simulations|Monitoring>

  Open it here: https://app.coval.dev/dashboards/<dashboard_id>

  Layout:
  | Widget              | Type      | Size   | Metric              |
  |---------------------|-----------|--------|---------------------|
  | Response Performance| text      | 48×2   | —                   |
  | Latency             | line      | 24×8   | Latency             |
  | ...                 | ...       | ...    | ...                 |
```

**Always suggest next steps:**
- Run more evaluations to enrich the data: `/quick-eval`
- Add more widgets later: `coval dashboards widgets create`
- Set up scheduled runs for continuous data: `coval scheduled-runs create`
- Configure more metrics: `/configure-metrics`
