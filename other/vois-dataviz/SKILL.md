---
name: vois-dataviz
description: Data visualization and dashboard rules for web apps. Use whenever a screen contains a chart, graph, sparkline, KPI tile, heatmap, map, or data-heavy dashboard, whether you are building it, picking a chart type, choosing chart colors, designing filters or date ranges, designing loading and empty states for data, or reviewing and improving an existing dashboard. Walks a chart-selection decision tree, gives do's and don'ts per principle, ships a chart spec, a code detector and a review protocol that agents can run. Optionally records the chart form via vois_record_component_choice if that tool is available.
version: 1.0.2
---

# Vois Data Visualization Skill

A chart is read by people and built by you. This skill makes the result right by construction: it picks the form from the viewer's job, assigns color by the job it does, builds the states most dashboards forget, and gives you something to check against.

It answers **"what should this data look like, and is it honest and usable?"** Page structure is `vois-patterns`, container components are `vois-components`, token values and motion are `vois-tokens`, and every word on the screen is `righter`.

**Two modes.** BUILD: you're creating a visualization or dashboard. REVIEW: you're evaluating or improving an existing one. The steps differ; the rules are the same.

---

## BUILD: the order of work

1. **Write the spec.** One per visualization, following `data/chart-spec.schema.json`: the question it answers, the audience, the job, the form. If you can't write the question, the chart shouldn't exist `[DV-PURPOSE-001]`.
2. **Walk the decision tree** (below, in full in `references/decision-tree.md`). Land on a result node and a form id from `data/chart-catalog.json`.
3. **Check the spec:** `node scripts/check-spec.mjs spec.json`. Fix every FAIL before you write code. `--tree <job>` lists the forms a job can reach.
4. **Record the choice.** If a `vois_record_component_choice` tool is available, call it with `job` (the viewer's question), `componentName` (such as `ChartContainer + LineChart`), `alternativesConsidered` (other forms from the tree) and `reasoning` (the tree result id, e.g. `CHART-R-LINE-MULTI`). If nothing in the tree fits and `vois_report_pattern_gap` is available, call it with the closest result as `attemptedFallback`; otherwise say so in your answer.
5. **Get tokens.** Get the chart roles in `references/implementation.md` from the workspace tokens (`vois_get_tokens` if available). Never write a color value, and never invent a missing role: report the gap.
6. **Build** from one typed config `[DV-SUSTAIN-001]`, following `references/implementation.md`. Build the dashboard from `DASH-*` templates and pieces (`references/dashboard-patterns.md`).
7. **Build the states:** skeleton, four kinds of empty, error, refetch, partial `[DV-STATE-001]` through `[DV-STATE-007]`. Copy goes through `righter`.
8. **Check the code:** `node scripts/detect.mjs <files>`. Then look at it at 320, 640 and 1280px, light and dark, with a keyboard.
9. **Record usage** (optional): if `vois_record_rule_usage` is available, call it with the `DV-*` ids you applied (`violated` or `ambiguous` where they weren't met). These calls are telemetry; if one is missing or errors, carry on.

## REVIEW: the order of work

Follow `references/review-protocol.md`: inventory, infer each job, check the form against the tree, run the mechanical checks, run the judgment checks in triage order, check the page as a whole, propose the upgrade, report in `data/review-output.schema.json`. `data/review-checklist.json` has a symptom to fix playbook for the 20 most common problems. Don't flag what passes, and list what you couldn't check.

---

## Decision tree, at a glance

Start with the viewer's job, not the chart. Full tree with every branch: `references/decision-tree.md` and `data/decision-tree.json`.

| The viewer needs to... | Default form | Branch |
|---|---|---|
| Read one number | Stat tile with delta, sparkline if the trend matters. Meter if it's a ratio against a limit | `CHART-Q-SINGLE` |
| See change over time | Line (continuous), column (12 or fewer discrete periods), area (volume, zero baseline), step (holds between events) | `CHART-Q-TIME` |
| Compare or rank categories | Sorted horizontal bar. Top 10 plus Other past about 12 | `CHART-Q-COMPARE` |
| See parts of a whole | Donut for 3 to 6 parts, stacked bar to compare across groups, sorted bar past 6 | `CHART-Q-PART` |
| See how two measures relate | Scatter, heatmap for two categories | `CHART-Q-RELATE` |
| See spread or outliers | Histogram for general audiences; box plot only for analysts | `CHART-Q-DIST` |
| See stages or flows | Funnel as aligned bars with step conversion; Sankey for 15 or fewer nodes | `CHART-Q-FLOW` |
| See where | Choropleth for rates only; ranked bar for counts | `CHART-Q-GEO` |
| Look up exact values | Table, with inline sparklines or bars | `CHART-R-TABLE` |

Then run the **gates** on the result: audience, simpler form, series count, scale, table twin, volume.

## Quick reference

| Situation | Use | Not |
|---|---|---|
| A single current number | Stat tile with a named delta | A one-bar chart, a 2-slice pie `[DV-FORM-003]` |
| 2 to 4 series, same unit | Multi-line with a legend and end labels | Dual axis `[DV-HONEST-002]` |
| Different units or scales | Small multiples with a shared crosshair | Two y-axes on one plot |
| 6 or more series and one is the story | Emphasis: one accent, rest gray `[DV-COLOR-009]` | Eight hues competing |
| More than 8 groups | Top 8 plus Other, table for the tail `[DV-FILTER-007]` | A 16-hue stack with '+11 more' |
| Part-to-whole, 3 to 6 parts | Donut with the total in the hole | A 9-slice pie `[DV-FORM-004]` |
| Bars | Zero baseline, one color for one series `[DV-HONEST-001]` `[DV-COLOR-007]` | A truncated axis, a hue per bar |
| Line that curves | Monotone or linear; step for state `[DV-HONEST-005]` | Natural spline overshoot |
| Current period still open | Hatched bar or dashed line, labeled `[DV-HONEST-004]` | A cliff that is just an unfinished day |
| Delta on a KPI | Arrow, sign, number, named baseline `[DV-CONTEXT-002]` | A bare percent, color-only meaning |
| Value is zero because nothing was collected | A 'collecting data' state `[DV-STATE-002]` | A flat zero line `[DV-HONEST-008]` |
| Trend inside a table row | Axisless muted sparkline `[DV-FORM-008]` | A mini chart with axes and a legend |
| Date range | Presets first, comparison beside, timezone shown `[DV-FILTER-002]` | A calendar only |
| Every chart needs reading without sight or color | Text alternative, `accessibilityLayer`, Chart or Table toggle `[DV-A11Y-003]` `[DV-A11Y-004]` | A tooltip as the only readout `[DV-A11Y-006]` |

## Which dashboard?

Walk `DASH-Q-TYPE` in `references/dashboard-patterns.md`.

| Reader | Template |
|---|---|
| A leader scanning in 30 seconds | `DASH-EXEC` |
| An operator watching live state | `DASH-MONITOR` |
| An analyst asking new questions | `DASH-EXPLORER` |
| A weekly or monthly narrative that gets exported | `DASH-REPORT` |
| Users assembling their own widgets | `DASH-BUILDER` |
| Someone who drilled into one metric | `DASH-METRIC-DETAIL` |

Reusable pieces: `DASH-KPI-TILE`, `DASH-CHART-CARD`, `DASH-FILTER-BAR`, `DASH-DATE-RANGE`, `DASH-STATE-MATRIX`, `DASH-TABLE-SPARK`, `DASH-DRILLDOWN`, `DASH-TOOLTIP`.

---

## The 14 principles

Each one has a full do and don't list in `references/principles.md`. The headline:

| Principle | One line | Do | Don't |
|---|---|---|---|
| **DV-PURPOSE** Question and audience | One question, one reader | Write the question before the form | Add a chart because the data exists |
| **DV-FORM** Simplest form | The viewer's job picks the form | Walk the tree; stat tile for one number | Pie to compare close values; 22-type pickers |
| **DV-HONEST** Truthful | One honest axis, marked partials | Zero baseline for bars; hatch the open period | Dual axes, spline overshoot, flat zero for missing |
| **DV-CLARITY** Data, not ink | Remove what doesn't help reading | Label the end and the extreme | A number on every point; truncated axis titles |
| **DV-COLOR** Color by job | Identity, magnitude, polarity, status | Tokens in fixed order; entity keeps its color | Hex values; a hue per bar; a 9th hue |
| **DV-CONSIST** Consistent | Same metric, same look everywhere | One formatter and one period per filter | $1.2M here, 1,200,000 there |
| **DV-CONTEXT** Framed | Compare, scope, date | Delta against a named period; labeled targets | A bare number; a hidden chart filter |
| **DV-A11Y** Accessible | Works without color, mouse, sight, motion | Text alternative, table twin, 3:1 marks | Tooltip as the only readout; red and green alone |
| **DV-INTERACT** Interactive | Crosshair, shared tooltip, legend toggle | Visible click affordance, one card menu | Needing to hit a 2px line |
| **DV-FILTER** One slice | One row of filters above the cards | Presets, comparison, URL state | Per-card pickers; skeleton flash on refetch |
| **DV-STATE** Every state | Loading, empty (4 kinds), error, stale | Skeleton in final geometry | Full-page spinner; one generic 'No data' |
| **DV-LAYOUT** Hierarchy | Filters, hero KPIs, trend, breakdowns, table | One card anatomy | A grid of equal-weight cards |
| **DV-SUSTAIN** Built for live data | Typed config, ugly cases handled | One config feeds chart, table and export | Hardcoded demo data |
| **DV-IMPL** Vois stack | Primitives, tokens, accessibility defaults | shadcn Chart with a typed config | Inline colors, fixed pixel widths |

## Non-negotiables

These are `required` rules a reviewer will FAIL. Everything else is a WARN with a fix.

- One y-axis per chart `[DV-HONEST-002]`; bars and areas start at zero `[DV-HONEST-001]`.
- Categorical hues in fixed order, never cycled, eight at most `[DV-COLOR-003]`; chart colors are tokens `[DV-COLOR-001]`; an entity keeps its color `[DV-COLOR-004]`.
- Color is never the only signal `[DV-A11Y-001]`; marks 3:1 and text 4.5:1 `[DV-A11Y-002]`.
- Every chart has a text alternative and a table view `[DV-A11Y-003]` `[DV-A11Y-004]`; tooltips enhance and never gate `[DV-A11Y-006]`.
- Partial periods, forecasts and missing data look different from the real thing `[DV-HONEST-004]` `[DV-HONEST-008]`.
- Every KPI has a delta against a named period `[DV-CONTEXT-002]`.
- One filter row above what it scopes, and every card obeys it `[DV-FILTER-001]` `[DV-FILTER-004]`.
- Skeleton in final geometry on first load, held frame on refetch, errors isolated to the card `[DV-STATE-001]` `[DV-FILTER-008]` `[DV-STATE-003]`.
- No hardcoded data in a chart component `[DV-SUSTAIN-005]`.

## Taste dials

When the project defines the three taste dials in `VOIS.md` or `DESIGN.md`: **DENSITY** moves the per-view cap from about 6 to 8 up to 10 visualizations and allows analyst forms for analyst audiences; **MOTION** never exceeds 300ms and always yields to reduced motion `[DV-A11Y-008]`; **VARIANCE** can vary card composition but never the form choice or any honesty rule. Dials tune within the rules, never against them.

---

## Reference files

Generated from `data/*.json` by `scripts/build-reference.mjs`, so they can't drift:

| File | Use it for |
|---|---|
| `references/principles.md` | Do's and don'ts for each principle, and all 114 rules with do, don't, check and evidence |
| `references/decision-tree.md` | The full chart-selection tree with a diagram per branch and the gates |
| `references/chart-catalog.md` | 48 forms: when to use, when not, baseline, limits, color job, build hint |
| `references/dashboard-patterns.md` | Six page templates and eight reusable pieces |
| `references/evidence.md` | 57 real-product screens from Mobbin: what to adopt, what to avoid |

Written by hand:

| File | Use it for |
|---|---|
| `references/implementation.md` | Chart token roles, shadcn Chart and Recharts code, states, table twin, MCP calls |
| `references/review-protocol.md` | How to review and improve existing work, with a worked example |
| `references/sources.md` | What each source contributed, and what wasn't read |

## Structured data (query these instead of scanning prose)

| File | Keyed by | Holds |
|---|---|---|
| `data/dataviz-rules.json` | `DV-<AREA>-NNN` | 14 principles and 114 rules: severity, enforcement, do, don't, check, sources, evidence |
| `data/decision-tree.json` | question and result node ids | The tree as a graph, job entry points, gates |
| `data/chart-catalog.json` | `FORM-*` | 48 forms with fit, audience, baseline, color job, build hint |
| `data/dashboard-patterns.json` | `DASH-*` | Templates and pieces: structure, components, rules, evidence |
| `data/evidence.json` | `MOB-NN` | Mobbin observations with lesson and rule ids |
| `data/review-checklist.json` | | Review steps, severity map, triage order, fix playbook, the loop checklist |
| `data/chart-spec.schema.json` | | The spec you fill in before coding |
| `data/review-output.schema.json` | | The shape of a review |

**Source of truth.** The JSON is canonical and the generated references restate it. `scripts/dataviz.test.mjs` fails CI if an ID in prose has no JSON entry or the reverse.

## Scripts

| Script | Does |
|---|---|
| `scripts/check-spec.mjs <spec.json>` | Checks a chart spec: the 9 `spec` rules plus form-versus-job reachability in the tree |
| `scripts/check-spec.mjs --tree <job>` | Lists every form a job can reach |
| `scripts/detect.mjs <files>` | Finds the 15 `auto` rules in chart code (13 detectors). Add `// dataviz-allow: <detector>` for a deliberate exception |
| `scripts/build-reference.mjs [--check]` | Regenerates, or checks, the generated references |
| `scripts/dataviz.test.mjs` | 54 tests: detectors, spec checker, data integrity |

---

## Relationship to other skills

**`vois-patterns` first.** It decides that the screen is a dashboard or contains data. Come here for what's inside it.
**`vois-components`** (`JOB-VISUALIZE-DATA`) routes data jobs here, then picks the containers: Card, Tabs, Popover, Calendar, Table, Skeleton.
**`vois-tokens`** supplies live token values, motion and hit-area rules. This skill adds chart roles on top and cites `DS-A11Y-001`, `DS-A11Y-002`, `DS-ANIMATION-001` and `DS-ANIMATION-004`.
**`righter`** writes every title, subtitle, tooltip label, empty state and error. This skill says what the state is, never the words.
**`metrics-tagging`** instruments chart interactions (range change, legend toggle, drill-down, export) when asked.
**`design-rationale`** explains why a form or color choice is right when someone pushes back.

## Checklist before handoff

- [ ] Spec written for each visualization and `check-spec` has no FAIL
- [ ] Form reached through the tree (and `vois_record_component_choice` called, if available)
- [ ] Colors are chart tokens in fixed order, checked per mode
- [ ] Text alternative, `accessibilityLayer`, table view, keyboard path
- [ ] Tooltip and crosshair, legend for 2 or more series, drill-down affordance
- [ ] One filter row with date presets and a named comparison
- [ ] Skeleton, four empty cases, error, refetch and partial states built
- [ ] `detect.mjs` run and clean, or each finding justified
- [ ] Checked at 320, 640 and 1280px, light and dark
- [ ] `vois_record_rule_usage` called, if available
