---
name: data-visualization
description: Say it with charts — right chart for the job, honest axes, accessible color, annotation that explains.
version: 1
triggers: charts, data visualization, graph this, honest charts, visualize data
category: Thinking & decisions
blurb: Say it with charts — the right chart for the job, honest axes and annotation that explains.
archetype: knowledge
example: Pick the right chart for this data and build it honestly.
---

# Data Visualization

A chart is an argument. Choose the encoding that fits the question, keep it honest, and annotate so the reader sees what you see — in five seconds.

## When to use
- Any chart destined for a report, dashboard, or decision.
- Reviewing charts for distortion or confusion.
- Dashboards: layout, hierarchy, what deserves space.

## Method
1. **Question → chart**: comparison → sorted bars; trend → line (time on x); distribution → histogram/box; relationship → scatter; composition → stacked bars (sparingly); part-to-whole over time → small multiples, not pie-animations.
2. **Honesty rules**: y-axis at zero for bars; no dual axes implying causation; consistent scales when comparing panels; label data source + date; if an axis is truncated — flag it loudly.
3. **Perception first**: position/length beat angle/area/color; most important thing top-left (or largest); chart-junk minimized (faint gridlines, no 3D).
4. **Color with purpose**: colorblind-safe categorical palettes; sequential for magnitude; diverging around a real midpoint; never red/green alone; ≤7 categories.
5. **Annotation that explains**: title = the finding, not the topic ("Revenue fell 12% in Q3", not "Revenue"); mark events/thresholds; call out outliers directly.
6. **Accessibility + text**: legible sizes; alt text or table fallback; values readable without hover; contrast for print and screen.
7. **Dashboards**: one screen = one story; metric definitions + owners (`product-analytics`); refresh cadence visible; retire stale panels.
8. **Tooling**: matplotlib/plotly/vega/Excel — version + data snapshot with every exported chart, so it's reproducible.

## Quality gates
- [ ] Chart type matches the question; zero-baseline rules respected (or flagged).
- [ ] Colorblind-safe palette; no red/green-only encoding.
- [ ] Title states the finding; key values annotated.
- [ ] Source + date + snapshot recorded; accessible alternative exists.

## Red lines
- No misleading axes/scales; no chart-junk as branding; never chart data you can't reproduce.

## Related
`product-analytics` · `electrical-test-records` (domain trending) · `technical-writing`.
