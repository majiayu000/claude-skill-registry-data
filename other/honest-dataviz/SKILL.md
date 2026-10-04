---
name: honest-dataviz
description: >
  Charts and dashboards that read at a glance, survive a colour-blind
  reviewer, and never imply more certainty than the data has. Use this
  BEFORE writing any chart, graph, KPI tile, dashboard, or data
  visualization — in any library or in hand-drawn SVG/HTML — and whenever
  choosing chart colours, building a stat row, or deciding whether
  something should be a chart at all.
---

# Honest dataviz

A chart is read by people and executed by you. This skill turns "make it
look good" into decisions with reasons, so the result is right by
construction. Every rule here was bought with a measured failure in a
production reporting engine — none is taste.

## First decision: is it even a chart?

| The data is… | Use | Not |
|---|---|---|
| One current value (+ trend) | Stat tile: label, hero figure, semantic delta, small sparkline | A one-bar bar chart |
| A handful of headline numbers | A KPI row of stat tiles | A grouped bar chart |
| A ratio against a limit | A meter with the limit marked | A two-slice pie |
| More than ~7 categories that all matter | A table (or table + chart) | More colours |
| A verification story (checks, statuses) | A tracker strip: one cell per check | Prose |

If a chart is right, the data's JOB picks the form: magnitude → bars;
trend → line/area; part-to-whole → stacked bar (horizontal when names are
long) or a two-segment donut at most; above/below a baseline → diverging
bars around zero; one series against context → emphasis (one hue, grey
rest). The most underused honest form is **emphasis**; the most overused
dishonest one is categorical rainbow.

## Typography on charts — the two highest-leverage fixes

1. **At most three font sizes per view.** Generated dashboards carry five
   to eight; consolidating to three is the single biggest "suddenly looks
   designed" move.
2. **Pull the weights back.** Nothing above semibold. Bold everywhere is
   the clearest generated-dashboard tell there is.
3. Values, labels and legends wear TEXT colours (ink/soft/muted), never
   the series colour. A coloured mark beside them carries identity.

## The colour law

- **Colour is spent on data, never on chrome.** Axes, grids, panels and
  labels are neutral. If a colour appears, it means something.
- **Semantic pair**: green = up/good/verified, red = down/fails — and
  NOTHING else ever borrows those two. A red that sometimes means
  "category B" destroys the one thing colour was teaching the eye.
- **The semantic pair is a STATUS pair, not a chart palette.** Measured:
  a standard green/red pair fails colour-blind separation (deutan ΔE ≈ 5,
  where ≥ 8 is safe). Legal only when polarity is ALSO carried by
  position (diverging around zero), glyphs (▲ ▼ ✓), or words — colour
  reinforces, never carries alone.
- **Magnitude = one hue, light→dark** (an ink ramp is safest). Identity
  for 2–3 series = distinct hues, direct-labelled. More series than that:
  fold to "Other", facet into small multiples, or emphasize one — never
  generate a 9th hue.
- **Validate, don't eyeball.** Run any CVD simulator/validator over the
  final palette against the actual surface colour, in BOTH themes. If a
  pair lands in the marginal band, secondary encoding (labels, position,
  texture) is mandatory, not nice-to-have.

## Mark specs (the difference between crisp and mushy)

- Bars ≤ 24px thick; 4px rounded data-end, square at the baseline; grow
  from one baseline. 2px gap in the SURFACE colour between touching marks.
- Lines 2px, round joins; markers ≥ 8px with a 2px surface ring.
- Sparklines: de-emphasis grey with an ink endpoint dot; ~12–28 points.
- Direct-label only the max, the min, and the point the caption is about.
  A number on every point is noise wearing a badge.
- Grid and axes recessive (faintest text colour); one axis only — a dual
  y-axis chart is the #1 chart mistake; use two charts or index to 100.

## Honesty mechanics (what makes a dashboard trustworthy, not just pretty)

- **A receipts panel must add up to its own headline.** If rows are
  rounded independently, they won't (measured: $819,771 of rows under an
  $819,770 headline). Show evidence at full precision.
- **A sample size belongs to its figure, not to the page.** "n=1,204" as
  a page-level fact beside a metric computed on 218 is a wrong number
  with a right value.
- **A component is not a peer.** Two equal tiles invite addition; when
  one is inside the other, the page invites double-counting. Render the
  component subordinate and say "part of X".
- **A state is not a finding.** "First period, nothing to compare against"
  is the absence of history — state it; never count it as doubt, and
  never colour it as failure.
- **Unverified figures are shown AND labelled** — muted value, a plain
  "not verified" flag, and the reason somewhere findable. Hiding doubt is
  the one dishonesty a reader never forgives.

## Anti-pattern catalogue (if the chart matches an entry, it's wrong)

Dual axes · rainbow categoricals · a hue at a diverging midpoint · pies
beyond 2–3 slices · cumulative charts implying growth while the periodic
series falls · truncated bar axes · a number on every point · gradient
fills on data · colour re-assigned when a filter changes the series count
· hover states on inert elements · decorative icons anchoring KPI corners
· light/dark mode as the flagship feature of an MVP dashboard.

## Hand-drawn SVG traps (each cost a real debugging round)

- **Author SVG at its rendered width.** Text inside SVG scales with the
  viewBox: a label authored 12px at 1044 units renders 5px in a 473px
  column. Prefer HTML for labels around width-fluid charts.
- Grid cells must equal the column template — extras wrap into invisible
  second rows and triple the row height silently.
- **Only a render is evidence.** Screenshot the result and look at it, in
  both themes, at mobile width, and printed. CSS that "reads right" has
  shipped invisible twice in the corpus this skill comes from.

---
*kymira honest-dataviz · v2026.08.21 · lifetime updates included*
