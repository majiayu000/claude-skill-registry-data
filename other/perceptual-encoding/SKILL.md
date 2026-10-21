---
name: perceptual-encoding
description: "Use when deciding how a quantity is mapped to something visible (position, length, angle, area, colour, line style), when a comparison in a chart is hard to read, when choosing between bars, dots, pies, bubbles or heatmaps, or when picking a colormap for ordered or diverging values. Applies the perception-accuracy ordering from graphical-perception research to concrete chart decisions."
license: CC-BY-4.0
---

# Perceptual encoding

The reader decodes values from marks. Some channels are decoded accurately,
others only roughly. Put the comparison that matters on the most accurate
channel available.

## The ordering (cited finding)

Cleveland and McGill (1984), replicated by Heer and Bostock (2010) with
crowdsourced participants, found that people judge quantitative comparisons
most accurately from **position on a common aligned scale**, then position on
non-aligned scales, then **length** and **direction/angle**, then **area**,
with **volume, curvature and shading/colour saturation** least accurate. Hue
was not in their ranking; it separates categories but does not carry
magnitude. Treat this as an ordering, not a precise scale.

## Rules

1. **The key comparison goes on a common scale.** If the point is "North
   vs South region revenue per order", put both on one axis side by side, not in
   two pies or two panels with different scales.
2. **Length needs a zero baseline.** Bars and areas are read as length from
   the baseline; a truncated baseline misstates every ratio. Dots and lines
   encode position and may use a non-zero range.
3. **Prefer length to angle, angle to area.** Bars beat pies; pies beat
   bubbles for shares. A bubble chart is acceptable when the third variable is
   secondary; scale *area*, not radius, to the value.
4. **Hue is for categories, lightness for order.** Use distinct hues for
   unordered groups (channels, cities). Use a single-hue light-to-dark ramp
   for ordered magnitude (utilisation 0–100%), a two-hue ramp with a neutral
   midpoint for signed deviation (vs target). Avoid rainbow colormaps for
   magnitude: hue changes create false boundaries and the order is not
   perceived.
5. **Diverging scales need a meaningful centre**: target, zero change, last
   year. State the centre ("white = plan").
6. **Differences are a separate encoding.** If the message is the gap
   between two series, plot the gap (one line of the difference, or diverging
   bars). Readers judge the vertical distance between two curves poorly when
   both slope.
7. **Highlight by contrast, not decoration.** One accent colour for the series
   the title talks about; others in grey. One emphasis device per chart.
8. **Direct labels beat legends** when there are few series: the reader
   matches label to line by position, not by colour.
9. **Do not encode the same variable twice without reason** (bar height *and*
   colour ramp for revenue) unless redundancy aids accessibility; do not
   encode two variables in one channel.
10. **Aspect ratio sets slope.** Choose it so the slopes that matter are
    neither flat nor near-vertical; check that the visual change matches the
    claimed change.

## ieeVisualizer notes

- Bars: `bar` mark; bar layers sharing a category are dodged side by side,
  so the comparison stays on one aligned scale (docs/RENDERING.md "Bars").
- Colour: `style.colormap` on heatmaps and coloured scatters. The library does
  not reject rainbow colormaps; choose `viridis`/`cividis` (sequential) or a
  diverging map such as `RdBu` deliberately. The skill is the guard.
- Paired encodings: `style.color_of` draws bound lines in the colour of the
  value they bound; use it rather than a second, unrelated hue.
- More than 10 series wrap the colour cycle (`colour_cycle_wrapped`
  warning); the renderer then varies line style or marker. Treat that warning
  as a signal to reduce series, not as a solution.

## Good / bad

Bad: two pies, "Orders by channel, Aug" and "Sep", to show that referrals
grew from 31% to 36%.
Good: one slope chart or paired bars with the 31% → 36% change labelled.

Bad: heatmap of team utilisation with a jet/rainbow colormap.
Good: single-hue sequential map, colourbar labelled "Utilisation (%)",
0–100 fixed so months are comparable.

Bad: two training-loss curves overlaid to show "model B learns faster" when
the gap is 0.02 nats on a 0–4 axis.
Good: plot B minus A per step with a zero reference line (and the seed
spread; see `uncertainty-display`).

## Checklist

- [ ] The comparison in the title sits on a common aligned scale.
- [ ] Bars/areas start at zero; non-zero ranges only for position encodings.
- [ ] No angle, area or volume encoding where a length would do.
- [ ] Sequential data uses a lightness ramp; diverging data a stated centre.
- [ ] No rainbow colormap for magnitude.
- [ ] If the message is a difference, the difference is plotted.
- [ ] One accent; others muted; labels direct where series are few.

Adapted in part from Anthropic's `data-visualization` skill (Apache-2.0);
changed: colour-role guidance rewritten and tied to the perception ordering.
Sources and licences: `SOURCES.md`.
