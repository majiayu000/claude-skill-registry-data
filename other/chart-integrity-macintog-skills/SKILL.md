---
name: chart-integrity
description: Use when creating, revising, or critiquing a chart, dashboard, or KPI display that makes a quantitative comparison someone will act on. Covers honest comparison and rendered checks; leave palette, marks, and library mechanics to the medium's own skill. Skip decorative graphics and diagrams with no data.
---

# Chart integrity

What survives a capable model is integrity slips and unchecked rendering, not chart-type choice. Check:

1. **Comparable inputs.** Same definition, unit, population, denominator, and window on both sides. Mark or drop a partial current period beside complete ones; never draw it as a decline. Don't connect across missing intervals.
2. **Magnitude.** Show the base with relative change ("100 → 110, +10%"). Label percentage points vs percent. Length encodings start at zero; a non-zero line axis is fine when disclosed.
3. **Claims.** Titles state only what the data supports; no causal verbs for observational data. Name the interval type when showing uncertainty; don't rank estimates whose intervals make the order unstable. Declare top-N, filtered, or excluded subsets.
4. **Visible by default.** Units, active filters, source and as-of date, and material caveats sit on or beside the chart, not in hover only. Captions and alt text match the active filtered state. KPIs carry a comparator (prior, target, or trend).
5. **Look at it.** Render at delivery size and each viewport you ship. Inspect for clipped or colliding labels, legends over data, illegible ticks, inconsistent panel scales, and color as the only carrier of meaning. Fix and re-render. If you could not render, say so.

A request for "Tufte" or "clean" style means dense, honest evidence: plain background, plain type, direct labels. Skip stock styling (cream paper, serif fonts, a muted red accent) applied for looks.

Use real data; label any synthetic data as synthetic.

For critique, lead with what misleads, then what impairs reading, then craft. Skip items that pass.
