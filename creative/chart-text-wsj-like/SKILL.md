---
name: chart-text-wsj-like
description: "WSJ-like chart text and graphics practice. Use when writing the words on and around a chart or table: headline title that states the finding, subtitle with measure/unit/period/population, axis labels, tick formatting, direct labels, annotations, legend, and the source-and-notes line. Use for every figure in a report, briefing, paper or slide, and when a chart's title only names the metric ('Revenue by month')."
license: CC-BY-4.0
---

# Chart text (WSJ-like)

A reader looks at the title, then the shape, then the labels. The words must
tell them what to see and exactly what was measured, in that order, without
hype and without leaving them to decode abbreviations.

This is a WSJ-like graphics style: our own adaptation of principles
described in public reviews and summaries of Dona M. Wong's *The Wall Street
Journal Guide to Information Graphics* (2010), combined with UK government
statistics guidance (see `SOURCES.md`), restated in our own words. It is not
the Journal's style guide, is not affiliated with or endorsed by the paper,
and uses none of its fonts or logos. Numeric limits below are guidance, not hard rules.

## The text stack (top to bottom)

1. **Headline title: the finding.** A short sentence with the claim:
   "Orders recovered to 47 a week after the September dip". Not "Weekly
   orders". Every number and verb in it must be checked against the data
   (`headline-and-deck`). Where no single finding is warranted (a monitoring
   chart), a plain descriptive title is honest: do not invent a story.
2. **Subtitle: what exactly is measured.** Measure, unit, period, population,
   and any transform: "Paid orders per ISO week, all regions,
   ISO weeks 36–40 (31 Aug–4 Oct 2026)". "Index, Jan 2026 = 100". "7-day rolling mean".
3. **Plot labels.** Axis labels with units ("Revenue (€ thousands)"); direct
   labels at line ends or on bars instead of a legend when there are few
   series; annotations for the one or two events that explain the shape
   ("Attribution window changed", "Price list v7").
4. **Source and notes line.** "Source: order service, retrieved 5 Oct 2026
   06:00 CEST. Note: no data for week of 14 Sep (export failed). Forecast:
   orders model v3." See `source-and-provenance`.

## Rules

- **Plain text.** Sentence case; no all-caps; horizontal labels only (if they
  do not fit, flip to horizontal bars or shorten); spell out acronyms on first
  use ("cost per order (CPA)") unless the audience uses them daily.
- **One emphasis device.** Bold *or* colour *or* an arrow, not all three.
- **Natural ticks.** Steps of 1, 2, 5 or 10 × a power of ten; about ten
  gridlines at most, light grey; units in the axis label rather than on every
  tick; thousands separators; consistent decimals.
- **Scale with intent.** Choose the y-range so the line uses most of the plot
  height (summaries of Wong report roughly two thirds) unless the zero
  baseline is the point; bars always from zero.
- **Few series.** About four lines, never more than five (both the UK
  Analysis Function guidance and summaries of Wong say so); a handful of
  bars, each about twice as wide as the gap between bars; pies only with few
  slices. More: highlight and grey, or split.
- **Legend last resort.** Order legend entries as the series appear in the
  plot; never make the reader match colours across the page.
- **Annotate events, not decorations.** Each annotation is a dated fact with
  a source, not an interpretation the data cannot support.
- **No hype in the title.** "soared", "plunged", "record" need the number to
  justify them, and "record" needs the full history.

## Graphics-desk practice (reported in summaries of Wong's guide)

These are restated from public reviews and summaries, not from the book.

- **Process: research → edit → plot → review.** Start from a reliable source,
  decide the one message, cut the data to what supports it, choose the form,
  and finally check every plotted value and label against the source.
- **Do the maths for the reader.** If the point is a change, plot or label the
  change (% change, difference vs last year), not two levels the reader must
  subtract. If levels mislead (two regions of very different size), switch to
  a rate or per-unit measure.
- **Give a reference point.** A figure without a comparison (last year,
  plan, peers, per-unit) leaves the reader unable to judge good or bad.
- **One variable, one colour.** Use shades of one hue for one variable's
  categories; do not spread a single kind of data over unrelated colours.
- **Direct labels first;** a legend only when space is tight or lines cross.
- **Missing data in the open.** Footnote gaps; drop a series that has too
  many gaps to read as a line; never draw a pie with a missing slice.
- **Pies, if at all:** few slices, largest starting at 12 o'clock and running
  clockwise, the next largest just counter-clockwise from 12.
- **Pictograms** only for small counts, one icon per whole unit; never a
  fractional icon.
- **Name the average.** Mean, median, weighted or moving; pick the one that
  fits the distribution and say which.
- **Tables are graphics too.** A thin rule every three to five rows to guide
  the eye; spell out names instead of acronyms; round only at the last step.
  Common practice we add: right-align numbers on the decimal point, units in
  the column header rather than every cell, consistent decimals per column.
- **Restraint.** No 3D, shadows, rotated elements or decorative images; let
  the data carry the message without over-annotation.

## ieeVisualizer mapping

| Text | Where |
|---|---|
| Headline title | `spec.title` (template param `title`) |
| Subtitle, source, notes | `spec.caption` (no subtitle field in spec 1.0; first caption sentence = subtitle) |
| Axis label + unit | `axes.y.label`, `axes.y.unit`; rendered as "Label (unit)", or derived from the column's description/name and unit |
| Series names | layer `name` (legend label) |
| Events | `annotations`: `text`, `reference_line` (with `label`), `reference_band` |
| Target | `timeseries` param `target` / `target_label` |
| Ticks | renderer automatic in spec 1.0; set `axes.*.limits` to round values |

The renderer thins category labels past 50 (`category_labels_thinned`
warning): treat it as a sign the chart has too many categories.

## Good / bad

Bad title: "CPA by Channel Q3 2026".
Good: "Cost per order fell on Google Ads and rose on Meta" + subtitle
"Ad spend per paid order (€), by channel, Jul–Sep 2026, 28-day
click attribution".

Bad axis: "conv_rate" with ticks 0.2134, 0.2268, ….
Good: "Consultation-to-order conversion (%)" with ticks 20, 22, 24, 26.

Bad: legend with 7 entries at the bottom, colours to match.
Good: two highlighted lines labelled at their ends, others grey and
unlabelled, caption "Grey: other channels".

## Checklist

- [ ] Title states the finding (or is honestly descriptive for monitoring).
- [ ] Subtitle/caption gives measure, unit, period, population, transform.
- [ ] Axis labels carry units; ticks are round numbers with separators.
- [ ] Few series; direct labels instead of legend where possible.
- [ ] At most one emphasis device; no all-caps, rotated text or unexplained acronyms.
- [ ] Annotations are dated facts.
- [ ] Source and notes line present, including gaps and forecasts.
- [ ] The chart does the maths (change or rate plotted when that is the point) and has a reference point.
- [ ] Every plotted value and label re-checked against the source after plotting.
- [ ] Tables: numbers right-aligned, units in headers, consistent rounding.

Adapted in part from UK Analysis Function chart guidance (OGL v3.0); changed:
rewritten and combined with cited news-graphics principles. Sources and
licences: `SOURCES.md`.
