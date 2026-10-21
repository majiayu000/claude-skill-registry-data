---
name: color-and-accessibility
description: "Use when choosing colours for a chart or report, when a figure must work for colour-blind readers, in grayscale print or in email, when writing alt text or a text alternative for a figure, or when checking contrast. Covers colour roles, palette size, consistent category colours across a report, highlight-and-grey, contrast ratios, not relying on colour alone, and alt text that states the message."
license: CC-BY-4.0
---

# Colour and accessibility

Colour is a data channel, not decoration. Every reader, including the roughly
1 in 12 men with a colour-vision deficiency and anyone reading a grayscale
printout, must get the same message.

## Colour rules

1. **Assign a role before a colour.** Categorical (distinct hues), sequential
   (one hue, light to dark), diverging (two hues around a stated neutral
   centre), highlight (one accent, rest grey).
2. **Few colours.** Aim for five or fewer categorical colours in a chart;
   beyond that, group into "Other", use small multiples, or highlight one
   series and grey the rest.
3. **One colour per category, everywhere.** "Google Ads" is the same colour in
   every figure of a report and across report issues. Keep a mapping table in
   the report template, not in each chart.
4. **Never colour alone.** Pair colour with line style, marker, direct label,
   position or hatching. Red vs green as the only cue fails for the most common
   deficiencies; if good/bad must be shown, add a sign, label or icon.
5. **Contrast.** For web/WCAG 2.2: text at least 4.5:1 against its
   background (3:1 for large text); graphical objects needed to understand the
   chart (lines, bars, markers) at least 3:1 against adjacent colours. Light
   pastel series on white usually fail.
6. **Grey is for context.** Benchmarks, prior years and comparison series in
   grey; the series the title talks about in the accent colour.
7. **Semantic colours are reserved.** If red means "below target" in the
   report, do not also use red as an ordinary category colour.
8. **Check in grayscale and with a CVD simulator.** Grayscale is a useful
   screen, not a complete test.

A safe categorical starting point is the Okabe–Ito palette (designed for
colour-vision deficiencies). Brand palettes must be checked against rules 4–5
before use.

## Text alternatives

Every figure that leaves the workspace carries a text alternative. Good alt
text states the **message and the key numbers**, not the chart's appearance
and not every data point:

> Line chart of weekly paid orders, 31 Aug to 4 Oct 2026. Orders rose
> from 41 to 47; the week of 14 Sep has no data because the order export
> failed.

Bad: "Chart showing orders." / "A blue line going up." / a list of all 52
weekly values.

Also provide: the data as a table or download where the medium allows, a
specific source line, and the description directly below the figure in web
reports.

## ieeVisualizer: what it does and does not do

- Forecasts are distinguished by dash pattern, opacity, hollow markers and
  hatching, not by colour alone, and the legend says "forecast".
- Uncertainty bounds take their value series' colour (`color_of`), keeping
  one colour per entity.
- After 10 series the colour cycle wraps (`colour_cycle_wrapped`); the
  renderer varies line style/marker so series stay distinct. Fix the
  figure (fewer series) rather than relying on it.
- Not enforced: contrast ratios, CVD safety of the default 10-colour cycle,
  consistent category→colour mapping across figures (set `style.color`
  explicitly per layer to guarantee it), alt text (the manifest has no alt
  text field; supply it in the report). Automated accessibility checks are
  planned for agent-contributed templates (ROADMAP "Phase 2 onward").

## Good / bad

Bad: six acquisition channels in six saturated hues, legend at the bottom,
"Paid social" and "Organic" in red and green.
Good: the two channels discussed in accent colours with direct labels, the
other four grey, labelled at line ends.

Bad: heatmap where "no data" cells are white and low values are near-white.
Good: missing cells in a distinct neutral with a "no data" key entry
(ieeVisualizer leaves null cells blank: say so in the caption).

## Checklist

- [ ] Each colour has a role; categorical palette ≤ about 5 colours.
- [ ] Same category → same colour across the report.
- [ ] Every colour distinction has a second cue (style, marker, label).
- [ ] Text ≥ 4.5:1, essential graphics ≥ 3:1 against their background.
- [ ] Figure checked in grayscale and with a CVD simulator.
- [ ] Alt text states the message and key numbers, plus a data table or link.
- [ ] Missing values look different from low values.

Adapted in part from ONS Service Manual and UK Analysis Function guidance
(OGL v3.0), Anthropic `data-visualization` (Apache-2.0) and K-Dense
`scientific-visualization` (MIT); changed: rewritten, merged, examples
replaced. Sources and licences: `SOURCES.md`.
