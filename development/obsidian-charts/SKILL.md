---
name: obsidian-charts
category: obsidian
description: >
  Build interactive Chart.js charts in Obsidian notes via `chart` codeblocks — inline
  series, a markdown table by block ID, or a Dataview query. Use when the user wants to
  chart, plot, graph, or visualize data in their Obsidian notes, or mentions "obsidian
  charts" or "renderChart".
codex-short-description: "Build Chart.js charts in Obsidian notes from inline series, tables, or Dataview"
related-skills:
  - obsidian-bases
loop-eligible: false

compatibility: claude-code codex opencode
---
# Obsidian Charts Skill

Assumes the user already has the **Charts** community plugin (phibr0/obsidian-charts) installed and enabled.

## Decide the data source first

Before writing any codeblock, pick the source — it changes the syntax:

| Source | Use when | Pattern |
|---|---|---|
| Inline literal | Small, hand-typed series | `chart` codeblock with `labels:` + `series:` |
| Markdown table in same note | Data already lives in a table | `chart` codeblock with `id: <blockId>` |
| Markdown table in another note | Shared data table | `chart` codeblock with `id:` + `file:` |
| Dataview / Dataviewjs query | Data is computed/aggregated | `dataviewjs` codeblock calling `window.renderChart(...)` |
| Frontmatter values | Comparing notes by property | Dataviewjs + `renderChart` (Dataview required) |

If the user is unsure, look at the note. A table → use table linking. A query → use renderChart. Loose numbers in prose → inline literal.

## Quick start — inline data

````markdown
```chart
type: bar
labels: [Mon, Tue, Wed, Thu, Fri]
series:
  - title: Hours focused
    data: [4, 3, 5, 2, 6]
beginAtZero: true
width: 80%
```
````

## Quick start — from a table in the same note

````markdown
| | Q1 | Q2 | Q3 | Q4 |
| - | - | - | - | - |
| Revenue | 10 | 14 | 12 | 18 |
| Cost    | 8  | 9  | 11 | 13 |
^revenue

```chart
type: bar
id: revenue
layout: rows
beginAtZero: true
```
````

`layout: rows` reads each table row as a series; `layout: columns` reads each column as a series. Add `select: [Revenue]` to restrict which rows/columns are charted. Add `file: <OtherNote>` to point at a `^blockId` in another note.

## Quick start — from a Dataview query

Requires the **Dataview** plugin with JS enabled.

````markdown
```dataviewjs
const pages = dv.pages('"Journal"').where(p => p.mood);
window.renderChart({
  type: 'line',
  data: {
    labels: pages.map(p => p.file.name).array(),
    datasets: [{
      label: 'Mood',
      data: pages.map(p => p.mood).array(),
      tension: 0.3,
    }]
  }
}, this.container);
```
````

## Core parameters (chart codeblock)

| Key | Values | Notes |
|---|---|---|
| `type` | `bar` `line` `pie` `doughnut` `radar` `polarArea` | Required |
| `labels` | `[a, b, c]` | Required for non-table source |
| `series` | list of `{ title, data }` | Required for non-table source |
| `id` | block ID | Use instead of `labels`/`series` to pull from a table |
| `file` | note basename | Pairs with `id` for cross-note tables |
| `layout` | `rows` \| `columns` | Table-source only |
| `select` | `[name1, name2]` | Filter rows/cols from a table |
| `beginAtZero` | bool | Force y-axis to start at 0 |
| `stacked` | bool | Stack series (bar/line) |
| `tension` | 0–1 | Line curve smoothing |
| `fill` | bool | Fill area under line |
| `width` | `80%` etc. | Chart width |
| `legend` | bool | Show legend |
| `legendPosition` | `top` `bottom` `left` `right` | |
| `bestFit` | bool | Draw trend line (line/scatter) |
| `bestFitTitle` | string | Label for trend line |
| `bestFitNumber` | number | Series index for trend |
| `labelColors` | bool | Color labels by series |
| `time` | `day` `month` `year` etc. | Treat labels as dates |
| `indexAxis` | `x` \| `y` | `y` makes horizontal bar chart |
| `xMin` `xMax` `yMin` `yMax` | number/date | Axis bounds |
| `xTitle` `yTitle` | string | Axis labels |

See [REFERENCE.md](REFERENCE.md) for the full parameter list, `renderChart` API, color/styling, multi-series patterns, and troubleshooting.

## Workflow when helping the user

1. **Locate the data.** Read the note, identify whether the data is a table (does it have a `^blockId`?), a query result, or loose values.
2. **Pick the chart type.** Comparing categories → `bar`. Trend over time → `line`. Parts of a whole → `pie` / `doughnut`. Multi-dimensional → `radar`.
3. **If using a table**, confirm there is a `^blockId` line beneath it. If not, add one — without it, the chart cannot reference the table.
4. **Draft the codeblock** inline in the note (don't make a new file unless the user asks).
5. **Pick `layout`** carefully — `rows` vs `columns` is the most common "why is my chart wrong" issue. If the chart looks transposed, flip it.
6. **Tell the user to open the note in Reading view or Live Preview** to render the chart; Source view shows the raw codeblock.

## Common gotchas

- **No render in Source mode** — switch to Live Preview or Reading view.
- **Table reference fails** — the `^blockId` must be on its own line immediately after the table, and `id:` in the codeblock must match exactly (no `^`).
- **`layout` mismatch** — series and labels look swapped; flip `rows` ↔ `columns`.
- **Date axis flat / unsorted** — set `time: day` (or `month`/`year`) so the plugin treats labels as dates.
- **`renderChart` undefined** — the Charts plugin isn't enabled, or the codeblock isn't `dataviewjs` (it must be — `dataview` won't work for JS).
- **Series with mismatched lengths** — every `data` array must match `labels.length` (pad with `null` for missing points).

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/obsidian-charts.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
